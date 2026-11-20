// Plain-language text for planner issue codes, changes, places, server errors and job
// events, in the editor's language (see i18n.js).

import { has, joinList, language, t, tList } from "./i18n.js";
import { rowCol } from "./layout.js";

const quote = (text) => t("quote", { text });

// Why a drop was refused, in a few words (shown on the dragged icon).
export function refusalShort(problem) {
  const key = `refusal.${problem?.code}`;
  return has(key) ? t(key) : t("refusal.default");
}

// A refused drop, as a sentence.
export function refusalText(problem, nameOf = (id) => id) {
  const d = problem.details || {};
  switch (problem.code) {
    case "dock_full":
      return t("refused.dock_full", { count: d.capacity ?? 4 });
    case "page_full":
      return t("refused.page_full", { page: problem.location?.page ?? "", capacity: d.capacity ?? 24 });
    case "folder_to_library":
      return t("refused.folder_to_library");
    default:
      return issueText(problem, nameOf);
  }
}

// Plain sentence for a planner issue ({code, message, location, details}).
export function issueText(issue, nameOf = (id) => id) {
  const d = issue.details || {};
  const where = issue.location || {};
  const name = d.id ? quote(nameOf(d.id)) : t("issue.an_item");
  switch (issue.code) {
    case "too_many_pages":
      return t("issue.too_many_pages", { count: d.capacity ?? 15 });
    case "hidden_app":
      return t("issue.hidden_app", { name });
    case "dock_full": {
      const capacity = d.capacity ?? 4;
      return t("issue.dock_full", { capacity, count: (d.count ?? 5) - capacity });
    }
    case "page_full":
      return t("issue.page_full", { page: where.page ?? "?", cells: d.cells, capacity: d.capacity ?? 24 });
    case "widget_in_dock":
    case "widget_in_folder":
    case "nested_folder":
    case "folder_name_missing":
    case "duplicate_item":
    case "unknown_app":
    case "unknown_item":
      return t(`issue.${issue.code}`, { name });
    case "empty_folder":
    case "empty_folder_page":
      return t("issue.empty_folder", { folder: quote(where.folder || "") });
    case "wrong_kind":
      return t("issue.wrong_kind", { name, kind: kindName(d.kind) });
    case "ambiguous_name":
      return t("issue.ambiguous_name", { name: quote(d.name) });
    case "not_removable": {
      const kind = d.kind === "webapp" ? "webapp" : "webclip";
      return t(`issue.not_removable.${kind}`, { name: quote(d.name || nameOf(d.id)) });
    }
    case "removal_not_allowed": {
      const ids = d.ids || [];
      return t("issue.removal_not_allowed", { names: joinList(ids.map((id) => quote(nameOf(id)))) });
    }
    case "invalid_toml":
      return t("issue.invalid_toml", { detail: issue.message.replace(/^invalid TOML: /, "") });
    default:
      // Codes without a translation (hand-edited layout files) keep the server's English.
      return issue.message ? issue.message[0].toUpperCase() + issue.message.slice(1) : issue.code;
  }
}

export function kindName(type) {
  return t(has(`kind.${type}`) ? `kind.${type}` : "kind.item");
}

// Where a change puts an item, as the user sees it: "page 1, row 5, column 2".
function destination(where, id, draft, pageIndex) {
  if (!where) return "";
  if (where.folder) return t("dest.folder", { folder: quote(where.folder) });
  if (where.section === "dock") return t("dest.dock", { index: where.index });
  const index = pageIndex(where.page);
  const spot = index == null ? null : rowCol(draft.pages[index] || [], id);
  return spot ? t("dest.page_spot", { page: where.page, row: spot.row, col: spot.col }) : t("dest.page", { page: where.page });
}

// { title, detail, tone } for one change from the server: the item's name and, in
// plain words, what happens to it.
export function describeChange(change, draft) {
  const nonEmpty = draft.pages.map((p, i) => (p.length ? i : null)).filter((i) => i !== null);
  const pageIndex = (page) => nonEmpty[page - 1] ?? null;
  const to = () => destination(change.to, change.id, draft, pageIndex);
  const kind = kindName(change.type);
  const name = change.name || kind[0].toLocaleUpperCase() + kind.slice(1);
  switch (change.kind) {
    case "added":
      if (change.type && change.type !== "app") return { title: name, detail: t("change.added", { where: to() }), tone: "add" };
      return { title: name, detail: t("change.from_library", { where: to() }), tone: "add" };
    case "moved":
    case "reordered":
      return { title: name, detail: t("change.moved", { where: to() }), tone: "move" };
    case "to_library":
      return { title: name, detail: t("change.to_library"), tone: "library" };
    case "removed": {
      const key = has(`change.removed.${change.type}`) ? `change.removed.${change.type}` : "change.removed.item";
      return { title: name, detail: t(key), tone: "danger" };
    }
    case "folder_created":
      return { title: name, detail: t("change.folder_created", { where: to() }), tone: "add" };
    case "folder_renamed":
      return { title: name, detail: t("change.folder_renamed", { old: quote(change.old_name) }), tone: "move" };
    case "folder_deleted":
      return { title: name, detail: t("change.folder_deleted"), tone: "library" };
    case "pages":
      return { title: t("change.pages_title"), detail: t("change.pages", { before: change.before, after: change.after }), tone: "move" };
    default:
      return { title: name, detail: change.kind, tone: "move" };
  }
}

export function relativeTime(iso) {
  if (!iso) return "";
  const then = new Date(iso);
  const seconds = Math.round((Date.now() - then.getTime()) / 1000);
  if (Number.isNaN(seconds)) return "";
  if (seconds < 45) return t("time.just_now");
  const format = new Intl.RelativeTimeFormat(language(), { numeric: "always" });
  const minutes = Math.round(seconds / 60);
  if (minutes < 60) return format.format(-minutes, "minute");
  const hours = Math.round(minutes / 60);
  if (hours < 24) return format.format(-hours, "hour");
  return format.format(-Math.round(hours / 24), "day");
}

export function formatDate(iso) {
  const date = new Date(iso);
  if (Number.isNaN(date.getTime())) return iso;
  return date.toLocaleString(language(), {
    year: "numeric",
    month: "short",
    day: "numeric",
    hour: "2-digit",
    minute: "2-digit",
    second: "2-digit",
  });
}

// ------------------------------------------------------------------ server text

// The server's friendly errors ({code, title, steps, detail}) are English; the codes
// pick the translation. Generic ones (no known code) are matched by their title.
const GENERIC_TITLES = {
  "The layout has problems": "layout",
  "The file or layout cannot be used": "state",
  "The iPhone operation failed": "device",
  "Something went wrong": "other",
};

// The USB service help depends on the system, like ui/errors.py. The editor only
// listens on 127.0.0.1, so the browser runs on the same system as the server.
function system() {
  const name = navigator.userAgentData?.platform || navigator.platform || "";
  if (/^mac/i.test(name)) return "darwin";
  if (/^win/i.test(name)) return "win32";
  return "linux";
}

export function errorText(error) {
  if (!error) return error;
  let key = `error.${error.code}`;
  if (error.code === "usbmuxd_unreachable") key = `error.usbmuxd_unreachable.${system()}`;
  if (!has(`${key}.title`)) {
    const generic = GENERIC_TITLES[error.title];
    if (!generic) return error;
    key = `error.generic.${generic}`;
  }
  let steps = tList(`${key}.steps`) || [];
  if (error.code === "timeout" || error.code === "connection_failed") steps = [...steps, t(`error.restart.${system()}`)];
  return { ...error, title: t(`${key}.title`), steps };
}

// An API failure for a toast: the server's message unless its code has a translation.
export function apiErrorText(error) {
  if (error?.code === "offline") return t("api.offline");
  if (error?.code === "busy") return t("api.busy");
  if (error?.code === "showcase") return errorText({ code: "showcase", title: "" }).title;
  if (error?.code === "unexpected" && error.data?.error) return errorText(error.data.error).title;
  return error?.message || String(error);
}

const fileName = (path) => String(path || "").split(/[\\/]/).pop();

// A job event ({code, message, step, total, data}) in the editor's language; events
// without a translation keep the server's message.
export function eventText(event, nameOf = (id) => id) {
  if (!event) return "";
  const data = event.data || {};
  const names = () => joinList((data.ids || []).map((id) => nameOf(id)));
  switch (event.code) {
    case "reading":
      return t(event.total === 5 ? "event.reading_backup" : "event.reading");
    case "backup_saved":
      return t("event.backup_saved", { file: fileName(data.path) });
    case "read_saved":
      return t("event.read_saved", { file: fileName(data.path) });
    case "showcase":
      return data.path ? t("event.showcase", { file: fileName(data.path) }) : event.message;
    case "writing":
      return t("event.writing", { count: data.ignored ?? 0 });
    case "widgets_reflowed":
    case "webclips_added":
      return t(`event.${event.code}`, { names: names() });
    case "rollback_failed":
      return t("event.rollback_failed", { file: fileName(data.path) });
    case "failed":
      return errorText({ code: data.code, title: event.message }).title;
    default:
      return has(`event.${event.code}`) ? t(`event.${event.code}`) : event.message;
  }
}
