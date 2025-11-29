// ==============================
//  login.js – Unofficial Uniclare
// ==============================

document.addEventListener("DOMContentLoaded", async () => {
  const API_BASE_URL = "/api/v1";

  const loginForm = document.getElementById("login-form");
  const feedback = document.getElementById("feedback-message");
  const submitBtn = loginForm.querySelector('button[type="submit"]');
  const mobInput = document.getElementById("mob_num");
  const passInput = document.getElementById("password");

  // ------------------------------
  // Utility: Show feedback message
  // ------------------------------
  function showMessage(message, type = "info") {
    feedback.textContent = message;
    feedback.classList.remove(
      "hidden",
      "text-red-600",
      "text-green-600",
      "text-blue-600",
      "text-gray-600"
    );
    const color =
      type === "error"
        ? "text-red-600"
        : type === "success"
        ? "text-green-600"
        : type === "info"
        ? "text-blue-600"
        : "text-gray-600";
    feedback.classList.add(color);
  }

  function disableForm(state = true) {
    submitBtn.disabled = state;
    mobInput.disabled = state;
    passInput.disabled = state;
    submitBtn.classList.toggle("opacity-50", state);
    submitBtn.classList.toggle("cursor-not-allowed", state);
  }

  // ------------------------------
  // Step 1: Check API health
  // ------------------------------
  async function checkAPIHealth() {
    try {
      const [rootRes, healthRes] = await Promise.all([
        fetch(`${API_BASE_URL}/`),
        fetch(`${API_BASE_URL}/health`),
      ]);

      const rootData = await rootRes.json().catch(() => null);
      const healthData = await healthRes.json().catch(() => null);

      const rootOk =
        rootData?.success === true &&
        rootData?.data?.message === "Unofficial uniclare API - v1";
      const healthOk =
        healthData?.success === true && healthData?.data?.status === "OK";

      if (!rootOk || !healthOk) {
        showMessage(
          "⚠️ Unable to connect to the Uniclare API. Please try again later.",
          "error"
        );
        disableForm(true);
        return false;
      }
      return true;
    } catch (err) {
      console.error("API health check failed:", err);
      showMessage(
        "⚠️ Network error while contacting the API. Please check your connection.",
        "error"
      );
      disableForm(true);
      return false;
    }
  }

  // ------------------------------
  // Step 2: Validate active session
  // ------------------------------
  async function validateSession() {
    try {
      const res = await fetch(`${API_BASE_URL}/auth/validate-session`);
      const data = await res.json().catch(() => null);

      if (data?.success && data?.data?.session_valid) {
        showMessage("Active session found. Redirecting to profile...", "success");
        setTimeout(() => {
          window.location.href = "/static/pages/profile.html";
        }, 1000);
        return true;
      }
      return false;
    } catch (err) {
      console.warn("Session validation failed:", err);
      return false;
    }
  }
  // ------------------------------
  // Step 3: Handle login form submit
  // ------------------------------
  loginForm.addEventListener("submit", async (e) => {
    e.preventDefault();
    const phone = mobInput.value.trim();
    const password = passInput.value.trim();

    // Basic validation
    if (!phone || !password) {
      showMessage("Please enter both mobile number and password.", "error");
      return;
    }

    // Allow only numbers or a leading + followed by 10–13 digits (e.g., +91XXXXXXXXXX)
    const phoneRegex = /^\+?\d{10,13}$/;
    if (!phoneRegex.test(phone)) {
      showMessage(
        "Please enter a valid mobile number.",
        "error"
      );
      return;
    }

    disableForm(true);
    showMessage("Signing in...", "info");

    try {
      const res = await fetch(`${API_BASE_URL}/auth/login`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          phone_number: phone,
          password: password,
        }),
      });

      const data = await res.json().catch(() => null);

      if (
        data?.success === true &&
        data?.data?.session_id &&
        data?.data?.msg?.toLowerCase().includes("success")
      ) {
        showMessage("Login successful! Redirecting...", "success");
        setTimeout(() => {
          window.location.href = "/static/pages/profile.html";
        }, 1000);
      } else {
        showMessage("Invalid mobile number or password. Please try again.", "error");
        disableForm(false);
      }
    } catch (err) {
      console.error("Login error:", err);
      showMessage("Unable to connect to the server. Please try again.", "error");
      disableForm(false);
    }
  });

  // ------------------------------
  // Step 4: Initialize on page load
  // ------------------------------
  disableForm(true);
  showMessage("Checking server status...", "info");

  const apiHealthy = await checkAPIHealth();
  if (!apiHealthy) return;

  const hasSession = await validateSession();
  if (hasSession) return;

  // If all checks pass, enable form
  showMessage("Welcome back! Please log in to continue.", "info");
  disableForm(false);
});
