document.addEventListener("DOMContentLoaded", async () => {
  const API_BASE = "/api";
  const usernameEl = document.getElementById("sidebar-username");
  if (!usernameEl) return; // Safety check

  // Validate session first
  async function validateSession() {
    try {
      const res = await fetch(`${API_BASE}/auth/validate-session`, {
        method: "GET",
        credentials: "include",
        cache: "no-store",
      });
      const data = await res.json();
      return data.success;
    } catch (err) {
      console.error("Sidebar session validation error:", err);
      return false;
    }
  }

  // Format name by removing father/mother names and limiting length
  function formatName(fullName, fatherName, motherName) {
    if (!fullName) return "User";

    let cleanName = fullName.trim();

    // Remove father's and mother's names (case-insensitive)
    [fatherName, motherName].forEach((n) => {
      if (n && typeof n === "string" && n.trim() !== "") {
        const pattern = new RegExp(`\\b${n.trim()}\\b`, "i");
        cleanName = cleanName.replace(pattern, "").trim();
      }
    });

    // Replace multiple spaces with single
    cleanName = cleanName.replace(/\s+/g, " ");

    // Limit to 20 chars max
    const limit = 20;
    if (cleanName.length > limit) {
      cleanName = cleanName.slice(0, limit - 3).trim() + "...";
    }

    return cleanName || "User";
  }

  async function loadUsername() {
    try {
      const res = await fetch(`${API_BASE}/profile`, {
        method: "GET",
        credentials: "include",
        cache: "force-cache", // use cached response for 1h
      });
      const result = await res.json();

      if (!result.success || !result.data) throw new Error("Invalid response");

      const { full_name, fath_name, mot_name } = result.data;
      const displayName = formatName(full_name, fath_name, mot_name);
      usernameEl.textContent = displayName;
    } catch (err) {
      console.warn("Failed to fetch sidebar username:", err);
      usernameEl.textContent = "User";
    }
  }

  const isValid = await validateSession();
  if (isValid) {
    await loadUsername();
  } else {
    usernameEl.textContent = "Guest";
  }
});
