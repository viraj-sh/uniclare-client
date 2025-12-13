document.addEventListener("DOMContentLoaded", () => {
  const BASE_URL = "";
  const LOGIN_PAGE = "/static/index.html";

  // Find the "Sign Out" link
  const logoutBtn = Array.from(document.querySelectorAll('a[href="#"], a'))
    .find(a => a.textContent.trim().includes("Sign Out"));

  if (!logoutBtn) {
    console.warn("⚠️ Sign Out button not found in DOM.");
    return;
  }

  console.log("✅ Found Sign Out button.");

  logoutBtn.addEventListener("click", async (e) => {
    e.preventDefault();

    try {
      // STEP 1: Validate session
      const validateRes = await fetch(`${BASE_URL}/api/v1/auth/validate-session`, {
        method: "GET",
        credentials: "include",
        cache: "no-store",
      });

      const validateData = await validateRes.json();

      if (!validateData.success || !validateData.data?.session_valid) {
        console.log("ℹ️ Session not active. Redirecting to login...");
        window.location.href = LOGIN_PAGE;
        return;
      }

      console.log("✅ Active session found, proceeding to logout...");

      // STEP 2: Attempt logout
      const logoutRes = await fetch(`${BASE_URL}/api/v1/auth/logout`, {
        method: "POST",
        credentials: "include",
        cache: "no-store",
      });

      const logoutData = await logoutRes.json();

      if (logoutData.success && logoutData.data?.message === "Logout successful") {
        console.log("✅ Logout successful:", logoutData.data.message);
      } else if (logoutData.error?.includes("No active session")) {
        console.log("ℹ️ No active session found. Redirecting...");
      } else {
        console.warn("⚠️ Unexpected logout response:", logoutData);
      }

      // Redirect in all cases
      window.location.href = LOGIN_PAGE;
    } catch (err) {
      console.error("❌ Sign-out error:", err);
      window.location.href = LOGIN_PAGE;
    }
  });
});
