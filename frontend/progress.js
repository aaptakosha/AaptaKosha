(function () {
  const API_BASE = "/api";
  const SUBJECT = "dravyaguna";

  async function loadProgress() {
    const response = await fetch(API_BASE + "/progress?subject_id=" + encodeURIComponent(SUBJECT), {
      headers: { Accept: "application/json" }
    });
    if (!response.ok) throw new Error("Progress request failed");
    return response.json();
  }

  function renderProgress(items) {
    const row = Array.from(document.querySelectorAll(".subject-row"))
      .find((el) => el.dataset.subject === SUBJECT);
    if (!row) return;

    const completed = items.filter((item) => item.status === "completed").length;
    const total = items.length;
    const percent = total ? Math.round(items.reduce((sum, item) => sum + item.completion_percent, 0) / total) : 0;

    row.querySelector("[data-progress-percent]").textContent = percent + "%";
    row.querySelector("[data-progress-summary]").textContent =
      total ? completed + " of " + total + " tracked resources" : "No tracked resources yet";
    row.querySelector("[data-progress-bar]").style.width = percent + "%";
  }

  loadProgress().then((data) => renderProgress(data.progress || [])).catch(() => {
    // Keep the designed fallback values when the API is temporarily unavailable.
  });
})();
