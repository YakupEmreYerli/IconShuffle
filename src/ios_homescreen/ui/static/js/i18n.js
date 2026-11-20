// The editor's text in the person's language. Each language is one JSON file under
// /static/i18n/; English is the source and fills any gap. t("key", { name }) picks the
// text and fills {name}; an entry with plural forms ({ one, other, ... }) is chosen by
// `count` through Intl.PluralRules.

export const LANGUAGES = [
  { code: "en", name: "English" },
  { code: "tr", name: "Türkçe" },
  { code: "de", name: "Deutsch" },
  { code: "es", name: "Español" },
  { code: "fr", name: "Français" },
  { code: "ja", name: "日本語" },
  { code: "pt-BR", name: "Português (Brasil)" },
  { code: "zh-Hans", name: "简体中文" },
];

const STORAGE_KEY = "iconshuffle.language";
const CODES = LANGUAGES.map((l) => l.code);

let current = "en";
let strings = {};
let english = {};
let plurals = new Intl.PluralRules("en");

// The best of LANGUAGES for a list like navigator.languages, or English.
export function matchLanguage(preferred) {
  for (const tag of preferred || []) {
    const lower = String(tag).toLowerCase();
    const exact = CODES.find((code) => code.toLowerCase() === lower);
    if (exact) return exact;
    const [base, ...rest] = lower.split("-");
    if (base === "zh") {
      // Traditional Chinese readers get English rather than the wrong script.
      if (rest.some((part) => ["hant", "tw", "hk", "mo"].includes(part))) continue;
      return "zh-Hans";
    }
    if (base === "pt") return "pt-BR";
    const loose = CODES.find((code) => code === base);
    if (loose) return loose;
  }
  return "en";
}

function saved() {
  try {
    const value = localStorage.getItem(STORAGE_KEY);
    return CODES.includes(value) ? value : null;
  } catch {
    return null;
  }
}

export function initialLanguage() {
  return saved() || matchLanguage(navigator.languages?.length ? navigator.languages : [navigator.language]);
}

async function fetchStrings(code) {
  const response = await fetch(`/static/i18n/${code}.json`, { credentials: "same-origin" });
  if (!response.ok) throw new Error(`HTTP ${response.status}`);
  return response.json();
}

// Load a language and make it current. English stays loaded as the fallback.
export async function setLanguage(code, { remember = false } = {}) {
  if (!CODES.includes(code)) code = "en";
  if (!Object.keys(english).length) english = await fetchStrings("en");
  try {
    strings = code === "en" ? english : await fetchStrings(code);
  } catch {
    code = "en";
    strings = english;
  }
  current = code;
  plurals = new Intl.PluralRules(code);
  document.documentElement.lang = code;
  if (remember) {
    try {
      localStorage.setItem(STORAGE_KEY, code);
    } catch {
      // private windows may refuse; the choice then lasts until the page closes
    }
  }
  return code;
}

export function language() {
  return current;
}

function fill(text, params) {
  return text.replace(/\{(\w+)\}/g, (whole, name) => (name in params ? String(params[name]) : whole));
}

function lookup(key) {
  return key in strings ? strings[key] : english[key];
}

export function t(key, params = {}) {
  let entry = lookup(key);
  if (entry == null) return key;
  if (typeof entry === "object" && !Array.isArray(entry)) {
    entry = entry[plurals.select(params.count ?? 0)] ?? entry.other;
  }
  return fill(String(entry), params);
}

// A list entry (the steps of an error), each item filled like t().
export function tList(key, params = {}) {
  const entry = lookup(key);
  return Array.isArray(entry) ? entry.map((text) => fill(text, params)) : null;
}

export function has(key) {
  return lookup(key) != null;
}

// "a, b and c" in the current language.
export function joinList(items) {
  try {
    return new Intl.ListFormat(current, { type: "conjunction" }).format(items);
  } catch {
    return items.join(", ");
  }
}
