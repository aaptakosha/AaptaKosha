(function () {
  const SUBJECT = "dravyaguna";

  async function loadProgress() {
    if (!window.AaptaKoshaApi) throw new Error("API client unavailable");
    return window.AaptaKoshaApi.request("/progress");
  }

  async function loadAnalytics() {
    if (!window.AaptaKoshaApi) throw new Error("API client unavailable");
    return window.AaptaKoshaApi.request("/analytics");
  }

  function renderProgress(items) {
    const row = Array.from(document.querySelectorAll(".subject-row"))
      .find((el) => el.dataset.subject === SUBJECT);
    if (!row) return;

    const syllabusItems = items.filter((item) => item.resource_type !== "assessment");
    const completed = syllabusItems.filter((item) => item.status === "completed").length;
    const total = syllabusItems.length;
    const percent = total
      ? Math.round(syllabusItems.reduce((sum, item) => sum + item.completion_percent, 0) / total)
      : 0;

    const overall = document.querySelector("[data-overall-progress]");
    if (overall) overall.textContent = percent + "%";
    row.querySelector("[data-progress-percent]").textContent = percent + "%";
    row.querySelector("[data-progress-summary]").textContent =
      total ? completed + " of " + total + " tracked syllabus resources" : "No tracked syllabus resources yet";
    row.querySelector("[data-progress-bar]").style.width = percent + "%";
    const note = document.querySelector("[data-overall-progress-note]");
    if (note) note.textContent = total ? "Across " + total + " tracked syllabus resources" : "No tracked syllabus resources yet";
  }

  function renderAnalytics(data) {
    const metrics = data || {};
    const average = document.querySelector("[data-assessment-average]");
    const attempts = document.querySelector("[data-assessment-attempts]");
    if (average) average.textContent = (metrics.average_percent || 0) + "%";
    if (attempts) attempts.textContent = "Across " + (metrics.attempt_count || 0) + " submitted attempts";

    const list = document.querySelector("[data-score-list]");
    if (!list) return;
    list.replaceChildren();
    const assessments = metrics.assessments || [];
    assessments.forEach((item) => {
      const span = document.createElement("span");
      span.textContent = item.assessment_id + " · " + (item.best_percent || 0) + "% best";
      list.appendChild(span);
    });
    if (!assessments.length) {
      const span = document.createElement("span");
      span.textContent = "No submitted assessments yet";
      list.appendChild(span);
    }
  }

  window.AaptaKoshaSessionReady
    ?.then(async () => {
      const [progress, analytics] = await Promise.all([loadProgress(), loadAnalytics()]);
      renderProgress(progress.progress || []);
      renderAnalytics(analytics);
    })
    .catch((error) => {
      const state = document.querySelector("[data-ui-state]");
      const authenticated = window.AaptaKoshaSession && window.AaptaKoshaSession.authenticated;
      if (state && (authenticated || window.AAPTAKOSHA_API_BASE)) {
        window.AaptaKoshaUi?.status(
          state,
          error.message || "Unable to load progress.",
          "error"
        );
      }
    });
})();
