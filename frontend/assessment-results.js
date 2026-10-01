(() => {
  const api = window.AaptaKoshaAssessment;
  const key = "aaptakosha.assessment.session.result";
  let r = null;
  try { r = JSON.parse(localStorage.getItem(key) || "null"); } catch {}

  const escapeHtml = (value) => String(value ?? "").replace(/[&<>"']/g, (char) => ({
    "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;"
  }[char]));

  const optionText = (item, ids) => {
    const match = (item.options || []).find((option) => ids.includes(option.option_id));
    return match ? match.text : "";
  };

  const bindActions = () => { document.querySelector("#reviewAnswers")?.addEventListener("click",()=>document.querySelector(".review")?.scrollIntoView({behavior:"smooth"})); document.querySelector("#continueLearning")?.addEventListener("click",()=>location.href="./samhita-study.html?chapter=charaka.sutra.01"); };\n\n  const paint = () => {
    if (!r) return;\n    bindActions();
    const p = r.percent || 0;
    document.querySelector(".result-hero .eyebrow").textContent = "Completed · " + r.assessment.title;
    document.querySelector(".result-hero p").textContent = `You scored ${r.score} of ${r.maximum_score}. Review the questions below to strengthen your next attempt.`;
    document.querySelector(".score-ring strong").textContent = p + "%";
    document.querySelector(".score-ring span").textContent = `${r.score} / ${r.maximum_score}`;
    document.querySelector(".score-ring").style.background = `conic-gradient(var(--forest) 0 ${p}%,#dfe9df ${p}% 100%)`;

    const host = document.querySelector(".review");
    const bad = (r.breakdown || []).filter((item) => !item.is_correct);
    const weakHost = document.querySelector("#weakShlokaList");
    if (weakHost) {
      const refs = [];
      bad.forEach((item) => (item.content_refs || []).forEach((ref) => {
        const match = ref.match(/^(charaka\\.sutra\\.01)\\.(\\d{3})$/);
        if (match && !refs.some((x) => x.verse === Number(match[2]))) refs.push({ verse: Number(match[2]), ref });
      }));
      weakHost.innerHTML = refs.length
        ? refs.map((item) => `<a class="weak-card" href="./samhita-study.html?chapter=charaka.sutra.01&verse=${item.verse}"><span class="weak-number">श्लोक ${item.verse}</span><span><strong>पुनः पढ़ें और revise करें</strong><small>Canonical Chapter 1 content</small></span><span>→</span></a>`).join("")
        : '<div class="weak-empty">इस attempt में कोई गलत NCISM shloka नहीं मिला। Chapter 1 revision फिर भी जारी रख सकते हैं।</div>';
    }
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
    try {
      await window.AaptaKoshaSessionReady;
      const id = new URLSearchParams(location.search).get("attempt_id");
      const authenticated = window.AaptaKoshaSession && window.AaptaKoshaSession.authenticated;
      if (id && (authenticated || !r)) {
        const live = await api.result(id);
        if (live) r = live;
      }
      if (r) localStorage.setItem(key, JSON.stringify(r));
      paint();
    } catch (error) {
      const state = document.querySelector("[data-ui-state]");
      if (state) window.AaptaKoshaUi?.status(state, error.message || "Unable to load assessment results.", "error");
    }
  })();
})();