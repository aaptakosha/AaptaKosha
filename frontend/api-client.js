/* Shared browser API boundary for AaptaKosha. */
(function () {
  const base = (window.AAPTAKOSHA_API_BASE || "/api").replace(/\/$/, "");

  function getAuthProvider() {
    return window.AaptaKoshaAuth || null;
  }

  async function authHeaders() {
    const provider = getAuthProvider();
    if (!provider || typeof provider.getToken !== "function") return {};
    const token = await provider.getToken();
    return token ? { Authorization: "Bearer " + token } : {};
  }

  async function request(path, options) {
    const config = options || {};
    const headers = Object.assign(
      { Accept: "application/json" },
      config.body !== undefined ? { "Content-Type": "application/json" } : {},
      await authHeaders(),
      config.headers || {}
    );

    const response = await fetch(base + path, Object.assign({}, config, { headers }));
    let body = null;
    try { body = await response.json(); } catch (_) {}

    if (!response.ok) {
      const error = body && body.error;
      const failure = new Error((error && error.message) || "AaptaKosha request failed");
      failure.code = error && error.code;
      failure.status = response.status;
      throw failure;
    }
    return body;
  }

  window.AaptaKoshaApi = {
    base,
    request,
    getAuthHeaders: authHeaders
  };
})();
