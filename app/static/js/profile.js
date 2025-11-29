document.addEventListener("DOMContentLoaded", async () => {
  const API_BASE = "/api/v1";

  const profileError = document.getElementById("profile-error");
  const profileSection = document.getElementById("profile-section");

  // Utility to safely set text content
  const setText = (id, value) => {
    const el = document.getElementById(id);
    if (el) el.textContent = value && value !== "" ? value : "NA";
  };

  // Validate user session before loading anything
  async function validateSession() {
    try {
      const res = await fetch(`${API_BASE}/auth/validate-session`, {
        method: "GET",
        credentials: "include",
      });

      const data = await res.json();
      if (!data.success) {
        window.location.href = "/static/index.html";
        return false;
      }
      return true;
    } catch (err) {
      console.error("Session validation failed:", err);
      window.location.href = "/static/index.html";
      return false;
    }
  }

  // Fetch and display profile details
  async function loadProfile() {
    try {
      const res = await fetch(`${API_BASE}/profile`, {
        method: "GET",
        credentials: "include",
      });

      const result = await res.json();

      // Handle failed API response
      if (!result.success || !result.data) {
        throw new Error(result.error || "Failed to fetch profile");
      }

      const data = result.data;

      // Populate UI fields
      document.getElementById("student-photo").src = data.photo || "";
      setText("student-name", data.full_name);
      setText("degree-name", data.degree_name);
      setText("college-name", data.coll_name);
      setText("reg-no", data.reg_no);
      setText("father-name", data.fath_name);
      setText("mother-name", data.mot_name);
      setText("category", data.category);
      setText("degree-id", data.degree_id);
      setText("college-id", data.coll_id);
      setText("exam-date", data.exam_date);
      setText("student-mobile", data.smobile_no);
      setText("parent-mobile", data.pmobile_no);
      setText("student-email", data.semail);
      setText("fee-type", data.fee_type);

      // Hide error message if previously shown
      profileError.classList.add("hidden");
      profileSection.classList.remove("hidden");
    } catch (err) {
      console.error("Error loading profile:", err);
      profileSection.classList.add("hidden");
      profileError.classList.remove("hidden");
    }
  }

  // --- Initialize ---
  const isValid = await validateSession();
  if (isValid) {
    await loadProfile();
  }
});
