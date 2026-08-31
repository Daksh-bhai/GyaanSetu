import { useEffect, useState, useCallback } from "react";
import { useNavigate } from "react-router-dom";
import {
  getAllRequests, acceptRequest, rejectRequest,
  completeSession, cancelSession, rateTutor, reportUser, deleteSession
} from "../api";
import Navbar from "../components/Navbar";

const STATUS_STYLE = {
  pending:   "bg-amber-500/10 border-amber-500/30 text-amber-400",
  accepted:  "bg-blue-500/10 border-blue-500/30 text-blue-400",
  completed: "bg-emerald-500/10 border-emerald-500/30 text-emerald-400",
  cancelled: "bg-slate-700/50 border-slate-600 text-slate-400",
  rejected:  "bg-red-500/10 border-red-500/30 text-red-400",
};

const REPORT_CATEGORIES = [
  { value: "harassment",    label: "Harassment" },
  { value: "fraud",         label: "Fraud / Fake Skills" },
  { value: "spam",          label: "Spam" },
  { value: "inappropriate", label: "Inappropriate Behavior" },
  { value: "violence",      label: "Violence / Threats" },
];

// ── Live clock hook ───────────────────────────────────────────
function useTimer() {
  const [now, setNow] = useState(new Date());
  useEffect(() => {
    const t = setInterval(() => setNow(new Date()), 1000);
    return () => clearInterval(t);
  }, []);
  return now;
}

// ── Date formatter ────────────────────────────────────────────
// FIX: Append "Z" if missing so all dates are parsed as UTC by the browser.
// Python's isoformat() without Z is now fixed on backend too, but this
// provides a safe fallback for any legacy data in the DB.
function parseUTCDate(iso) {
  if (!iso) return null;
  try {
    // If string doesn't have timezone info, treat as UTC
    const str = (typeof iso === "string" && !iso.endsWith("Z") && !iso.includes("+"))
      ? iso + "Z"
      : iso;
    const d = new Date(str);
    return isNaN(d.getTime()) ? null : d;
  } catch {
    return null;
  }
}

function fmtDate(iso) {
  const d = parseUTCDate(iso);
  if (!d) return null;
  return d.toLocaleString("en-IN", {
    day:    "2-digit",
    month:  "short",
    year:   "numeric",
    hour:   "2-digit",
    minute: "2-digit",
    hour12: true,
  });
}

// ── Session timer info ────────────────────────────────────────
// Uses session_started_at (set when BOTH users join the room via socket).
// If null → nobody joined yet → show "Join to start".
// FIX: If session_started_at elapsed > duration, it means it was set from
// a previous visit. Show "Join session to sync timer" instead of "done".
function getTimerInfo(session, now) {
  if (session.status !== "accepted") return null;

  const startedAt = session.session_started_at || null;

  if (!startedAt) {
    return { notStarted: true };
  }

  const startMs     = parseUTCDate(startedAt)?.getTime();
  if (!startMs || isNaN(startMs)) return { notStarted: true };

  const durationMs   = (session.duration || 60) * 60 * 1000;
  const nowMs        = now.getTime();
  const elapsedMs    = nowMs - startMs;
  const remainingMs  = durationMs - elapsedMs;
  const elapsedSec   = Math.floor(elapsedMs / 1000);
  const remainingSec = Math.max(0, Math.floor(remainingMs / 1000));
  const isDone       = elapsedMs >= durationMs;
  const pct          = Math.min(100, (elapsedSec / (durationMs / 1000)) * 100);
  const elapsedMin   = Math.floor(elapsedSec / 60);
  const total        = session.duration || 60;

  // FIX: If elapsed > 2× duration, session_started_at is probably stale from
  // a previous room visit. Treat as "not started" so it doesn't falsely show "done".
  if (elapsedMs > durationMs * 2) {
    return { notStarted: true, stale: true };
  }

  const fmt = (s) => {
    const h   = Math.floor(s / 3600);
    const m   = Math.floor((s % 3600) / 60);
    const sec = s % 60;
    if (h > 0) return `${h}:${String(m).padStart(2,"0")}:${String(sec).padStart(2,"0")}`;
    return `${String(m).padStart(2,"0")}:${String(sec).padStart(2,"0")}`;
  };

  return { notStarted: false, remainingSec, isDone, formatted: fmt(remainingSec), elapsedMin, total, pct };
}

export default function Sessions() {
  const navigate = useNavigate();
  const now      = useTimer();
  const myEmail  = localStorage.getItem("email") || "";

  const [sessions,  setSessions]  = useState([]);
  const [loading,   setLoading]   = useState(true);
  const [toast,     setToast]     = useState({ msg: "", type: "success" });

  // Delete confirmation state
  const [deleteConfirm, setDeleteConfirm] = useState(null); // session object

  const [ratingModal,  setRatingModal]  = useState(null);
  const [rating,       setRating]       = useState(5);
  const [comment,      setComment]      = useState("");

  const [reportModal,  setReportModal]  = useState(null);
  const [reportCat,    setReportCat]    = useState("harassment");
  const [reportDesc,   setReportDesc]   = useState("");
  const [submitting,   setSubmitting]   = useState(false);

  const fetchSessions = useCallback(async () => {
    try {
      const res = await getAllRequests();
      setSessions(Array.isArray(res.data) ? res.data : []);
    } catch {
      localStorage.clear(); navigate("/login");
    } finally { setLoading(false); }
  }, [navigate]);

  useEffect(() => { fetchSessions(); }, [fetchSessions]);

  const showToast = (msg, type = "success") => {
    setToast({ msg, type });
    setTimeout(() => setToast({ msg: "", type: "success" }), 3500);
  };

  const action = async (fn, id, successMsg) => {
    try {
      const res  = await fn(id);
      const data = res?.data || {};
      if (data.early_complete) {
        showToast(`⚠️ Early complete — credits refunded (${data.refunded_to_requester} credits)`, "warn");
      } else {
        showToast(successMsg);
      }
      fetchSessions();
    } catch (e) {
      showToast(e.response?.data?.error || "Action failed", "error");
    }
  };

  const handleDelete = async (sessionId) => {
    try {
      await deleteSession(sessionId);
      showToast("🗑️ Session deleted");
      setSessions(prev => prev.filter(s => (s._id || s.session_id) !== sessionId));
    } catch (e) {
      showToast(e.response?.data?.error || "Delete failed", "error");
    } finally {
      setDeleteConfirm(null);
    }
  };

  const submitRating = async () => {
    setSubmitting(true);
    try {
      await rateTutor(ratingModal.reporteeEmail, { rating, comment });
      showToast("✅ Rating submitted!");
      setRatingModal(null); setRating(5); setComment("");
      fetchSessions();
    } catch (e) {
      showToast(e.response?.data?.error || "Rating failed", "error");
    } finally { setSubmitting(false); }
  };

  const submitReport = async () => {
    setSubmitting(true);
    try {
      await reportUser(reportModal.email, { category: reportCat, description: reportDesc });
      showToast("🚨 Report submitted");
      setReportModal(null); setReportCat("harassment"); setReportDesc("");
    } catch (e) {
      showToast(e.response?.data?.error || "Report failed", "error");
    } finally { setSubmitting(false); }
  };

  const isAccepter  = (s) => s.tutor?.email  === myEmail;
  const isRequester = (s) => s.learner?.email === myEmail;

  // Robust date parser — handles strings with/without Z, and Date objects
  const toMs = (val) => {
    if (!val) return 0;
    if (val instanceof Date) return val.getTime();
    const s = typeof val === "string"
      ? (val.endsWith("Z") || val.includes("+") ? val : val + "Z")
      : String(val);
    const ms = new Date(s).getTime();
    return isNaN(ms) ? 0 : ms;
  };

  const sorted = [...sessions].sort((a, b) => {
    const order = { accepted: 0, pending: 1, completed: 2, cancelled: 3, rejected: 4 };
    const statusDiff = (order[a.status] ?? 9) - (order[b.status] ?? 9);
    if (statusDiff !== 0) return statusDiff;
    // Same status → latest first (newest created_at on top)
    return toMs(b.created_at) - toMs(a.created_at);
  });

  if (loading) return <Spinner />;

  return (
    <div className="min-h-screen bg-slate-950 text-white">
      <Navbar />
      <div className="max-w-4xl mx-auto px-6 pt-24 pb-12">

        <div className="flex items-center justify-between mb-8">
          <div>
            <h1 className="text-3xl font-black">Sessions</h1>
            <p className="text-slate-400 mt-1">{sessions.length} total sessions</p>
          </div>
          {toast.msg && (
            <div className={`px-4 py-2 text-sm rounded-xl border ${
              toast.type === "error" ? "bg-red-500/10 border-red-500/30 text-red-400"
              : toast.type === "warn" ? "bg-amber-500/10 border-amber-500/30 text-amber-400"
              : "bg-emerald-500/10 border-emerald-500/30 text-emerald-400"
            }`}>{toast.msg}</div>
          )}
        </div>

        {sorted.length === 0 ? (
          <div className="text-center py-24 text-slate-500">
            <p className="text-5xl mb-4">📭</p>
            <p className="text-lg font-semibold">No sessions yet</p>
          </div>
        ) : (
          <div className="space-y-4">
            {sorted.map((s) => {
              const sessionId = s._id || s.session_id;
              const timer     = getTimerInfo(s, now);
              const accepter  = isAccepter(s);
              const requester = isRequester(s);
              const isDeletable = ["completed", "cancelled", "rejected"].includes(s.status);

              return (
                <div key={sessionId}
                  className={`bg-slate-900 border rounded-2xl p-6 transition-all ${
                    s.status === "accepted"
                      ? "border-blue-500/40 ring-1 ring-blue-500/10"
                      : "border-slate-800 hover:border-slate-700"
                  }`}>

                  <div className="flex items-start justify-between gap-4 flex-wrap">
                    <div className="flex-1 min-w-0">

                      {/* ── Status row ── */}
                      <div className="flex items-center gap-3 flex-wrap">
                        <span className="text-white font-bold capitalize text-lg">{s.skill}</span>
                        <span className={`text-xs px-2.5 py-1 border rounded-full font-medium capitalize ${STATUS_STYLE[s.status] || ""}`}>
                          {s.status}
                        </span>
                        {s.duration && <span className="text-slate-500 text-xs">⏱ {s.duration} min</span>}
                        {s.early_complete && (
                          <span className="text-xs px-2 py-0.5 bg-orange-500/10 border border-orange-500/30 text-orange-400 rounded-full">
                            Early ended
                          </span>
                        )}
                      </div>

                      {/* ── People & credits ── */}
                      <div className="flex flex-wrap gap-4 mt-2 text-sm text-slate-400">
                        <span>🎓 <span className="text-slate-300">{s.learner?.name || "?"}</span>
                          {requester && <span className="text-emerald-400 text-xs ml-1">(you)</span>}
                        </span>
                        <span>🧑‍🏫 <span className="text-slate-300">{s.tutor?.name || "?"}</span>
                          {accepter && <span className="text-emerald-400 text-xs ml-1">(you)</span>}
                        </span>
                        {s.credits_used && <span>💰 {s.credits_used} credit(s)</span>}
                      </div>

                      {/* ── DATE / TIME INFO ── */}
                      <div className="flex flex-wrap gap-x-4 gap-y-0.5 mt-2">
                        {s.created_at && (
                          <span className="text-[11px] text-slate-600 flex items-center gap-1">
                            <span>📅</span>
                            <span>Requested: <span className="text-slate-500">{fmtDate(s.created_at)}</span></span>
                          </span>
                        )}
                        {s.accepted_at && (s.status === "accepted" || s.status === "completed") && (
                          <span className="text-[11px] text-slate-600 flex items-center gap-1">
                            <span>✅</span>
                            <span>Accepted: <span className="text-slate-500">{fmtDate(s.accepted_at)}</span></span>
                          </span>
                        )}
                        {s.completed_at && s.status === "completed" && (
                          <span className="text-[11px] text-slate-600 flex items-center gap-1">
                            <span>🏁</span>
                            <span>Completed: <span className="text-slate-500">{fmtDate(s.completed_at)}</span></span>
                          </span>
                        )}
                        {s.cancelled_at && s.status === "cancelled" && (
                          <span className="text-[11px] text-slate-600 flex items-center gap-1">
                            <span>❌</span>
                            <span>Cancelled: <span className="text-slate-500">{fmtDate(s.cancelled_at)}</span></span>
                          </span>
                        )}
                      </div>
                    </div>

                    {/* ── Actions ── */}
                    <div className="flex flex-col gap-2 shrink-0 min-w-[130px]">

                      {/* ACCEPTED: join button */}
                      {s.status === "accepted" && (
                        <button
                          onClick={() => navigate(`/session/${sessionId}`)}
                          className="px-4 py-2.5 bg-emerald-500 hover:bg-emerald-400 text-white text-xs font-bold rounded-lg transition-all flex items-center justify-center gap-1.5 animate-pulse hover:animate-none">
                          🎯 Join Session
                        </button>
                      )}

                      {/* PENDING: accepter actions */}
                      {s.status === "pending" && accepter && (
                        <>
                          <Btn color="green" onClick={() => action(acceptRequest, sessionId, "✅ Accepted!")}>Accept</Btn>
                          <Btn color="red"   onClick={() => action(rejectRequest, sessionId, "Rejected")}>Reject</Btn>
                          <Btn color="gray"  onClick={() => action(cancelSession, sessionId, "Cancelled")}>Cancel</Btn>
                        </>
                      )}
                      {s.status === "pending" && requester && (
                        <Btn color="gray" onClick={() => action(cancelSession, sessionId, "Cancelled")}>Cancel</Btn>
                      )}

                      {/* COMPLETED: rate + report */}
                      {s.status === "completed" && requester && !s.rated && (
                        <Btn color="amber"
                          onClick={() => { setRatingModal({ sessionId, reporteeEmail: s.tutor?.email, reporteeName: s.tutor?.name }); setRating(5); setComment(""); }}>
                          Rate ⭐
                        </Btn>
                      )}
                      {s.status === "completed" && requester && (
                        <Btn color="red-outline"
                          onClick={() => setReportModal({ email: s.tutor?.email, name: s.tutor?.name })}>
                          Report 🚨
                        </Btn>
                      )}
                      {s.status === "completed" && accepter && (
                        <Btn color="red-outline"
                          onClick={() => setReportModal({ email: s.learner?.email, name: s.learner?.name })}>
                          Report 🚨
                        </Btn>
                      )}

                      {/* DELETE button for completed/cancelled/rejected */}
                      {isDeletable && (
                        <Btn color="delete" onClick={() => setDeleteConfirm({ id: sessionId, skill: s.skill, status: s.status })}>
                          🗑️ Delete
                        </Btn>
                      )}
                    </div>
                  </div>

                  {/* ── TIMER BAR for accepted sessions ── */}
                  {s.status === "accepted" && timer && (
                    <TimerBar timer={timer} duration={s.duration || 60} />
                  )}

                  {/* Early complete notice */}
                  {s.status === "completed" && s.early_complete && (
                    <div className="mt-3 px-4 py-2 bg-orange-500/10 border border-orange-500/20 rounded-xl text-xs text-orange-400">
                      ⚠️ Session ended before scheduled duration. Credits were refunded to requester.
                    </div>
                  )}
                </div>
              );
            })}
          </div>
        )}
      </div>

      {/* ── Delete Confirm Modal ── */}
      {deleteConfirm && (
        <Modal onClose={() => setDeleteConfirm(null)}>
          <div className="text-center">
            <p className="text-4xl mb-4">🗑️</p>
            <h3 className="text-white font-black text-xl mb-2">Delete Session?</h3>
            <p className="text-slate-400 text-sm mb-2">
              This will permanently remove the <span className="capitalize font-semibold text-white">{deleteConfirm.skill}</span> session from your history.
            </p>
            <p className="text-slate-500 text-xs mb-6">
              Status: <span className="capitalize">{deleteConfirm.status}</span> · This action cannot be undone.
            </p>
            <div className="flex gap-3">
              <button onClick={() => setDeleteConfirm(null)}
                className="flex-1 py-3 border border-slate-700 text-slate-400 rounded-xl text-sm font-semibold hover:border-slate-500 transition-all">
                Cancel
              </button>
              <button onClick={() => handleDelete(deleteConfirm.id)}
                className="flex-1 py-3 bg-red-500 hover:bg-red-400 text-white rounded-xl text-sm font-bold transition-all">
                Yes, Delete
              </button>
            </div>
          </div>
        </Modal>
      )}

      {/* ── Rating Modal ── */}
      {ratingModal && (
        <Modal onClose={() => setRatingModal(null)}>
          <h3 className="text-white font-black text-xl mb-1">Rate Session</h3>
          <p className="text-slate-400 text-sm mb-6">with <span className="text-emerald-400">{ratingModal.reporteeName}</span></p>
          <div className="flex gap-2 justify-center mb-6">
            {[1,2,3,4,5].map(n => (
              <button key={n} onClick={() => setRating(n)}
                className={`text-3xl transition-all hover:scale-110 ${n <= rating ? "opacity-100" : "opacity-30"}`}>⭐</button>
            ))}
          </div>
          <textarea value={comment} onChange={e => setComment(e.target.value)}
            placeholder="Leave a comment (optional)..." rows={3}
            className="w-full bg-slate-800 border border-slate-700 text-white rounded-xl px-4 py-3 text-sm focus:outline-none focus:border-emerald-500 resize-none mb-4"
          />
          <div className="flex gap-3">
            <button onClick={() => setRatingModal(null)}
              className="flex-1 py-3 border border-slate-700 text-slate-400 rounded-xl text-sm font-semibold hover:border-slate-500 transition-all">Cancel</button>
            <button onClick={submitRating} disabled={submitting}
              className="flex-1 py-3 bg-emerald-500 hover:bg-emerald-400 disabled:opacity-50 text-white rounded-xl text-sm font-bold transition-all">
              {submitting ? "Submitting..." : "Submit Rating"}
            </button>
          </div>
        </Modal>
      )}

      {/* ── Report Modal ── */}
      {reportModal && (
        <Modal onClose={() => setReportModal(null)}>
          <h3 className="text-white font-black text-xl mb-1">Report User</h3>
          <p className="text-slate-400 text-sm mb-6">Reporting <span className="text-red-400">{reportModal.name}</span></p>
          <div className="mb-4">
            <label className="text-slate-300 text-sm font-medium mb-2 block">Category</label>
            <div className="grid grid-cols-1 gap-2">
              {REPORT_CATEGORIES.map(c => (
                <button key={c.value} onClick={() => setReportCat(c.value)}
                  className={`text-left px-4 py-2.5 rounded-xl border text-sm transition-all ${
                    reportCat === c.value
                      ? "border-red-500/60 bg-red-500/10 text-red-400"
                      : "border-slate-700 text-slate-400 hover:border-slate-500"
                  }`}>{c.label}</button>
              ))}
            </div>
          </div>
          <textarea value={reportDesc} onChange={e => setReportDesc(e.target.value)}
            placeholder="Describe what happened (optional)..." rows={3}
            className="w-full bg-slate-800 border border-slate-700 text-white rounded-xl px-4 py-3 text-sm focus:outline-none focus:border-red-500 resize-none mb-4"
          />
          <div className="flex gap-3">
            <button onClick={() => setReportModal(null)}
              className="flex-1 py-3 border border-slate-700 text-slate-400 rounded-xl text-sm font-semibold hover:border-slate-500 transition-all">Cancel</button>
            <button onClick={submitReport} disabled={submitting}
              className="flex-1 py-3 bg-red-500 hover:bg-red-400 disabled:opacity-50 text-white rounded-xl text-sm font-bold transition-all">
              {submitting ? "Reporting..." : "Submit Report 🚨"}
            </button>
          </div>
        </Modal>
      )}
    </div>
  );
}

// ================================================================
// TIMER BAR
// notStarted / stale → show "Join to start timer"
// running → countdown
// done → completed
// ================================================================
function TimerBar({ timer, duration }) {
  if (timer.notStarted) {
    return (
      <div className="mt-4 pt-4 border-t border-slate-800">
        <div className="flex items-center justify-between mb-2">
          <span className="text-xs text-slate-400">Session Timer</span>
          <span className="text-xs text-slate-500 flex items-center gap-1.5">
            <span className="w-1.5 h-1.5 rounded-full bg-slate-600 animate-pulse" />
            {timer.stale
              ? "Join session to sync timer"
              : `Waiting — join to start the ${duration}-min timer`
            }
          </span>
        </div>
        <div className="h-1.5 bg-slate-800 rounded-full overflow-hidden">
          <div className="h-full w-0 bg-blue-500 rounded-full" />
        </div>
      </div>
    );
  }

  const pct = Math.max(0, Math.min(100, timer.pct || 0));

  return (
    <div className="mt-4 pt-4 border-t border-slate-800">
      <div className="flex items-center justify-between mb-2">
        <span className="text-xs text-slate-400">Session Timer</span>
        <span className={`text-sm font-mono font-bold ${
          timer.isDone ? "text-emerald-400" : timer.pct > 75 ? "text-amber-400" : "text-blue-400"
        }`}>
          {timer.isDone
            ? "⏰ Time's up — ready to complete!"
            : `⏱ ${timer.formatted} remaining`}
        </span>
      </div>
      <div className="h-1.5 bg-slate-800 rounded-full overflow-hidden">
        <div className={`h-full rounded-full transition-all duration-1000 ${
          timer.isDone ? "bg-emerald-500" : timer.pct > 75 ? "bg-amber-500" : "bg-blue-500"
        }`} style={{ width: `${pct}%` }} />
      </div>
      {!timer.isDone && (
        <p className="text-xs text-slate-500 mt-1">
          {timer.elapsedMin}/{duration} min elapsed ·{" "}
          <span className="text-amber-400">Join session to chat & video call</span>
        </p>
      )}
    </div>
  );
}

function Btn({ children, onClick, color = "gray" }) {
  const styles = {
    green:        "bg-emerald-500 hover:bg-emerald-400 text-white",
    blue:         "bg-blue-500 hover:bg-blue-400 text-white",
    red:          "bg-red-500/10 border border-red-500/30 text-red-400 hover:bg-red-500/20",
    amber:        "bg-amber-500/10 border border-amber-500/30 text-amber-400 hover:bg-amber-500/20",
    gray:         "bg-slate-700 hover:bg-slate-600 text-slate-300",
    "red-outline":"border border-red-500/30 text-red-400 hover:bg-red-500/10",
    "delete":     "border border-slate-600 text-slate-500 hover:border-red-500/50 hover:text-red-400 hover:bg-red-500/5",
  };
  return (
    <button onClick={onClick}
      className={`px-4 py-2 text-xs font-bold rounded-lg transition-all ${styles[color] || styles.gray}`}>
      {children}
    </button>
  );
}

function Modal({ children, onClose }) {
  return (
    <div className="fixed inset-0 bg-black/70 backdrop-blur-sm flex items-center justify-center z-50 px-4">
      <div className="bg-slate-900 border border-slate-700 rounded-2xl p-8 max-w-md w-full max-h-[90vh] overflow-y-auto">
        {children}
      </div>
    </div>
  );
}

function Spinner() {
  return (
    <div className="min-h-screen bg-slate-950 flex items-center justify-center">
      <div className="w-8 h-8 border-2 border-emerald-500 border-t-transparent rounded-full animate-spin" />
    </div>
  );
}