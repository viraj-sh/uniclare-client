document.addEventListener("DOMContentLoaded", async () => {
  const API_BASE = "/api/v1";

  const profileError = document.getElementById("profile-error");
  const profileSection = document.getElementById("profile-section");

  // Utility to safely set text content
  const setText = (id, value) => {
    const el = document.getElementById(id);
    if (!el) return;
    el.textContent = value && value !== "" ? value : "NA";
    // remove skeleton once populated
    el.classList.remove("skeleton", "pulse");
  };

  const photoImg = document.getElementById("student-photo");
  const photoSkeleton = document.getElementById("student-photo-skeleton");

  function startSkeleton() {
    // all dynamic IDs
    const ids = [
      "student-name","degree-name","college-name","reg-no","father-name","mother-name",
      "category","degree-id","college-id","exam-date","student-mobile","parent-mobile",
      "student-email","fee-type"
    ];
    ids.forEach(id => {
      const el = document.getElementById(id);
      if (el) {
        // clear content to show :empty skeleton bar
        el.textContent = "";
        el.classList.add("skeleton", "pulse");
      }
    });
    // image: show skeleton, hide img
    if (photoSkeleton) photoSkeleton.classList.remove("hidden");
    if (photoImg) photoImg.classList.add("hidden");
  }

  function stopSkeleton() {
    const ids = [
      "student-name","degree-name","college-name","reg-no","father-name","mother-name",
      "category","degree-id","college-id","exam-date","student-mobile","parent-mobile",
      "student-email","fee-type"
    ];
    ids.forEach(id => {
      const el = document.getElementById(id);
      if (el) el.classList.remove("skeleton", "pulse");
    });
    if (photoSkeleton) photoSkeleton.classList.add("hidden");
    if (photoImg) photoImg.classList.remove("hidden");
  }

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
    startSkeleton();
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
      if (photoImg) {
        if (data.photo && data.photo !== "") {
          photoImg.src = data.photo;
        } else {
          // keep skeleton, don't show broken image
          photoImg.removeAttribute("src");
        }
      }

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

      // stop skeletons and reveal image
      stopSkeleton();
    } catch (err) {
      console.error("Error loading profile:", err);
      // stop skeletons and show error
      stopSkeleton();
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
