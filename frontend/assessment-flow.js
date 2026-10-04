(() => {
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

    throw new Error("The assessment service is unavailable. Please try again after the assessment API is restored.");
  }

  async function saveAnswers(session, answers) {
    const live = await request("/attempts/" + encodeURIComponent(session.attempt.attempt_id) + "/answers", {
      method: "PUT",
      body: JSON.stringify({ ...requestLearnerPayload(), answers })
    });
    if (!live?.data) throw new Error("Unable to save this answer because the assessment service is unavailable.");
    const next = { ...session, attempt: live.data };
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

    throw new Error("Unable to submit this assessment because the assessment service is unavailable.");

  async function result(id) {
    await window.AaptaKoshaSessionReady;
    const authenticated = window.AaptaKoshaSession && window.AaptaKoshaSession.authenticated;
    const suffix = authenticated ? "" : "?learner_id=" + encodeURIComponent(fallbackLearnerId());
    const live = await request("/attempts/" + encodeURIComponent(id) + suffix);
    return live?.data || null;
  }

  window.AaptaKoshaAssessment = { start, saveAnswers, submit, result, load };
})();
