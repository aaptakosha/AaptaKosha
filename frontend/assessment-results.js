(() => {
  const api = window.AaptaKoshaAssessment;
  const key = "aaptakosha.assessment.session.result";
  let r = null;
  try { r = JSON.parse(localStorage.getItem(key) || "null"); } catch {}

  const escapeHtml = (value) => String(value ?? "").replace(/[&<>"']/g, (char) => ({
    "&": "&amp;", "<": "&lt;", ">": "&gt;", """: "&quot;", "'": "&#39;"
  }[char]));

  const optionText = (item, ids) => {
    const match = (item.options || []).find((option) => ids.includes(option.option_id));
    return match ? match.text : "";
  };

  const paint = () => {
    if (!r) return;
    const p = r.percent || 0;
    document.querySelector(".result-hero .eyebrow").textContent = "Completed · " + r.assessment.title;
    document.querySelector(".result-hero p").textContent = `You scored ${r.score} of ${r.maximum_score}. Review the questions below to strengthen your next attempt.`;
    document.querySelector(".score-ring strong").textContent = p + "%";
    document.querySelector(".score-ring span").textContent = `${r.score} / ${r.maximum_score}`;
    document.querySelector(".score-ring").style.background = `conic-gradient(var(--forest) 0 ${p}%,#dfe9df ${p}% 100%)`;

    const host = document.querySelector(".review");
    const bad = (r.breakdown || []).filter((item) => !item.is_correct);
    host.querySelectorAll("article").forEach((item) => item.remove());

    bad.forEach((item, n) => {
      const selected = optionText(item, item.selected_option_ids || []);
      const correct = optionText(item, item.correct_option_ids || []);
      const selectedLabel = selected || (item.selected_option_ids || []).join(", ") || "Not answered";
      const correctLabel = correct || (item.correct_option_ids || []).join(", ") || "Not available";
      const prompt = item.prompt || item.question_id;
      host.insertAdjacentHTML("beforeend", `
        <article>
          <span class="q-number">Q${String(n + 1).padStart(2, "0")}</span>
          <div>
            <strong>${escapeHtml(prompt)}</strong>
            <p><b>Your answer:</b> ${escapeHtml(selectedLabel)}</p>
            <p class="correct"><b>Correct:</b> ${escapeHtml(correctLabel)}</p>
          </div>
          <span class="status">Review</span>
        </article>`);
    });
  };

  (async () => {
    if (!r) {
      const id = new URLSearchParams(location.search).get("attempt_id");
      if (id) r = await api.result(id);
      if (r) localStorage.setItem(key, JSON.stringify(r));
    }
    paint();
  })();
})();