document.addEventListener("DOMContentLoaded", async () => {
  const API_BASE = "/api";

  // Elements
  const fatherInput = document.getElementById("father-name");
  const motherInput = document.getElementById("mother-name");
  const abcInput = document.getElementById("abc-id");
  const fullNameEl = document.getElementById("full-name");
  const regNoEl = document.getElementById("reg-no");
  const profilePhoto = document.getElementById("student-photo");
  const saveBtn = document.getElementById("save-profile-btn");
  const feedback = document.getElementById("feedback-message");

  let originalData = {};
  let isEdited = false;

  // Utility: Show message
  function showMessage(message, type = "info") {
    feedback.textContent = message;
    feedback.classList.remove("hidden", "text-red-600", "text-green-600", "text-blue-600");
    const color =
      type === "error"
        ? "text-red-600"
        : type === "success"
        ? "text-green-600"
        : "text-blue-600";
    feedback.classList.add(color);
  }

  // Disable or enable UI
  function disableUI(state = true) {
    [fatherInput, motherInput, abcInput, saveBtn].forEach((el) => (el.disabled = state));
    saveBtn.classList.toggle("opacity-50", state);
    saveBtn.classList.toggle("cursor-not-allowed", state);
  }

  // Validate session
  async function validateSession() {
    try {
      const res = await fetch(`${API_BASE}/auth/validate-session`, {
        method: "GET",
        credentials: "include",
        cache: "no-store",
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

  // Load editable profile data
  async function loadProfileData() {
    try {
      disableUI(true);
      showMessage("Loading profile information...", "info");

      const res = await fetch(`${API_BASE}/profile/editable`, {
        method: "GET",
        credentials: "include",
        cache: "no-store",
      });
      const result = await res.json();

      if (!result.success || !result.data) {
        showMessage("Failed to fetch profile details.", "error");
        return;
      }

      const data = result.data;
      originalData = {
        father_name: data.fath_name || "",
        mother_name: data.mot_name || "",
        abc_no: data.abc_id || "",
      };

      // Populate non-editable fields
      fullNameEl.textContent = data.full_name || "NA";
      regNoEl.textContent = data.reg_no || "NA";
      if (profilePhoto && data.sphoto) {
        profilePhoto.src = data.sphoto.startsWith("http")
          ? data.sphoto
          : `https://university-student-photos.s3.ap-south-1.amazonaws.com/051/${data.sphoto}`;
      }

      // Populate editable inputs
      fatherInput.value = originalData.father_name;
      motherInput.value = originalData.mother_name;
      abcInput.value = originalData.abc_no;

      showMessage("", "info");
      feedback.classList.add("hidden");
    } catch (err) {
      console.error("Failed to load editable profile:", err);
      showMessage("Network error while fetching profile.", "error");
    } finally {
      disableUI(false);
    }
  }

  // Detect changes
  function detectChanges() {
    const currentData = {
      father_name: fatherInput.value.trim(),
      mother_name: motherInput.value.trim(),
      abc_no: abcInput.value.trim(),
    };

    isEdited =
      currentData.father_name !== originalData.father_name ||
      currentData.mother_name !== originalData.mother_name ||
      currentData.abc_no !== originalData.abc_no;

    const allFilled =
      currentData.father_name && currentData.mother_name && currentData.abc_no;

    saveBtn.disabled = !(isEdited && allFilled);
    saveBtn.classList.toggle("opacity-50", !(isEdited && allFilled));
    saveBtn.classList.toggle("cursor-not-allowed", !(isEdited && allFilled));
  }

  // Save edited profile
  async function saveProfileChanges() {
    if (!isEdited) return;

    const father_name = fatherInput.value.trim();
    const mother_name = motherInput.value.trim();
    const abc_no = abcInput.value.trim();

    if (!father_name || !mother_name || !abc_no) {
      showMessage("All fields are required.", "error");
      return;
    }

    disableUI(true);
    showMessage("Saving changes...", "info");

    try {
      const res = await fetch(`${API_BASE}/profile/edit`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        credentials: "include",
        body: JSON.stringify({
          father_name,
          mother_name,
          abc_no,
        }),
      });

      const data = await res.json();

      if (data.success && data.data) {
        showMessage("Profile updated successfully!", "success");
        setTimeout(() => window.location.reload(), 1200);
      } else {
        showMessage("Failed to update profile. Please try again.", "error");
      }
    } catch (err) {
      console.error("Profile edit failed:", err);
      showMessage("Network error while saving profile.", "error");
    } finally {
      disableUI(false);
    }
  }

  // Attach listeners
  [fatherInput, motherInput, abcInput].forEach((input) => {
    input.addEventListener("input", detectChanges);
  });

  saveBtn.addEventListener("click", saveProfileChanges);

  // Initialize
  if (await validateSession()) {
    await loadProfileData();
    detectChanges();
  }
});
