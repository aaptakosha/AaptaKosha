/* Provider-neutral learner session bootstrap.
   Production Clerk configuration is fetched from the same-origin API.
   Only the publishable key reaches the browser; the secret key stays server-side. */
(function () {
  async function loadClerk(publishableKey) {
    if (!publishableKey) return null;
    if (window.Clerk) return window.Clerk;

    const parts = publishableKey.split("_");
    if (parts.length < 3) throw new Error("invalid_clerk_publishable_key");
    const domain = atob(parts[2]).slice(0, -1);

    await new Promise((resolve, reject) => {
      const script = document.createElement("script");
      const timeout = setTimeout(() => reject(new Error("clerk_sdk_load_timeout")), 5000);
      script.src = `https://${domain}/npm/@clerk/clerk-js@6/dist/clerk.browser.js`;
      script.async = true;
      script.crossOrigin = "anonymous";
      script.onload = () => { clearTimeout(timeout); resolve(); };
      script.onerror = () => { clearTimeout(timeout); reject(new Error("clerk_sdk_load_failed")); };
      document.head.appendChild(script);
    });

    if (!window.Clerk) throw new Error("clerk_sdk_unavailable");
    if (!window.__aaptaClerkUI) {
      await new Promise((resolve, reject) => {
        const ui = document.createElement("script");
        const timeout = setTimeout(() => reject(new Error("clerk_ui_load_timeout")), 5000);
        ui.src = "https://" + domain + "/npm/@clerk/ui@1/dist/ui.browser.js";
        ui.async = true;
        ui.crossOrigin = "anonymous";
        ui.onload = () => { clearTimeout(timeout); window.__aaptaClerkUI = true; resolve(); };
        ui.onerror = () => { clearTimeout(timeout); reject(new Error("clerk_ui_load_failed")); };
        document.head.appendChild(ui);
      });
    }
    return window.Clerk;
  }

  async function bootstrap() {
    let authenticated = false;
    let clerk = null;

    try {
      const controller = new AbortController();
      const timeout = setTimeout(() => controller.abort(), 4000);
      let response;
      try {
        response = await fetch("/api/config", { headers: { Accept: "application/json" }, signal: controller.signal });
      } finally {
        clearTimeout(timeout);
      }
      if (!response.ok) throw new Error("auth_config_unavailable");
      const config = await response.json();
      const publishableKey = config.clerk_publishable_key || "";

      if (publishableKey) {
        const Clerk = await loadClerk(publishableKey);
        clerk = new Clerk(publishableKey);
        await clerk.load({
          ui: { ClerkUI: window.__internal_ClerkUICtor },
          signInForceRedirectUrl: window.location.href,
          signUpForceRedirectUrl: window.location.href
        });
        authenticated = Boolean(clerk.isSignedIn && clerk.session);
        window.AaptaKoshaAuth = {
          subjectId: clerk.user ? clerk.user.id : null,
          getToken: () => clerk.session ? clerk.session.getToken() : null,
          openSignIn: () => clerk.openSignIn({}),
          openUserProfile: () => clerk.openUserProfile({})
        };
      }
    } catch (_) {
      authenticated = false;
    }

    document.documentElement.dataset.authenticated = authenticated ? "true" : "false";
    window.AaptaKoshaSession = {
      authenticated,
      state: authenticated ? "authenticated" : "anonymous",
      clerk
    };
    return window.AaptaKoshaSession;
  }

  window.AaptaKoshaSessionReady = bootstrap();
})();
