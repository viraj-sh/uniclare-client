document.addEventListener("DOMContentLoaded", async () => {
  const API_BASE = "/api/v1";

  // Elements
  const studentNameEl = document.getElementById("student-name");
  const usnEl = document.getElementById("usn");
  const programmeEl = document.getElementById("programme");
  const collegeEl = document.getElementById("college");
  const resultsListEl = document.getElementById("results-list");
  const resultsErrorEl = document.getElementById("results-error");

  // Utility: Convert "23/07/2025" → "23 July 2025"
  function formatDate(dateStr) {
    if (!dateStr || !dateStr.includes("/")) return dateStr;
    try {
      const [day, month, year] = dateStr.split("/");
      const monthNames = [
        "January",
        "February",
        "March",
        "April",
        "May",
        "June",
        "July",
        "August",
        "September",
        "October",
        "November",
        "December",
      ];
      const monthIndex = parseInt(month, 10) - 1;
      return `${day} ${monthNames[monthIndex]} ${year}`;
    } catch {
      return dateStr;
    }
  }

  // Skeleton: start and stop (consistent with profile.js)
  function startSkeleton() {
    [studentNameEl, usnEl, programmeEl, collegeEl].forEach((el) => {
      if (el) {
        el.textContent = "";
        el.classList.add("skeleton", "pulse");
      }
    });

    const skeletonCard = `
      <div class="result-card border border-gray-200 rounded-lg p-4 shadow-sm">
        <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
          <div class="space-y-2">
            <p class="skeleton pulse w-24"></p>
            <p class="skeleton pulse w-48"></p>
            <p class="skeleton pulse w-40"></p>
            <p class="skeleton pulse w-32"></p>
            <p class="skeleton pulse w-28"></p>
          </div>
          <div>
            <div class="skeleton pulse w-24"></div>
          </div>
        </div>
      </div>
    `;
    resultsListEl.innerHTML = skeletonCard + skeletonCard + skeletonCard;
    resultsErrorEl.classList.add("hidden");
  }

  function stopSkeleton() {
    [studentNameEl, usnEl, programmeEl, collegeEl].forEach((el) => {
      if (el) el.classList.remove("skeleton", "pulse");
    });
  }

  // Utility: Create a result card
  function createResultCard(result) {
    const card = document.createElement("div");
    card.className =
      "result-card border border-gray-200 rounded-lg p-4 shadow-sm hover:shadow-md transition-shadow duration-200";

    const mcLine = result.mc_no
      ? `<p class="text-sm text-gray-800"><span class="font-medium">MC No.:</span> ${result.mc_no}</p>`
      : "";

    card.innerHTML = `
      <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        <div class="space-y-1">
          <p class="text-sm text-green-800 font-medium">${result.sem}</p>
          <p class="text-sm text-gray-800">
            <span class="font-medium">Exam Session:</span> ${result.exam_date}
          </p>
          <p class="text-sm text-gray-800">
            <span class="font-medium">Result Date:</span> ${formatDate(result.result_date)}
          </p>
          <p class="text-sm text-gray-800">
            <span class="font-medium">Status:</span> ${result.status}
          </p>
          ${mcLine}
        </div>
        <div>
          <button
            class="view-btn bg-green-800 text-white text-sm font-medium px-4 py-2 rounded-lg hover:bg-green-900 transition-colors"
            data-year-id="${result.year_id}">
            View
          </button>
        </div>
      </div>
    `;
    return card;
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

      if (!data.success || !data.data?.session_valid) {
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

  // Fetch and populate results
  async function loadResults() {
    startSkeleton();
    try {
      const res = await fetch(`${API_BASE}/results`, {
        method: "GET",
        credentials: "include",
        cache: "no-store",
      });
      const data = await res.json();

      if (!data.success || !data.data) {
        throw new Error(data.error || "Failed to fetch results.");
      }

      const results = data.data;

      if (!Array.isArray(results) || results.length === 0) {
        resultsListEl.innerHTML = "";
        resultsErrorEl.textContent = "No results available yet.";
        resultsErrorEl.classList.remove("hidden");
        stopSkeleton();
        return;
      }

      // Common info (from first record)
      const sample = results[0];
      studentNameEl.textContent = `Student Name: ${sample.full_name}`;
      usnEl.textContent = `USN: ${sample.reg_no}`;
      programmeEl.textContent = `Programme: ${sample.degree_id} - ${sample.degree_name}`;
      collegeEl.textContent = `College: ${sample.coll_id} - ${sample.coll_name}`;

      // Populate results list
      resultsListEl.innerHTML = "";
      results.forEach((r) => {
        const card = createResultCard(r);
        resultsListEl.appendChild(card);
      });

      // Add click listeners for View buttons
      const viewButtons = document.querySelectorAll(".view-btn");
      viewButtons.forEach((btn) => {
        btn.addEventListener("click", () => {
          const yearId = btn.getAttribute("data-year-id");
          if (yearId) {
            window.location.href = `/static/pages/result_details.html?exam_id=${encodeURIComponent(yearId)}`;
          } else {
            alert("Missing exam identifier!");
          }
        });
      });

      stopSkeleton();
    } catch (err) {
      console.error("Error loading results:", err);
      resultsListEl.innerHTML = "";
      resultsErrorEl.textContent = "⚠️ Failed to load results. Please try again later.";
      resultsErrorEl.classList.remove("hidden");
      stopSkeleton();
    }
  }

  // Initialize
  if (await validateSession()) {
    await loadResults();
  }
});
