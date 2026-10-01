(() => {
  const DEMO = {
    assessment: {
      assessment_id: "demo-dravyaguna-3",
      title: "Dravyaguna · Chapter 3 Assessment",
      curriculum_refs: ["subject:dravyaguna"],
      questions: [
        { question_id: "q1", prompt: "Which principle is most useful for organising related dravyas during study?", points: 1, options: [
          { option_id: "a", text: "Memorising each dravya as an isolated fact" },
          { option_id: "b", text: "Connecting source, properties, action and use" },
          { option_id: "c", text: "Studying only the common names" },
          { option_id: "d", text: "Grouping topics only by page number" }
        ]},
        { question_id: "q2", prompt: "Which relationship best supports therapeutic application?", points: 1, options: [
          { option_id: "a", text: "Properties → action → use" },
          { option_id: "b", text: "Page → chapter → book" },
          { option_id: "c", text: "Name → spelling → page" },
          { option_id: "d", text: "Source → index → appendix" }
        ]}
      ]
    }
  };

  const key = "aaptakosha.assessment.session";
  function fallbackLearnerId() {
    return "demo-learner";
  }

  function requestLearnerPayload() {
    const session = window.AaptaKoshaSession;
    return session && session.authenticated ? {} : { learner_id: fallbackLearnerId() };
  }

  async function request(path, options) {
    if (!window.AaptaKoshaApi) throw new Error("API client unavailable");
    try {
      return await window.AaptaKoshaApi.request(path, options);
    } catch (error) {
      if (window.AAPTAKOSHA_API_BASE || (window.AaptaKoshaSession && window.AaptaKoshaSession.authenticated)) throw error;
      return null;
    }
  }

  function save(value) { localStorage.setItem(key, JSON.stringify(value)); }
  function load() {
    try { return JSON.parse(localStorage.getItem(key) || "null"); }
    catch (_) { return null; }
  }

  async function start(id) {
    await window.AaptaKoshaSessionReady;
    const live = await request("/assessments/" + encodeURIComponent(id) + "/attempts", {
      method: "POST",
      body: JSON.stringify(requestLearnerPayload())
    });
    if (live?.data) {
      save(live.data);
      return live.data;
    }

    if (id === "charaka.sutra.01.ncism-revision") throw new Error("Chapter 1 NCISM assessment is temporarily unavailable. Please try again.");
    const assessment = DEMO.assessment;
    const attempt = {
      attempt_id: "demo-" + Date.now(),
      assessment_id: assessment.assessment_id,
      learner_id: (window.AaptaKoshaSession && window.AaptaKoshaSession.authenticated)
        ? (window.AaptaKoshaAuth && window.AaptaKoshaAuth.subjectId) || null
        : fallbackLearnerId(),
      status: "in_progress",
      answers: []
    };
    const session = { attempt, assessment };
    save(session);
    return session;
  }

  async function saveAnswers(session, answers) {
    const live = await request("/attempts/" + encodeURIComponent(session.attempt.attempt_id) + "/answers", {
      method: "PUT",
      body: JSON.stringify({ ...requestLearnerPayload(), answers })
    });
    const next = live?.data
      ? { ...session, attempt: live.data }
      : { ...session, attempt: { ...session.attempt, answers } };
    save(next);
    return next;
  }

  async function submit(session) {
    const live = await request("/attempts/" + encodeURIComponent(session.attempt.attempt_id) + "/submit", {
      method: "POST",
      body: JSON.stringify(requestLearnerPayload())
    });
    if (live?.data) {
      localStorage.setItem(key + ".result", JSON.stringify(live.data));
      localStorage.removeItem(key);
      return live.data;
    }

    const map = Object.fromEntries(session.attempt.answers || []);
    const assessment = session.assessment;
    const breakdown = assessment.questions.map((question) => {
      const selected = map[question.question_id] || [];
      const correct = question.question_id === "q1" ? ["b"] : ["a"];
      const isCorrect = selected.length === correct.length && selected.every((value) => correct.includes(value));
      return {
        question_id: question.question_id,
        selected_option_ids: selected,
        correct_option_ids: correct,
        is_correct: isCorrect,
        points: isCorrect ? question.points : 0,
        maximum_points: question.points
      };
    });
    const score = breakdown.reduce((sum, item) => sum + item.points, 0);
    const maximum = assessment.questions.reduce((sum, item) => sum + item.points, 0);
    const result = {
      attempt: { ...session.attempt, status: "submitted" },
      assessment: { assessment_id: assessment.assessment_id, title: assessment.title },
      score,
      maximum_score: maximum,
      percent: Math.round(score * 100 / maximum),
      breakdown,
      analytics: {
        attempt_count: 1,
        submitted_attempt_count: 1,
        best_score: score,
        best_percent: Math.round(score * 100 / maximum),
        latest_score: score
      }
    };
    localStorage.setItem(key + ".result", JSON.stringify(result));
    localStorage.removeItem(key);
    return result;
  }

  async function result(id) {
    await window.AaptaKoshaSessionReady;
    const authenticated = window.AaptaKoshaSession && window.AaptaKoshaSession.authenticated;
    const suffix = authenticated ? "" : "?learner_id=" + encodeURIComponent(fallbackLearnerId());
    const live = await request("/attempts/" + encodeURIComponent(id) + suffix);
    return live?.data || null;
  }

  window.AaptaKoshaAssessment = { start, saveAnswers, submit, result, load, DEMO };
})();
