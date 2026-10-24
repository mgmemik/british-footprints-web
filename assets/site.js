/* British Footprints: Istanbul - language switch (EN/TR) and theme toggle.
   English is baked into the HTML by tools/build.py; other languages are loaded from
   assets/i18n/<lang>.json and swapped into every [data-i18n] / [data-i18n-attr] element. */
(function () {
  "use strict";
  var SUPPORTED = ["en", "tr"];
  var LOCALES = { en: "en_GB", tr: "tr_TR" };
  var script = document.currentScript;
  var root = (script && script.getAttribute("data-root")) || "";
  var page = (script && script.getAttribute("data-page")) || "home";
  var cache = {};

  function store(key, value) {
    try { localStorage.setItem(key, value); } catch (e) {}
  }
  function read(key) {
    try { return localStorage.getItem(key); } catch (e) { return null; }
  }
  function textOf(html) {
    var d = document.createElement("div");
    d.innerHTML = html;
    return d.textContent;
  }

  function pickLang() {
    var q = new URLSearchParams(location.search).get("lang");
    if (SUPPORTED.indexOf(q) >= 0) return q;
    var saved = read("bf_lang");
    if (SUPPORTED.indexOf(saved) >= 0) return saved;
    return (navigator.language || "").toLowerCase().indexOf("tr") === 0 ? "tr" : "en";
  }

  function load(lang) {
    if (cache[lang]) return Promise.resolve(cache[lang]);
    return fetch(root + "assets/i18n/" + lang + ".json")
      .then(function (r) { if (!r.ok) throw new Error(r.status); return r.json(); })
      .then(function (t) { cache[lang] = t; return t; });
  }

  function apply(t) {
    document.querySelectorAll("[data-i18n]").forEach(function (el) {
      var v = t[el.getAttribute("data-i18n")];
      if (v == null) return;
      if (el.tagName === "TITLE") document.title = textOf(v);
      else el.innerHTML = v;
    });
    document.querySelectorAll("[data-i18n-attr]").forEach(function (el) {
      el.getAttribute("data-i18n-attr").split(";").forEach(function (pair) {
        var i = pair.indexOf(":");
        var v = t[pair.slice(i + 1)];
        if (v != null) el.setAttribute(pair.slice(0, i), textOf(v));
      });
    });
  }

  function reflect(lang) {
    document.documentElement.lang = lang;
    document.querySelectorAll(".lang-btn").forEach(function (b) {
      b.setAttribute("aria-pressed", String(b.getAttribute("data-lang") === lang));
    });
    var url = new URL(location.href);
    if (lang === "en") url.searchParams.delete("lang");
    else url.searchParams.set("lang", lang);
    history.replaceState(null, "", url);
    var canon = document.querySelector("link[rel=canonical]");
    if (canon) {
      var base = canon.getAttribute("data-canonical-base");
      canon.href = lang === "en" ? base : base + "?lang=" + lang;
    }
    var loc = document.querySelector("meta[property='og:locale']");
    if (loc) loc.setAttribute("content", LOCALES[lang]);
  }

  function setLang(lang, remember) {
    if (SUPPORTED.indexOf(lang) < 0) lang = "en";
    if (remember) store("bf_lang", lang);
    return load(lang).then(function (t) { apply(t); reflect(lang); })
      .catch(function () { reflect("en"); });
  }

  function initTheme() {
    var btn = document.getElementById("theme-btn");
    if (!btn) return;
    btn.addEventListener("click", function () {
      var next = document.documentElement.getAttribute("data-theme") === "light" ? "dark" : "light";
      document.documentElement.setAttribute("data-theme", next);
      store("bf_theme", next);
    });
    // Follow system changes while the visitor has not chosen a theme here.
    if (window.matchMedia) {
      var mq = matchMedia("(prefers-color-scheme: light)");
      var onChange = function () {
        var saved = read("bf_theme");
        if (saved !== "light" && saved !== "dark") {
          document.documentElement.setAttribute("data-theme", mq.matches ? "light" : "dark");
        }
      };
      if (mq.addEventListener) mq.addEventListener("change", onChange);
    }
  }

  document.querySelectorAll(".nav-link[data-nav='" + page + "']").forEach(function (a) {
    a.setAttribute("aria-current", "page");
  });
  document.querySelectorAll(".lang-btn").forEach(function (b) {
    b.addEventListener("click", function () { setLang(b.getAttribute("data-lang"), true); });
  });
  initTheme();
  var initial = pickLang();
  if (initial !== "en") setLang(initial, false);
  else reflect("en");
})();
