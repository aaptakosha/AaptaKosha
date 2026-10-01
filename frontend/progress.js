(function () {
  const SUBJECT = "dravyaguna";

  async function loadProgress() {
    if (!window.AaptaKoshaApi) throw new Error("API client unavailable");
    return window.AaptaKoshaApi.request("/progress");
  }

  function renderProgress(items) {
    const row = Array.from(document.querySelectorAll(".subject-row"))
      .find((el) => el.dataset.subject === SUBJECT);
    if (!row) return;

    const completed = items.filter((item) => item.status === "completed").length;
    const total = items.length;
    const percent = total
      ? Math.round(items.reduce((sum, item) => sum + item.completion_percent, 0) / total)
      : 0;

    row.querySelector("[data-progress-percent]").textContent = percent + "%";
    row.querySelector("[data-progress-summary]").textContent =
      total ? completed + " of " + total + " tracked resources" : "No tracked resources yet";
    row.querySelector("[data-progress-bar]").style.width = percent + "%";
  }

  window.AaptaKoshaSessionReady
    ?.then(loadProgress)
    .then((data) => renderProgress(data.progress || []))
    .catch(() => {
      // Keep designed fallback values when the API is unavailable or the learner is signed out.
    });
})();
