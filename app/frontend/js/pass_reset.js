document.addEventListener("DOMContentLoaded", async () => {
  const API_BASE = "/api";
  const LOGIN_PAGE = "/static/index.html";
  const PROFILE_PAGE = "/static/pages/profile.html";

  // Elements (IDs match your HTML)
  const form = document.getElementById("pass-reset-form");
  const phoneInput = document.getElementById("phone");
  const otpSection = document.getElementById("otp-section");
  const otpInput = document.getElementById("otp");
  const passwordInput = document.getElementById("password");
  const confirmPasswordInput = document.getElementById("confirm-password");
  const sendOtpBtn = document.getElementById("send-otp-btn");
  const resetPassBtn = document.getElementById("reset-pass-btn"); // matches HTML
  const feedback = document.getElementById("feedback-message");
  const togglePasswordBtn = document.getElementById("toggle-password");
  const toggleConfirmPasswordBtn = document.getElementById("toggle-confirm-password");
  const eyeIcon = document.getElementById("eye-icon");
  const eyeIconConfirm = document.getElementById("eye-icon-confirm");

  let canResend = true;
  let resendTimer = null;

  // Helper: show feedback
  function showMessage(text = "", type = "info") {
    if (!feedback) return;
    feedback.textContent = text;
    feedback.classList.remove("hidden", "text-red-600", "text-green-600", "text-blue-600", "text-gray-600");
    const cls = type === "error" ? "text-red-600" : type === "success" ? "text-green-600" : "text-blue-600";
    feedback.classList.add(cls);
    if (!text) feedback.classList.add("hidden");
  }

  // Helper: enable/disable UI controls
  function setUIState(disabled = true) {
    [phoneInput, otpInput, passwordInput, confirmPasswordInput, sendOtpBtn, resetPassBtn].forEach(el => {
      if (!el) return;
      el.disabled = disabled;
    });
    if (sendOtpBtn) sendOtpBtn.classList.toggle("opacity-50", disabled);
    if (resetPassBtn) resetPassBtn.classList.toggle("opacity-50", disabled);
  }

  // Validate session: redirect to profile if active
  async function validateSession() {
    try {
      const res = await fetch(`${API_BASE}/auth/validate-session`, {
        method: "GET",
        credentials: "include",
        cache: "no-store",
      });
      if (!res.ok) {
        console.warn("validate-session returned non-ok:", res.status);
        return false;
      }
      const data = await res.json().catch(() => null);
      if (data?.success && data?.data?.session_valid) {
        window.location.href = PROFILE_PAGE;
        return true;
      }
      return false;
    } catch (err) {
      console.warn("Session validation error:", err);
      return false;
    }
  }

  // Phone number validator: allows +<cc><10digits> or just 10 digits
  function validatePhoneNumber(phone) {
    if (!phone) return null;
    const cleaned = phone.replace(/\s+/g, "");
    // Accepts +<1-3 digits> followed by 10 digits OR exactly 10 digits
    if (/^(\+\d{1,3})?\d{10}$/.test(cleaned) && cleaned.length >= 10 && cleaned.length <= 13) {
      return cleaned;
    }
    return null;
  }

  // Send OTP
  async function sendOTP() {
    showMessage("", "info");
    const raw = phoneInput?.value?.trim() ?? "";
    const validPhone = validatePhoneNumber(raw);
    if (!validPhone) {
      showMessage("Please enter a valid 10–13 digit phone number.", "error");
      return;
    }
    if (!canResend) return;

    setUIState(true);
    showMessage("Sending OTP...", "info");
    try {
      const res = await fetch(`${API_BASE}/auth/password-reset/send-otp`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        credentials: "include",
        body: JSON.stringify({ phone_number: validPhone }),
      });

      const data = await res.json().catch(() => null);
      if (data?.success && data?.data?.status === "OTP sent") {
        showMessage("OTP sent successfully! Enter OTP and new password.", "success");
        if (otpSection) otpSection.classList.remove("hidden");
        startResendCooldown();
      } else {
        // show backend message if available
        const errMsg = data?.error || data?.data?.status || "Failed to send OTP. Ensure number is registered.";
        showMessage(errMsg, "error");
      }
    } catch (err) {
      console.error("sendOTP error:", err);
      showMessage("Network error while sending OTP.", "error");
    } finally {
      setUIState(false);
    }
  }

  // Start resend cooldown
  function startResendCooldown() {
    canResend = false;
    let seconds = 20;
    if (sendOtpBtn) sendOtpBtn.textContent = `Resend OTP (${seconds}s)`;
    resendTimer = setInterval(() => {
      seconds--;
      if (sendOtpBtn) sendOtpBtn.textContent = `Resend OTP (${seconds}s)`;
      if (seconds <= 0) {
        clearInterval(resendTimer);
        resendTimer = null;
        canResend = true;
        if (sendOtpBtn) sendOtpBtn.textContent = "Resend OTP";
      }
    }, 1000);
  }

  // Toggle password visibility
  function toggleVisibility(inputEl, iconEl) {
    if (!inputEl) return;
    inputEl.type = inputEl.type === "password" ? "text" : "password";
    // keep icon as is; you can swap SVGs if you want visual change
    if (iconEl) iconEl.classList.toggle("opacity-60");
  }

  // Reset password (submit)
  async function verifyAndReset(e) {
    if (e && e.preventDefault) e.preventDefault();
    showMessage("", "info");

    const rawPhone = phoneInput?.value?.trim() ?? "";
    const otp = otpInput?.value?.trim() ?? "";
    const password = passwordInput?.value ?? "";
    const confirm = confirmPasswordInput?.value ?? "";

    const validPhone = validatePhoneNumber(rawPhone);
    if (!validPhone) {
      showMessage("Invalid phone number.", "error");
      return;
    }
    if (!otp || !/^\d{6}$/.test(otp)) {
      showMessage("Please enter a valid 6-digit OTP.", "error");
      return;
    }
    if (!password || password.length < 6) {
      showMessage("Password must be at least 6 characters long.", "error");
      return;
    }
    if (password !== confirm) {
      showMessage("Passwords do not match.", "error");
      return;
    }

    setUIState(true);
    showMessage("Verifying OTP and resetting password...", "info");

    try {
      const payload = {
        mobile: validPhone.replace(/^\+91/, ""), // remove +91 if present
        otp,
        new_password: password,
      };

      const res = await fetch(`${API_BASE}/auth/password-reset/confirm`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        credentials: "include",
        body: JSON.stringify(payload),
      });

      const data = await res.json().catch(() => null);

      if (data?.success && data?.data?.status === "Password reset successful") {
        showMessage("Password reset successful! Redirecting to login...", "success");
        setTimeout(() => (window.location.href = LOGIN_PAGE), 1400);
      } else {
        const err = data?.error || data?.data?.status || "Failed to reset password. Check OTP/phone.";
        showMessage(err, "error");
      }
    } catch (err) {
      console.error("verifyAndReset error:", err);
      showMessage("Network error during password reset.", "error");
    } finally {
      setUIState(false);
    }
  }

  // Password match check to enable/disable reset button
  function checkPasswordMatchAndToggle() {
    const p = passwordInput?.value ?? "";
    const c = confirmPasswordInput?.value ?? "";
    const match = p && c && p === c;
    if (resetPassBtn) {
      resetPassBtn.disabled = !match;
      resetPassBtn.classList.toggle("opacity-50", !match);
      resetPassBtn.classList.toggle("cursor-not-allowed", !match);
    }
    // only show mismatch message if user typed something
    if (!match && c) {
      showMessage("Passwords do not match.", "error");
    } else {
      showMessage("", "info");
    }
  }

  // attach UI handlers
  if (togglePasswordBtn) togglePasswordBtn.addEventListener("click", () => toggleVisibility(passwordInput, eyeIcon));
  if (toggleConfirmPasswordBtn) toggleConfirmPasswordBtn.addEventListener("click", () => toggleVisibility(confirmPasswordInput, eyeIconConfirm));
  if (passwordInput) passwordInput.addEventListener("input", checkPasswordMatchAndToggle);
  if (confirmPasswordInput) confirmPasswordInput.addEventListener("input", checkPasswordMatchAndToggle);

  // Initialize button state
  if (resetPassBtn) {
    resetPassBtn.disabled = true;
    resetPassBtn.classList.add("opacity-50", "cursor-not-allowed");
  }

  // Attach event listeners only after session check
  const hasSession = await validateSession();
  if (!hasSession) {
    // not logged in: allow send OTP and reset flow
    if (sendOtpBtn) sendOtpBtn.addEventListener("click", sendOTP);
    if (form) form.addEventListener("submit", verifyAndReset);
  }
});
