// The page: top bar, App Library, phone, changes. Starts by asking the server what it has.

import { render } from "preact";
import { useEffect, useRef } from "preact/hooks";
import * as actions from "./actions.js";
import { ContextMenu, Dialogs, Toasts } from "./dialogs.js";
import { html } from "./html.js";
import { LANGUAGES, initialLanguage, language, setLanguage, t } from "./i18n.js";
import { ChangesPanel, LibraryPanel } from "./panels.js";
import { Phone } from "./phone.js";
import { getState, setState, useStore } from "./store.js";

const logo = html`<img class="logo" src="/static/favicon.svg" alt="" width="28" height="28" draggable="false" />`;

function DeviceStatus() {
  const state = getState();
  const server = state.server || {};
  const device = server.device;
  const running = state.job?.state === "running";
  const error = server.error && !server.demo && !running;
  const name = device?.name || (server.demo ? t("device.demo_name") : "iPhone");
  const link = server.demo ? t("device.pretend") : server.connection?.kind === "wifi" ? "Wi-Fi" : "USB";
  const tone = running ? "busy" : error ? "error" : server.read ? "ok" : "idle";
  const details = [device?.model, device?.ios_version && `iOS ${device.ios_version}`].filter(Boolean).join(", ");
  return html`<div class=${`device tone-${tone}`} title=${details || undefined}>
    <span class="status-dot" aria-hidden="true"></span>
    <span class="device-name">${name}</span>
    <span class="device-link">${link}</span>
  </div>`;
}

function LayoutFileButtons() {
  const input = useRef(null);
  const state = getState();
  return html`<div class="btn-group">
    <input
      ref=${input}
      type="file"
      accept=".toml,text/plain,application/toml"
      hidden
      onChange=${(e) => {
        const file = e.currentTarget.files?.[0];
        e.currentTarget.value = "";
        if (file) actions.importLayout(file);
      }}
    />
    <button class="btn btn-ghost" disabled=${!state.draft} title=${t("top.import_title")} onClick=${() => input.current.click()}>
      <svg viewBox="0 0 20 20"><path d="M10 13V3M6 7l4-4 4 4M4 13v3h12v-3" /></svg><span>${t("top.import")}</span>
    </button>
    <button class="btn btn-ghost" disabled=${!state.draft} title=${t("top.export_title")} onClick=${actions.exportLayout}>
      <svg viewBox="0 0 20 20"><path d="M10 3v10M6 9l4 4 4-4M4 13v3h12v-3" /></svg><span>${t("top.export")}</span>
    </button>
  </div>`;
}

// The editor opens in the system language; a choice made here is remembered.
function LanguagePicker() {
  return html`<label class="lang-picker" title=${t("top.language")}>
    <svg viewBox="0 0 20 20" aria-hidden="true"><circle cx="10" cy="10" r="7" /><path d="M3 10h14M10 3c-2.2 2-2.2 12 0 14M10 3c2.2 2 2.2 12 0 14" /></svg>
    <select
      aria-label=${t("top.language")}
      value=${language()}
      onChange=${async (e) => {
        const code = await setLanguage(e.currentTarget.value, { remember: true });
        setState({ language: code });
      }}
    >
      ${LANGUAGES.map(({ code, name }) => html`<option value=${code} lang=${code}>${name}</option>`)}
    </select>
  </label>`;
}

function TopBar() {
  const state = getState();
  const running = state.job?.state === "running";
  const changes = state.check.changes?.length || 0;
  return html`<header class="topbar">
    <div class="brand">
      ${logo}<span class="brand-name">IconShuffle</span>
      ${state.server?.demo && !state.server?.showcase ? html`<span class="brand-note">${t("top.demo_mode")}</span>` : null}
    </div>
    <div class="toolbar">
      <button class="btn btn-ghost narrow-only" onClick=${() => setState({ drawer: state.drawer === "library" ? null : "library" })}>
        <svg viewBox="0 0 20 20"><rect x="3" y="3" width="6" height="6" rx="1.6" /><rect x="11" y="3" width="6" height="6" rx="1.6" /><rect x="3" y="11" width="6" height="6" rx="1.6" /><rect x="11" y="11" width="6" height="6" rx="1.6" /></svg>
        <span>${t("top.library")}</span>
      </button>
      <${DeviceStatus} />
      <button class="btn btn-ghost" disabled=${running} title=${t("top.read_title")} onClick=${() => actions.readFromPhone()}>
        <svg viewBox="0 0 20 20" class=${running && state.job.kind === "read" ? "spin" : ""}><path d="M16 10a6 6 0 1 1-1.8-4.3M16 3.5v3.7h-3.7" /></svg>
        <span>${t("top.read")}</span>
      </button>
      <${LayoutFileButtons} />
      <button class="btn btn-ghost" disabled=${!state.draft || running} title=${t("top.sort_title")} onClick=${actions.sortAZ}>
        <svg viewBox="0 0 20 20"><path d="M4 5h12M4 10h9M4 15h6" /></svg>
        <span>${t("top.sort")}</span>
      </button>
      <button class="btn btn-ghost backups-btn" title=${t("top.backups_title")} onClick=${actions.openBackups}>
        <svg viewBox="0 0 20 20"><ellipse cx="10" cy="5" rx="6" ry="2.5" /><path d="M4 5v5c0 1.4 2.7 2.5 6 2.5s6-1.1 6-2.5V5M4 10v5c0 1.4 2.7 2.5 6 2.5s6-1.1 6-2.5v-5" /></svg>
        <span>${t("top.backups")}</span>
      </button>
      <${LanguagePicker} />
      <button class="btn btn-ghost narrow-only" onClick=${() => setState({ drawer: state.drawer === "changes" ? null : "changes" })}>
        <svg viewBox="0 0 20 20"><path d="M4 5h12M4 10h12M4 15h8" /></svg>
        <span>${changes ? t("top.changes_count", { count: changes }) : t("top.changes")}</span>
      </button>
    </div>
  </header>`;
}

function isTyping(event) {
  const target = event.target;
  return target instanceof HTMLElement && (target.isContentEditable || ["INPUT", "TEXTAREA", "SELECT"].includes(target.tagName));
}

function App() {
  const state = useStore();
  useEffect(() => {
    actions.boot();
    const key = (event) => {
      const s = getState();
      if (isTyping(event) || s.drag) return;
      const mod = event.ctrlKey || event.metaKey;
      if (mod && event.key.toLowerCase() === "z" && !event.shiftKey) {
        event.preventDefault();
        actions.undo();
      } else if (mod && (event.key.toLowerCase() === "y" || (event.key.toLowerCase() === "z" && event.shiftKey))) {
        event.preventDefault();
        actions.redo();
      } else if (s.dialog || s.menu) {
        return;
      } else if (event.key === "Escape") {
        if (s.openFolder) actions.closeFolder();
        else if (s.drawer) setState({ drawer: null });
      } else if (event.key === "ArrowLeft" && !s.openFolder) {
        actions.goToPage(s.page - 1);
      } else if (event.key === "ArrowRight" && !s.openFolder) {
        actions.goToPage(s.page + 1);
      }
    };
    window.addEventListener("keydown", key);
    const leave = (event) => {
      const s = getState();
      if (s.job?.state === "running" && s.job.kind !== "read") {
        event.preventDefault();
        event.returnValue = "";
      }
    };
    window.addEventListener("beforeunload", leave);
    return () => {
      window.removeEventListener("keydown", key);
      window.removeEventListener("beforeunload", leave);
    };
  }, []);
  return html`<div class=${`app${state.drag ? " is-dragging" : ""}`}>
    <${TopBar} />
    <main class="workspace">
      <${LibraryPanel} />
      <section class="center" aria-label=${t("phone.home_screen")}>
        <${Phone} />
      </section>
      <${ChangesPanel} />
      ${state.drawer ? html`<div class="drawer-backdrop" onClick=${() => setState({ drawer: null })}></div>` : null}
    </main>
    <${Dialogs} />
    <${ContextMenu} />
    <${Toasts} />
  </div>`;
}

await setLanguage(initialLanguage());
render(html`<${App} />`, document.getElementById("app"));
