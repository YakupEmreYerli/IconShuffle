// Modal dialogs (apply, progress, backups, confirmations), the context menu and toasts.

import { useEffect, useRef, useState } from "preact/hooks";
import * as actions from "./actions.js";
import { html } from "./html.js";
import { t } from "./i18n.js";
import { describeChange, errorText, eventText, formatDate, issueText, relativeTime } from "./messages.js";
import { REMOVABLE, STUCK, allItems, blockReason, locate, removeId } from "./ops.js";
import { renderCode } from "./phone.js";
import { getState, setState, useStore } from "./store.js";

function close() {
  setState({ dialog: null });
}

function Modal({ title, children, tone = "", wide = false, onClose = close, dismissable = true }) {
  const box = useRef(null);
  useEffect(() => {
    const focusable = box.current?.querySelector("[data-autofocus]") || box.current?.querySelector("button");
    focusable?.focus();
    const key = (event) => {
      if (event.key === "Escape" && dismissable) onClose();
    };
    window.addEventListener("keydown", key);
    return () => window.removeEventListener("keydown", key);
  }, [dismissable]);
  return html`<div class="modal-backdrop" onPointerDown=${(e) => dismissable && e.target === e.currentTarget && onClose()}>
    <div class=${`modal${wide ? " is-wide" : ""}${tone ? ` tone-${tone}` : ""}`} role="dialog" aria-modal="true" aria-label=${title} ref=${box}>
      ${children}
    </div>
  </div>`;
}

const STEPS = [1, 2, 3, 4, 5];

const check = html`<svg viewBox="0 0 20 20"><path d="m5 10.5 3.2 3L15 6.5" /></svg>`;

function ApplyDialog() {
  const state = getState();
  const changes = state.check.changes || [];
  const summary = state.check.summary || {};
  const device = state.server?.device?.name || "iPhone";
  const removed = changes.filter((c) => c.kind === "removed");
  const widgets = state.draft && allItems(state.draft).some((item) => item.type === "widget");
  const lines = changes.slice(0, 8).map((change) => describeChange(change, state.draft));
  return html`<${Modal} title=${t("apply.label")}>
    <h3 class="modal-title">${t("apply.title", { count: changes.length, device })}</h3>
    <ul class="apply-lines">
      ${lines.map(
        (line) =>
          html`<li class=${`tone-${line.tone}`}><strong>${line.title}</strong>${" "}<span>${line.detail}</span></li>`,
      )}
      ${changes.length > lines.length ? html`<li class="more">${t("apply.more", { count: changes.length - lines.length })}</li>` : null}
    </ul>
    ${summary.to_library?.length || summary.to_home_screen?.length
      ? html`<p class="apply-counts">
          ${summary.to_home_screen?.length ? `${t("apply.to_home", { count: summary.to_home_screen.length })} ` : ""}
          ${summary.to_library?.length ? t("apply.to_library", { count: summary.to_library.length }) : ""}
        </p>`
      : null}
    ${removed.length
      ? html`<div class="callout tone-danger">
          ${t("apply.removed_warning", { count: removed.length })}
        </div>`
      : null}
    ${widgets
      ? html`<div class="callout">
          ${t("apply.widgets_note")}
        </div>`
      : null}
    <div class="callout">
      ${t("apply.gaps_note")}
    </div>
    <ol class="safety">
      <li><span>1</span>${t("apply.safety_backup")}</li>
      <li><span>2</span>${t("apply.safety_write")}</li>
      <li><span>3</span>${t("apply.safety_check")}</li>
      <li><span>4</span>${t("apply.safety_rollback")}</li>
    </ol>
    <div class="modal-actions">
      <button class="btn" onClick=${close}>${t("action.cancel")}</button>
      <button class="btn btn-commit" data-autofocus onClick=${() => actions.startApply()}>${t("action.apply")}</button>
    </div>
  <//>`;
}

function JobDialog() {
  const state = getState();
  const job = state.job;
  const dialog = state.dialog;
  if (!job) return null;
  const running = job.state === "running";
  const events = job.events || [];
  const reached = Math.max(0, ...events.filter((e) => e.step && e.total === 5).map((e) => e.step));
  const status = job.result?.status;
  const error = errorText(job.error);
  const restore = dialog.jobKind === "restore";
  let outcome = null;
  if (!running && status === "applied") {
    outcome = html`<div class="outcome tone-success">
      <div class="outcome-icon">${check}</div>
      <div>
        <h3>${restore ? t("job.restored") : t("job.applied")}</h3>
        <p>${t("job.applied_text", { file: job.result.backup_name })}</p>
      </div>
    </div>`;
  } else if (!running && status === "rolled-back") {
    outcome = html`<div class="outcome tone-warning">
      <div class="outcome-icon">↺</div>
      <div>
        <h3>${t("job.rolled_back")}</h3>
        <p>${t("job.rolled_back_text")}</p>
      </div>
    </div>`;
  } else if (!running && status === "rollback-failed") {
    outcome = html`<div class="outcome tone-danger">
      <div class="outcome-icon">!</div>
      <div>
        <h3>${t("job.rollback_failed")}</h3>
        <p>${t("job.rollback_failed_text", { file: job.result.backup_name })}</p>
      </div>
    </div>`;
  } else if (!running && error) {
    outcome = html`<div class="outcome tone-danger">
      <div class="outcome-icon">!</div>
      <div>
        <h3>${error.title}</h3>
        ${error.code !== "layout_changed" ? html`<p>${t("job.nothing_written")}</p>` : null}
        ${error.steps?.length ? html`<ol class="screen-steps">${error.steps.map((s) => html`<li>${renderCode(s)}</li>`)}</ol>` : null}
        ${error.detail ? html`<details class="screen-detail"><summary>${t("error.details")}</summary><code>${error.detail}</code></details>` : null}
      </div>
    </div>`;
  }
  const reread = job.result?.reread_error;
  return html`<${Modal} title=${restore ? t("job.restore_label") : t("job.apply_label")} dismissable=${!running} wide>
    <h3 class="modal-title">${running ? (restore ? t("job.restoring") : t("job.applying")) : restore ? t("job.restore") : t("action.apply")}</h3>
    <ol class="stepper">
      ${STEPS.map((step) => {
        const failedCheck = step === 4 && (status === "rolled-back" || status === "rollback-failed");
        const done = !failedCheck && (reached > step || (reached === step && step === 5) || (!running && status === "applied"));
        const active = running && (reached === step || (reached === 0 && step === 1));
        return html`<li class=${`${done ? "is-done" : ""}${active ? " is-active" : ""}${failedCheck ? " is-failed" : ""}`}>
          <span class="step-mark">${done ? check : failedCheck ? "!" : active ? html`<span class="spinner small"></span>` : step}</span>
          <span>${t(`job.step${step}`)}</span>
        </li>`;
      })}
    </ol>
    <div class="event-log" aria-live="polite">
      ${events.slice(-6).map((e) => html`<div class=${`event level-${e.level}`}>${eventText(e, actions.nameOf)}</div>`)}
    </div>
    ${outcome}
    ${reread ? html`<div class="callout">${t("job.reread_failed", { reason: errorText(reread).title })}</div>` : null}
    <div class="modal-actions">
      ${!running && error?.code === "layout_changed"
        ? html`<button class="btn" onClick=${() => actions.readFromPhone()}>${t("top.read")}</button>
            <button class="btn btn-danger" onClick=${() => actions.startApply({ force: true })}>${t("job.apply_anyway")}</button>`
        : null}
      ${!running && status === "rollback-failed"
        ? html`<button class="btn" onClick=${actions.openBackups}>${t("job.open_backups")}</button>`
        : null}
      ${!running && status === "rolled-back"
        ? html`<button class="btn" onClick=${() => actions.startApply()}>${t("action.try_again")}</button>`
        : null}
      <button class="btn btn-primary" disabled=${running} onClick=${close}>${running ? t("job.working") : t("action.done")}</button>
    </div>
  <//>`;
}

function BackupsDialog() {
  const state = getState();
  const backups = state.dialog.backups;
  const [asking, setAsking] = useState(null);
  const running = state.job?.state === "running";
  const showcase = Boolean(state.server?.showcase);
  return html`<${Modal} title=${t("top.backups")} wide>
    <h3 class="modal-title">${t("top.backups")}</h3>
    <p class="modal-text">${t("backups.text")}</p>
    ${backups === null ? html`<div class="empty"><span class="spinner small"></span> ${t("backups.loading")}</div>` : null}
    ${showcase ? html`<div class="empty">${t("backups.showcase")}</div>` : null}
    ${backups && !backups.length && !showcase ? html`<div class="empty">${t("backups.none")}</div>` : null}
    ${backups?.length
      ? html`<ul class="backup-list">
          ${backups.map(
            (b) => html`<li class=${asking === b.name ? "is-asking" : ""}>
              <div class="backup-main">
                <strong>${formatDate(b.created)}</strong>
                <span>${b.summary ? t("backups.summary", { time: relativeTime(b.created), dock: t("backups.dock", { count: b.summary.dock }), pages: t("backups.pages", { count: b.summary.pages }), items: t("backups.items", { count: b.summary.items }) }) : relativeTime(b.created)}</span>
                <span class="backup-file">${b.name}</span>
              </div>
              ${asking === b.name
                ? html`<div class="backup-confirm">
                    <span>${t("backups.ask")}</span>
                    <button class="btn" onClick=${() => setAsking(null)}>${t("action.cancel")}</button>
                    <button class="btn btn-primary" disabled=${running} onClick=${() => actions.restoreBackup(b.name)}>${t("job.restore")}</button>
                  </div>`
                : html`<button class="btn" disabled=${running} onClick=${() => setAsking(b.name)}>${t("backups.restore_more")}</button>`}
            </li>`,
          )}
        </ul>`
      : null}
    <div class="modal-actions"><button class="btn btn-primary" onClick=${close}>${t("action.close")}</button></div>
  <//>`;
}

function ConfirmRemove() {
  const { item } = getState().dialog;
  return html`<${Modal} title=${t("remove.button")} tone="danger">
    <h3 class="modal-title">${t("remove.title", { name: item.name })}</h3>
    <p class="modal-text">${t("remove.text")}</p>
    <div class="modal-actions">
      <button class="btn" data-autofocus onClick=${close}>${t("remove.keep")}</button>
      <button class="btn btn-danger" onClick=${actions.confirmRemove}>${t("remove.button")}</button>
    </div>
  <//>`;
}

function ConfirmRead() {
  return html`<${Modal} title=${t("top.read")}>
    <h3 class="modal-title">${t("reread.title")}</h3>
    <p class="modal-text">${t("reread.text")}</p>
    <div class="modal-actions">
      <button class="btn" data-autofocus onClick=${close}>${t("reread.keep")}</button>
      <button class="btn btn-danger" onClick=${() => actions.readFromPhone({ confirmed: true })}>${t("reread.discard")}</button>
    </div>
  <//>`;
}

function ConfirmImport() {
  const { result, file } = getState().dialog;
  return html`<${Modal} title=${t("import.label")} tone="danger">
    <h3 class="modal-title">${t("import.title", { file, count: result.removed.length })}</h3>
    <p class="modal-text">${t("import.text", { names: result.removed.map((x) => x.name).join(", ") })}</p>
    <div class="modal-actions">
      <button class="btn" data-autofocus onClick=${close}>${t("action.cancel")}</button>
      <button class="btn btn-danger" onClick=${() => actions.useImported(result)}>${t("import.confirm")}</button>
    </div>
  <//>`;
}

function ImportIssues() {
  const { issues, file } = getState().dialog;
  return html`<${Modal} title=${t("import.issues_label")}>
    <h3 class="modal-title">${t("import.issues_title", { file })}</h3>
    <ul class="issue-list">${issues.map((issue) => html`<li>${issueText(issue, actions.nameOf)}</li>`)}</ul>
    <div class="modal-actions"><button class="btn btn-primary" onClick=${close}>${t("action.close")}</button></div>
  <//>`;
}

// Showcase mode looks like the normal editor, so Apply explains instead of writing.
function ShowcaseNotice() {
  return html`<${Modal} title=${t("showcase.label")}>
    <h3 class="modal-title">${t("showcase.title")}</h3>
    <p class="modal-text">${renderCode(t("showcase.text"))}</p>
    <div class="modal-actions"><button class="btn btn-primary" data-autofocus onClick=${close}>${t("action.ok")}</button></div>
  <//>`;
}

function ErrorDialog() {
  const error = errorText(getState().dialog.error);
  return html`<${Modal} title=${error.title}>
    <h3 class="modal-title">${error.title}</h3>
    ${error.steps?.length ? html`<ol class="screen-steps">${error.steps.map((s) => html`<li>${renderCode(s)}</li>`)}</ol>` : null}
    ${error.detail ? html`<details class="screen-detail"><summary>${t("error.details")}</summary><code>${error.detail}</code></details>` : null}
    <div class="modal-actions">
      <button class="btn" onClick=${close}>${t("action.close")}</button>
      <button class="btn btn-primary" onClick=${() => actions.readFromPhone({ confirmed: true })}>${t("action.try_again")}</button>
    </div>
  <//>`;
}

export function Dialogs() {
  const state = useStore();
  const kind = state.dialog?.kind;
  if (kind === "apply") return html`<${ApplyDialog} />`;
  if (kind === "job") return html`<${JobDialog} />`;
  if (kind === "backups") return html`<${BackupsDialog} />`;
  if (kind === "confirm-remove") return html`<${ConfirmRemove} />`;
  if (kind === "confirm-read") return html`<${ConfirmRead} />`;
  if (kind === "confirm-import") return html`<${ConfirmImport} />`;
  if (kind === "import-issues") return html`<${ImportIssues} />`;
  if (kind === "error") return html`<${ErrorDialog} />`;
  if (kind === "showcase") return html`<${ShowcaseNotice} />`;
  return null;
}

// ------------------------------------------------------------------ context menu

function menuEntries(item) {
  const state = getState();
  const draft = state.draft;
  const where = locate(draft, item.id);
  if (!where) return [];
  const entries = [];
  const inFolder = where.c.s === "folder";
  if (item.type === "folder") {
    entries.push({ label: t("menu.open"), run: () => actions.openFolder(item.id) });
    entries.push({ label: t("menu.rename"), run: () => actions.openFolder(item.id, true) });
    entries.push({ label: t("menu.unpack"), run: () => actions.ungroupFolder(item) });
  }
  if (inFolder) {
    entries.push({ label: t("menu.move_out"), run: () => actions.moveTo(item, { s: "page", p: state.page }) });
  }
  const base = removeId(draft, item.id).draft;
  const move = (label, c) => {
    const blocked = blockReason(base, item, c);
    entries.push({
      label: blocked ? t(blocked.code === "dock_full" ? "menu.full" : "menu.no_room", { label }) : label,
      disabled: Boolean(blocked),
      run: () => actions.moveTo(item, c),
    });
  };
  if (!inFolder && where.c.s !== "dock" && item.type !== "widget") move(t("menu.to_dock"), { s: "dock" });
  draft.pages.forEach((_, p) => {
    const samePlace = where.c.s === "page" && where.c.p === p;
    if (!samePlace) move(t("menu.to_page", { page: p + 1 }), { s: "page", p });
  });
  if (!inFolder && item.type !== "folder" && item.type !== "widget") {
    entries.push({ label: t("menu.new_folder"), run: () => actions.intoNewFolder(item) });
  }
  entries.push({ separator: true });
  if (item.type === "app") entries.push({ label: t("menu.to_library"), run: () => actions.sendAway(item) });
  if (item.type === "folder") entries.push({ label: t("menu.folder_to_library"), run: () => actions.sendAway(item) });
  if (REMOVABLE.has(item.type)) entries.push({ label: t("menu.remove_widget"), danger: true, run: () => actions.sendAway(item) });
  if (STUCK.has(item.type)) {
    entries.push({ label: t(item.type === "webapp" ? "menu.why_webapp" : "menu.why_webclip"), run: () => actions.sendAway(item) });
  }
  return entries;
}

export function ContextMenu() {
  const state = useStore();
  const menu = state.menu;
  const box = useRef(null);
  const [position, setPosition] = useState(null);
  useEffect(() => {
    if (!menu) return undefined;
    const away = (event) => {
      if (!box.current?.contains(event.target)) setState({ menu: null });
    };
    const key = (event) => event.key === "Escape" && setState({ menu: null });
    window.addEventListener("pointerdown", away, true);
    window.addEventListener("keydown", key);
    window.addEventListener("resize", away);
    return () => {
      window.removeEventListener("pointerdown", away, true);
      window.removeEventListener("keydown", key);
      window.removeEventListener("resize", away);
    };
  }, [menu]);
  useEffect(() => {
    if (!menu || !box.current) return setPosition(null);
    const rect = box.current.getBoundingClientRect();
    setPosition({
      x: Math.min(menu.x, window.innerWidth - rect.width - 8),
      y: Math.min(menu.y, window.innerHeight - rect.height - 8),
    });
  }, [menu]);
  if (!menu) return null;
  const entries = menuEntries(menu.item);
  const style = { left: `${(position || menu).x}px`, top: `${(position || menu).y}px`, visibility: position ? "visible" : "hidden" };
  return html`<div class="menu" role="menu" ref=${box} style=${style}>
    <div class="menu-title">${menu.item.name}</div>
    ${entries.map((entry) =>
      entry.separator
        ? html`<div class="menu-sep"></div>`
        : html`<button
            role="menuitem"
            disabled=${entry.disabled}
            class=${`menu-item${entry.danger ? " is-danger" : ""}`}
            onClick=${() => {
              setState({ menu: null });
              entry.run();
            }}
          >
            ${entry.label}
          </button>`,
    )}
  </div>`;
}

// ------------------------------------------------------------------ toasts

export function Toasts() {
  const state = useStore();
  return html`<div class="toasts" aria-live="polite">
    ${state.toasts.map(
      (entry) => html`<div class=${`toast tone-${entry.tone}`} key=${entry.id}>
        <span>${entry.text}</span>
        ${entry.action
          ? html`<button class="toast-action" onClick=${() => {
              actions.dismissToast(entry.id);
              entry.action.run();
            }}>${entry.action.label}</button>`
          : null}
        <button class="toast-close" aria-label=${t("action.dismiss")} onClick=${() => actions.dismissToast(entry.id)}>×</button>
      </div>`,
    )}
  </div>`;
}

