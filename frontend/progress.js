(function () {
  const SUBJECT = "dravyaguna";
  // Progress metrics are rendered only from authenticated API data; no demo analytics are used.

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
    const bar = row.querySelector("[data-progress-bar]");
    bar.style.width = percent + "%";
    bar.setAttribute("aria-valuenow", String(percent));
    const note = document.querySelector("[data-overall-progress-note]");
    if (note) note.textContent = total ? "Across " + total + " tracked syllabus resources" : "No tracked syllabus resources yet";
  }

  function renderAnalytics(data) {
    const metrics = data || {};
    const average = document.querySelector("[data-assessment-average]");
    const attempts = document.querySelector("[data-assessment-attempts]");
    if (average) average.textContent = metrics.average_percent == null ? "—" : metrics.average_percent + "%";
    if (attempts) attempts.textContent = metrics.attempt_count ? "Across " + metrics.attempt_count + " submitted attempts" : "No submitted assessments yet";

    const list = document.querySelector("[data-score-list]");
    if (!list) return;
    list.replaceChildren();
    const daily = Array.isArray(metrics.daily_minutes) ? metrics.daily_minutes : [];
    const bars = document.querySelectorAll("[data-study-bars] i");
    if (daily.length && bars.length) {
      const max = Math.max(1, ...daily.map((item) => Number(item.minutes) || 0));
      daily.slice(-bars.length).forEach((item, index) => {
        const value = Math.max(0, Number(item.minutes) || 0);
        bars[index].style.height = Math.round((value / max) * 100) + "%";
        bars[index].setAttribute("aria-label", value + " minutes");
      });
      const note = document.querySelector("[data-study-time-note]");
      if (note) note.textContent = "Synced from your study activity";
    }

    const assessments = metrics.assessments || [];
    const points = document.querySelector("[data-score-points]");
    if (points) {
      points.replaceChildren();
      assessments.slice(-6).forEach((item, index) => {
        const point = document.createElement("i");
        const value = Math.max(0, Math.min(100, Number(item.best_percent) || 0));
        point.style.bottom = value + "%";
        point.setAttribute("aria-label", value + "%");
        points.appendChild(point);
      });
    }

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
      document.querySelectorAll("[data-streak],[data-study-time],[data-study-trend],[data-calendar-trend]").forEach((el) => { el.textContent = "—"; });
      const studyNote = document.querySelector("[data-study-time-note]");
      const streakNote = document.querySelector("[data-streak-note]");
      const calendarNote = document.querySelector("[data-calendar-note]");
      if (studyNote) studyNote.textContent = "Sign in to sync your study time";
      if (streakNote) streakNote.textContent = "Sign in to sync your streak";
      if (calendarNote) calendarNote.textContent = "Sign in to sync your study activity.";
      const state = document.querySelector("[data-ui-state]");
      const authenticated = window.AaptaKoshaSession && window.AaptaKoshaSession.authenticated;
      const points = document.querySelector("[data-score-points]");
      if (points) points.replaceChildren();
      document.querySelectorAll("[data-study-bars] i").forEach((bar) => { bar.style.height = "0%"; });
      if (state && (authenticated || window.AAPTAKOSHA_API_BASE)) {
        window.AaptaKoshaUi?.status(
          state,
          error.message || "Unable to load progress.",
          "error"
        );
      }
    });
})();
