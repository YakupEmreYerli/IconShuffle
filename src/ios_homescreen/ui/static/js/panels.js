// The two side panels: the App Library on the left, the changes and Apply on the right.

import { useRef } from "preact/hooks";
import * as actions from "./actions.js";
import { startPress } from "./drag.js";
import { html } from "./html.js";
import { ICON } from "./layout.js";
import { joinList, t } from "./i18n.js";
import { describeChange, errorText, eventText, issueText, refusalShort, relativeTime } from "./messages.js";
import { allItems, fromView, shownApps } from "./ops.js";
import { getState, setState, useStore } from "./store.js";
import { Icon, ItemIcon } from "./visuals.js";

const HOME_TYPES = new Set(["User", "System", ""]);

function libraryApps(state) {
  if (!state.draft) return [];
  const shown = shownApps(state.draft);
  const before = state.baseline ? shownApps(fromView(state.baseline)) : new Set();
  return state.apps
    .filter((app) => HOME_TYPES.has(app.type) && !shown.has(app.id))
    .map((app) => ({ ...app, leaving: before.has(app.id) }));
}

function LibraryRow({ app }) {
  const icon = useRef(null);
  const item = { type: "app", id: app.id, name: app.name, cells: 1, offloaded: Boolean(app.offloaded) };
  const page = getState().page + 1;
  return html`<li
    class="lib-row"
    onPointerDown=${(event) => {
      if (event.target.closest("button")) return;
      startPress(event, { item, from: null, fromLibrary: true, el: icon.current, w: ICON, h: ICON });
    }}
  >
    <div class="lib-icon" ref=${icon}><${Icon} id=${app.id} name=${app.name} /></div>
    <div class="lib-text">
      <span class="lib-name">${app.name}</span>
      ${app.leaving ? html`<span class="lib-note">${t("library.leaving")}</span>` : null}
    </div>
    <button class="lib-add" title=${t("library.add_title", { page })} aria-label=${t("library.add_label", { name: app.name, page })} onClick=${() => actions.addFromLibrary(app)}>
      <svg viewBox="0 0 16 16"><path d="M8 3v10M3 8h10" /></svg>
    </button>
    <span class="grip" aria-hidden="true">
      <svg viewBox="0 0 10 16"><circle cx="3" cy="3" r="1.3" /><circle cx="7" cy="3" r="1.3" /><circle cx="3" cy="8" r="1.3" /><circle cx="7" cy="8" r="1.3" /><circle cx="3" cy="13" r="1.3" /><circle cx="7" cy="13" r="1.3" /></svg>
    </span>
  </li>`;
}

export function LibraryPanel() {
  const state = useStore();
  const apps = libraryApps(state);
  const query = state.search.trim().toLocaleLowerCase();
  const shown = query
    ? apps.filter((app) => app.name.toLocaleLowerCase().includes(query) || app.id.toLowerCase().includes(query))
    : apps;
  const drag = state.drag;
  const target = drag?.target;
  const dropping = drag && !drag.fromLibrary;
  const over = target?.zone === "library";
  return html`<aside
    class=${`panel library${state.drawer === "library" ? " is-open" : ""}${dropping ? " is-drop" : ""}${over ? " is-over" : ""}${over && target.invalid ? " is-refused" : ""}`}
    data-zone="library"
    aria-label=${t("library.title")}
  >
    <header class="panel-head">
      <h2>${t("library.title")}</h2>
    </header>
    <p class="panel-hint">
      ${state.draft
        ? t("library.hint", { count: apps.length })
        : t("library.hint_empty")}
    </p>
    <label class="search">
      <svg viewBox="0 0 20 20" aria-hidden="true"><circle cx="9" cy="9" r="5.5" /><path d="m13.2 13.2 3.8 3.8" /></svg>
      <input
        type="search"
        placeholder=${t("library.search")}
        value=${state.search}
        onInput=${(e) => setState({ search: e.currentTarget.value })}
        aria-label=${t("library.search_label")}
      />
    </label>
    <ul class="lib-list">
      ${shown.map((app) => html`<${LibraryRow} key=${app.id} app=${app} />`)}
    </ul>
    ${state.draft && !shown.length
      ? html`<div class="empty">${query ? t("library.no_match", { query: state.search }) : t("library.all_shown")}</div>`
      : null}
    <div class="drop-hint" aria-hidden="true">
      <svg viewBox="0 0 24 24"><path d="M4 7h16M6 7l1 12h10l1-12M9 7V4h6v3" /></svg>
      <span>${over && target.invalid ? refusalShort(target.invalid) : t("library.drop")}</span>
    </div>
  </aside>`;
}

function StatusLine() {
  const state = getState();
  const server = state.server || {};
  const job = state.job?.state === "running" ? state.job : null;
  const wifi = server.connection?.kind === "wifi";
  let tone = "ok";
  let text = server.read?.at
    ? t(wifi ? "status.wifi_read" : "status.usb_read", { time: relativeTime(server.read.at) })
    : t(wifi ? "status.wifi" : "status.usb");
  if (server.demo) {
    tone = "demo";
    text = t("status.demo");
  }
  if (job) {
    tone = "busy";
    text = eventText(job.events[job.events.length - 1], actions.nameOf) || t("status.connecting");
  } else if (server.error && !server.demo) {
    tone = "error";
    text = t("status.error", { reason: errorText(server.error).title });
  } else if (!server.read && !server.demo) {
    tone = "idle";
    text = t("status.not_read");
  }
  return html`<p class=${`status-line tone-${tone}`} role="status">
    <span class="status-dot" aria-hidden="true"></span>${text}
  </p>`;
}

function ChangeIcon({ change }) {
  const state = getState();
  if (change.kind === "pages") {
    return html`<div class="change-glyph"><svg viewBox="0 0 20 20"><rect x="4" y="3" width="12" height="14" rx="2" /></svg></div>`;
  }
  const item =
    (state.draft && allItems(state.draft).find((x) => x.id === change.id)) ||
    (state.baseline && allItems(fromView(state.baseline)).find((x) => x.id === change.id)) || {
      type: change.type,
      id: change.id,
      name: change.name,
      pages: [[]],
    };
  return html`<div class="change-icon"><${ItemIcon} item=${item} /></div>`;
}

function Change({ change }) {
  const state = getState();
  const text = describeChange(change, state.draft);
  const clickable = change.id && !["to_library", "removed", "folder_deleted"].includes(change.kind);
  return html`<li class=${`change tone-${text.tone}`}>
    <button class="change-btn" disabled=${!clickable} onClick=${() => actions.reveal(change.id)} title=${clickable ? t("changes.show") : undefined}>
      <${ChangeIcon} change=${change} />
      <span class="change-text">
        <span class="change-name">${text.title}</span>
        <span class="change-detail">${text.detail}</span>
      </span>
    </button>
  </li>`;
}

function Issues() {
  const state = getState();
  const issues = state.check.issues || [];
  if (!issues.length) return null;
  return html`<div class="issues" role="alert">
    <p class="issues-head">
      ${t("changes.issues", { count: issues.length })}
    </p>
    <ul>
      ${issues.map((issue) => {
        const page = issue.location?.section === "page" ? issue.location.page - 1 : null;
        return html`<li>
          <button class="issue" disabled=${page == null} onClick=${() => page != null && actions.goToPage(page)}>
            ${issueText(issue, actions.nameOf)}
          </button>
        </li>`;
      })}
    </ul>
  </div>`;
}

function summaryText(changes) {
  const count = (kinds) => changes.filter((c) => kinds.includes(c.kind)).length;
  const parts = [];
  const moved = count(["moved", "reordered"]);
  if (moved) parts.push(t("summary.moved", { count: moved }));
  const added = count(["added", "folder_created"]);
  if (added) parts.push(t("summary.added", { count: added }));
  const library = count(["to_library"]);
  if (library) parts.push(t("summary.to_library", { count: library }));
  const removed = count(["removed"]);
  if (removed) parts.push(t("summary.removed", { count: removed }));
  if (!parts.length) return "";
  const text = joinList(parts);
  return t("summary.sentence", { text: text[0].toLocaleUpperCase() + text.slice(1) });
}

export function ChangesPanel() {
  const state = useStore();
  const check = state.check;
  const changes = check.changes || [];
  const running = state.job?.state === "running";
  const ready = state.draft && check.ok && check.dirty && !check.pending && !running;
  let label = t("action.apply");
  if (!state.draft) label = t("action.apply");
  else if (running) label = state.job.kind === "read" ? t("changes.reading") : t("job.applying");
  else if (!check.ok) label = t("changes.fix", { count: check.issues.length });
  else if (!check.dirty) label = t("changes.none_to_apply");
  return html`<aside class=${`panel changes${state.drawer === "changes" ? " is-open" : ""}`} aria-label=${t("top.changes")}>
    <header class="panel-head">
      <h2>${t("top.changes")}</h2>
      <div class="head-actions">
        <button class="icon-btn" title=${t("changes.undo_title")} aria-label=${t("action.undo")} disabled=${!state.past.length} onClick=${actions.undo}>
          <svg viewBox="0 0 20 20"><path d="M7.5 5 3.5 9l4 4" /><path d="M4 9h8a4.5 4.5 0 0 1 0 9h-2" /></svg>
        </button>
        <button class="icon-btn" title=${t("changes.redo_title")} aria-label=${t("changes.redo")} disabled=${!state.future.length} onClick=${actions.redo}>
          <svg viewBox="0 0 20 20"><path d="m12.5 5 4 4-4 4" /><path d="M16 9H8a4.5 4.5 0 0 0 0 9h2" /></svg>
        </button>
      </div>
    </header>
    <${StatusLine} />
    <${Issues} />
    ${changes.length
      ? html`<ul class="change-list">${changes.map((change, i) => html`<${Change} key=${`${change.kind}-${change.id || i}`} change=${change} />`)}</ul>`
      : html`<div class="changes-empty">
          <p><strong>${t("changes.empty_title")}</strong></p>
          <p>${t("changes.empty_text")}</p>
        </div>`}
    <footer class="apply-bar">
      ${changes.length ? html`<div class="summary">${summaryText(changes)}</div>` : null}
      <button class="btn btn-apply" disabled=${!ready} onClick=${actions.openApply}>
        ${running ? html`<span class="spinner small"></span>` : null}${label}
      </button>
      <div class="apply-note">
        ${ready ? t("changes.apply_note") : ""}
        ${state.past.length && changes.length
          ? html`<button class="link-btn" onClick=${actions.discardChanges}>${t("changes.discard")}</button>`
          : null}
      </div>
    </footer>
  </aside>`;
}
