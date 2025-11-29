document.addEventListener("DOMContentLoaded", async () => {
  const BASE_URL = "";
  const LOGIN_PAGE = "/static/index.html";

  // Utility: Redirect to login
  const redirectToLogin = () => {
    window.location.href = LOGIN_PAGE;
  };

  // ✅ STEP 1: Validate Session
  try {
    const sessionRes = await fetch(`${BASE_URL}/api/v1/auth/validate-session`, {
      method: "GET",
      credentials: "include",
      cache: "no-store",
    });

    if (!sessionRes.ok) throw new Error("Session validation failed");
    const sessionData = await sessionRes.json();

    if (!sessionData.success || !sessionData.data?.session_valid) {
      console.warn("Session invalid:", sessionData);
      redirectToLogin();
      return;
    }

    console.log("✅ Session validated:", sessionData.data.message);
  } catch (err) {
    console.error("Session check error:", err);
    redirectToLogin();
    return;
  }

  // ✅ STEP 2: Get exam ID from query string
  const params = new URLSearchParams(window.location.search);
  const examId = params.get("exam_id");

  if (!examId) {
    alert("No exam ID provided in the URL!");
    window.location.href = "/static/pages/results.html";
    return;
  }

  // ✅ STEP 3: Fetch Result Details
  try {
    const res = await fetch(`${BASE_URL}/api/v1/results/${examId}`, {
      method: "GET",
      credentials: "include",
      cache: "no-store",
    });

    if (!res.ok) throw new Error("Failed to fetch result details");

    const resultData = await res.json();

    if (!resultData.success || !resultData.data) {
      alert("No result data found for this exam.");
      return;
    }

    const data = resultData.data;

    // ✅ STEP 4: Populate Header Info
    document.getElementById("student-name").textContent = data.full_name || "N/A";
    document.getElementById("student-usn").textContent = data.reg_no || "N/A";
    document.getElementById("college-name").textContent = data.col_name || "N/A";
    document.getElementById("exam-name").textContent = data.full_sem || "N/A";
    document.getElementById("exam-date").textContent = data.exam_date
      ? `Exam: ${data.exam_date}`
      : "";
    document.getElementById("result-date").textContent = data.result_date
      ? `Result Date: ${data.result_date}`
      : "";

    // ✅ STEP 5: Summary Cards (with Percentage)
    document.getElementById("sgpa").textContent = data.sgpa || "--";
    document.getElementById("cgpa").textContent = data.cgpa || "--";
    document.getElementById("credits").textContent = data.total_credits || "--";
    document.getElementById("percentage").textContent =
      data.percentage && data.percentage !== "0"
        ? `${parseFloat(data.percentage).toFixed(2)}%`
        : "--";
    document.getElementById("final-result").textContent = data.result || "--";

    // ✅ STEP 6: Additional Dates
    document.getElementById("reval-date").innerHTML = `<span class="font-semibold">Revaluation Date:</span> ${
      data.rv_date || "--"
    }`;
    document.getElementById("retot-date").innerHTML = `<span class="font-semibold">Re-totaling Date:</span> ${
      data.rt_date || "--"
    }`;
    document.getElementById("pc-date").innerHTML = `<span class="font-semibold">Provisional Certificate Date:</span> ${
      data.pc_date || "--"
    }`;

    // ✅ STEP 7: Subjects Table (Fixed column mapping)
    const tbody = document.getElementById("subjects-table-body");
    tbody.innerHTML = "";

    if (Array.isArray(data.subjects) && data.subjects.length > 0) {
      data.subjects.forEach((subject) => {
        const tr = document.createElement("tr");
        tr.innerHTML = `
          <td class="px-4 py-3">${subject.no || ""}</td>
          <td class="px-4 py-3 font-medium text-gray-900">${subject.sub || ""}</td>
          <td class="px-4 py-3">${subject.type || ""}</td>
          <td class="px-4 py-3">${subject.end_marks || "-"}</td>
          <td class="px-4 py-3">${subject.viva_marks || "-"}</td>
          <td class="px-4 py-3">${subject.ia_marks || "-"}</td>
          <td class="px-4 py-3">${subject.total_marks || "-"}</td>
          <td class="px-4 py-3">${subject.credit_hrs || "-"}</td>
          <td class="px-4 py-3">${subject.grade_points || "-"}</td>
          <td class="px-4 py-3">${subject.credit_points || "-"}</td>
          <td class="px-4 py-3 font-semibold ${
            subject.grade === "F" ? "text-red-600" : "text-green-700"
          }">${subject.grade || "-"}</td>
          <td class="px-4 py-3 ${
            subject.remarks === "Fail" ? "text-red-600" : "text-gray-800"
          }">${subject.remarks || "-"}</td>
        `;
        tbody.appendChild(tr);
      });
    } else {
      tbody.innerHTML = `<tr><td colspan="12" class="text-center py-4 text-gray-500">No subjects found</td></tr>`;
    }

    // ✅ STEP 8: Feedback if Fail
    const feedback = document.getElementById("result-feedback");
    const hasFail = data.subjects?.some((sub) => sub.remarks === "Fail");
    if (hasFail) {
      feedback.classList.remove("hidden");
      feedback.textContent =
        "⚠ Some subjects are marked as 'Fail'. Please apply for revaluation if applicable.";
      feedback.classList.add("text-red-600");
    }
  } catch (err) {
    console.error("Error fetching result details:", err);
    alert("An error occurred while fetching result details.");
  }
});
