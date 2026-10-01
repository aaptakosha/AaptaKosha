/* Provider-neutral learner session bootstrap.
   A production identity provider can expose AaptaKoshaAuth.getToken().
   The API remains the authority for learner identity and authorization. */
(function () {
  async function bootstrap() {
    const provider = window.AaptaKoshaAuth || null;
    let authenticated = false;

    if (provider && typeof provider.getToken === "function") {
      try {
        authenticated = Boolean(await provider.getToken());
      } catch (_) {
        authenticated = false;
      }
    }

    document.documentElement.dataset.authenticated = authenticated ? "true" : "false";
    window.AaptaKoshaSession = {
      authenticated,
      state: authenticated ? "authenticated" : "anonymous"
    };
    return window.AaptaKoshaSession;
  }

  window.AaptaKoshaSessionReady = bootstrap();
})();
