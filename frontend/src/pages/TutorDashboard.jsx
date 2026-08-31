import { useEffect, useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { getProfile, getCredits, testStatus, updateBio, getReviews, getSimilarTutors } from "../api";
import Navbar from "../components/Navbar";

const badgeColor = {
  Expert:       "text-amber-400 bg-amber-400/10 border-amber-400/30",
  Intermediate: "text-blue-400 bg-blue-400/10 border-blue-400/30",
  Beginner:     "text-emerald-400 bg-emerald-400/10 border-emerald-400/30",
};

const STARS = [1, 2, 3, 4, 5];

function StarDisplay({ rating }) {
  return (
    <div className="flex items-center gap-0.5">
      {STARS.map(n => (
        <span key={n} className={`text-sm ${n <= Math.round(rating) ? "text-amber-400" : "text-slate-700"}`}>★</span>
      ))}
    </div>
  );
}

export default function TutorDashboard() {
  const navigate = useNavigate();
  const [user,    setUser]    = useState(null);
  const [credits, setCredits] = useState(0);
  const [tStatus, setTStatus] = useState(null);
  const [reviews, setReviews] = useState([]);
  const [similar, setSimilar] = useState([]);
  const [bio,     setBio]     = useState("");
  const [editing, setEditing] = useState(false);
  const [msg,     setMsg]     = useState("");
  const [loading, setLoading] = useState(true);
  const [tab,     setTab]     = useState("overview"); // overview | reviews

  useEffect(() => {
    const role = localStorage.getItem("role");
    if (role !== "tutor") { navigate("/dashboard"); return; }
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      const [p, c, t] = await Promise.all([getProfile(), getCredits(), testStatus()]);
      setUser(p.data);
      setBio(p.data.bio || "");
      setCredits(c.data.credits);
      setTStatus(t.data);

      // Fetch reviews for this tutor
      if (p.data.email) {
        try {
          const r = await getReviews(p.data.email);
          setReviews(Array.isArray(r.data) ? r.data : []);
        } catch { setReviews([]); }
        try {
          const s = await getSimilarTutors(p.data.email, 4);
          setSimilar(Array.isArray(s.data) ? s.data : []);
        } catch { setSimilar([]); }
      }
    } catch {
      localStorage.clear();
      navigate("/login");
    } finally {
      setLoading(false);
    }
  };

  const saveBio = async () => {
    try {
      const { updateBio: upd } = await import("../api");
      await upd(bio);
      setMsg("Bio updated!");
      setEditing(false);
      setTimeout(() => setMsg(""), 3000);
    } catch (e) {
      setMsg(e.response?.data?.error || "Failed");
    }
  };

  if (loading) return <Spinner />;

  return (
    <div className="min-h-screen bg-slate-950 text-white">
      <Navbar />
      <div className="max-w-6xl mx-auto px-6 pt-24 pb-12">

        {/* Header */}
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 mb-6">
          <div>
            <h1 className="text-3xl font-black">Welcome, {user?.name} 👋</h1>
            <p className="text-slate-400 mt-1">Tutor Dashboard</p>
          </div>
          <div className="flex items-center gap-3">
            {user?.badge && (
              <span className={`px-3 py-1 text-xs font-bold border rounded-full ${badgeColor[user.badge] || badgeColor.Beginner}`}>
                {user.badge}
              </span>
            )}
            {!user?.is_verified && (
              <Link to="/verify"
                className="px-4 py-2 bg-amber-500 hover:bg-amber-400 text-white text-sm font-bold rounded-xl transition-all">
                Get Verified →
              </Link>
            )}
          </div>
        </div>

        {/* Stats Cards */}
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-4 mb-8">
          {[
            { label: "Credits",   value: credits,                       color: "text-emerald-400" },
            { label: "Sessions",  value: user?.sessions_completed || 0, color: "text-blue-400"    },
            { label: "Rating",    value: user?.rating ? `${user.rating} ⭐` : "—", color: "text-amber-400" },
            { label: "Reviews",   value: reviews.length,                 color: "text-purple-400"  },
          ].map(({ label, value, color }) => (
            <div key={label} className="bg-slate-900 border border-slate-800 rounded-2xl p-5">
              <p className="text-slate-400 text-xs font-medium uppercase tracking-wide mb-1">{label}</p>
              <p className={`text-2xl font-black ${color}`}>{value}</p>
            </div>
          ))}
        </div>

        {/* Tab Bar */}
        <div className="flex gap-1 bg-slate-900 border border-slate-800 rounded-xl p-1 mb-8 w-fit">
          {[
            { key: "overview", label: "📊 Overview" },
            { key: "reviews",  label: `⭐ Reviews (${reviews.length})` },
          ].map(t => (
            <button key={t.key} onClick={() => setTab(t.key)}
              className={`px-5 py-2 rounded-lg text-sm font-semibold transition-all ${
                tab === t.key
                  ? "bg-emerald-500/10 text-emerald-400 border border-emerald-500/30"
                  : "text-slate-400 hover:text-white"
              }`}>
              {t.label}
            </button>
          ))}
        </div>

        {/* ── OVERVIEW TAB ── */}
        {tab === "overview" && (
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">

            {/* Verification Status */}
            <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6">
              <h2 className="text-white font-bold text-lg mb-4">Verification Status</h2>
              {user?.is_verified ? (
                <div className="flex items-center gap-3 p-4 bg-emerald-500/10 border border-emerald-500/30 rounded-xl">
                  <span className="text-2xl">✅</span>
                  <div>
                    <p className="text-emerald-400 font-semibold">Verified Tutor</p>
                    <p className="text-slate-400 text-sm">{user.verified_skill} — {user.verified_level}</p>
                  </div>
                </div>
              ) : (
                <div className="p-4 bg-amber-500/10 border border-amber-500/30 rounded-xl">
                  <p className="text-amber-400 font-semibold mb-1">⚠️ Not Verified</p>
                  <p className="text-slate-400 text-sm mb-3">Pass a skill test to start accepting sessions.</p>
                  {tStatus && (
                    <p className="text-xs text-slate-500 mb-3">
                      Attempts: {tStatus.attempts_used}/{tStatus.max_attempts}
                      {tStatus.cooldown_active && ` · Wait ${tStatus.wait_minutes} min`}
                    </p>
                  )}
                  <Link to="/verify"
                    className="inline-block px-4 py-2 bg-amber-500 hover:bg-amber-400 text-white text-sm font-bold rounded-lg transition-all">
                    Take Skill Test →
                  </Link>
                </div>
              )}
            </div>

            {/* Skills */}
            <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6">
              <h2 className="text-white font-bold text-lg mb-4">My Skills</h2>
              <div className="space-y-4">
                <div>
                  <p className="text-xs text-slate-500 uppercase tracking-wide mb-2">I can teach</p>
                  <div className="flex flex-wrap gap-2">
                    {(user?.skills_i_can_teach || []).length > 0
                      ? user.skills_i_can_teach.map(s => (
                          <span key={s} className="px-2.5 py-1 bg-amber-500/10 border border-amber-500/30 text-amber-400 text-xs rounded-lg capitalize">{s}</span>
                        ))
                      : <span className="text-slate-500 text-sm">No teaching skills added</span>
                    }
                  </div>
                </div>
                <div>
                  <p className="text-xs text-slate-500 uppercase tracking-wide mb-2">I want to learn</p>
                  <div className="flex flex-wrap gap-2">
                    {(user?.skills_i_want_to_learn || []).length > 0
                      ? user.skills_i_want_to_learn.map(s => (
                          <span key={s} className="px-2.5 py-1 bg-emerald-500/10 border border-emerald-500/30 text-emerald-400 text-xs rounded-lg capitalize">{s}</span>
                        ))
                      : <span className="text-slate-500 text-sm">No learning skills added</span>
                    }
                  </div>
                </div>
              </div>
            </div>

            {/* Bio */}
            <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6">
              <div className="flex items-center justify-between mb-4">
                <h2 className="text-white font-bold text-lg">Bio</h2>
                <button onClick={() => setEditing(!editing)} className="text-emerald-400 text-sm hover:text-emerald-300">
                  {editing ? "Cancel" : "Edit"}
                </button>
              </div>
              {editing ? (
                <div className="space-y-3">
                  <textarea value={bio} onChange={e => setBio(e.target.value)} rows={4}
                    placeholder="Tell learners about yourself..."
                    className="w-full bg-slate-800 border border-slate-700 text-white rounded-xl px-4 py-3 text-sm focus:outline-none focus:border-emerald-500 resize-none"
                  />
                  <button onClick={saveBio}
                    className="px-4 py-2 bg-emerald-500 hover:bg-emerald-400 text-white text-sm font-bold rounded-lg transition-all">
                    Save Bio
                  </button>
                </div>
              ) : (
                <p className="text-slate-400 text-sm leading-relaxed">
                  {user?.bio || "No bio added yet. Click Edit to add one."}
                </p>
              )}
              {msg && <p className="text-emerald-400 text-xs mt-2">{msg}</p>}
            </div>

            {/* Quick Actions */}
            <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6">
              <h2 className="text-white font-bold text-lg mb-4">Quick Actions</h2>
              <div className="grid grid-cols-2 gap-3">
                {[
                  { to: "/smart-match", label: "🎯 Smart Match",  color: "border-emerald-500/50 hover:bg-emerald-500/10 text-emerald-400" },
                  { to: "/sessions",    label: "📋 My Sessions",  color: "border-blue-500/50 hover:bg-blue-500/10 text-blue-400"         },
                  { to: "/learn",       label: "📚 Learn a Skill",color: "border-purple-500/50 hover:bg-purple-500/10 text-purple-400"   },
                  { to: "/verify",      label: "✅ Get Verified", color: "border-amber-500/50 hover:bg-amber-500/10 text-amber-400"      },
                ].map(({ to, label, color }) => (
                  <Link key={to} to={to}
                    className={`p-4 border rounded-xl text-sm font-semibold text-center transition-all ${color}`}>
                    {label}
                  </Link>
                ))}
              </div>
            </div>
          </div>
        )}

        {/* ── Similar Tutors (shown in overview tab below grid) ── */}
        {tab === "overview" && similar.length > 0 && (
          <div className="mt-6">
            <div className="flex items-center justify-between mb-4">
              <h2 className="text-white font-bold text-xl">🤝 Similar Tutors</h2>
              <span className="text-slate-500 text-xs">Tutors with overlapping teaching skills</span>
            </div>
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
              {similar.map((t, i) => (
                <div key={i} className="bg-slate-900 border border-slate-800 hover:border-emerald-500/40 rounded-2xl p-5 transition-all">
                  <div className="flex items-start justify-between mb-3">
                    <div className="w-10 h-10 rounded-full bg-emerald-500/20 flex items-center justify-center text-emerald-400 font-bold text-sm">
                      {t.name?.[0] || "T"}
                    </div>
                    <div className="text-right">
                      {t.badge && (
                        <span className={`text-xs font-bold ${
                          t.badge === "Expert" ? "text-amber-400" : t.badge === "Intermediate" ? "text-blue-400" : "text-emerald-400"
                        }`}>{t.badge}</span>
                      )}
                      {t.similarity_pct && (
                        <p className="text-emerald-400 text-xs mt-0.5">{t.similarity_pct}% match</p>
                      )}
                    </div>
                  </div>
                  <h3 className="text-white font-semibold text-sm">{t.name}</h3>
                  {t.rating > 0 && <p className="text-amber-400 text-xs mt-1">⭐ {t.rating}</p>}
                  <div className="flex flex-wrap gap-1 mt-3">
                    {(t.skills_i_can_teach || []).slice(0, 2).map(s => (
                      <span key={s} className="text-[10px] px-2 py-0.5 bg-slate-800 text-slate-400 rounded capitalize">{s}</span>
                    ))}
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* ── REVIEWS TAB ── */}
        {tab === "reviews" && (
          <div>
            {reviews.length === 0 ? (
              <div className="text-center py-24 text-slate-500">
                <p className="text-5xl mb-4">💬</p>
                <p className="text-lg font-semibold">No reviews yet</p>
                <p className="text-sm mt-1">Complete sessions to start receiving reviews</p>
              </div>
            ) : (
              <div className="space-y-4">
                {/* Summary bar */}
                <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 flex items-center gap-8">
                  <div className="text-center">
                    <p className="text-4xl font-black text-amber-400">
                      {user?.rating ? user.rating.toFixed(1) : "—"}
                    </p>
                    <StarDisplay rating={user?.rating || 0} />
                    <p className="text-slate-400 text-xs mt-1">{reviews.length} reviews</p>
                  </div>
                  <div className="flex-1 space-y-1.5">
                    {[5,4,3,2,1].map(star => {
                      const count = reviews.filter(r => Math.round(r.rating) === star).length;
                      const pct   = reviews.length ? (count / reviews.length) * 100 : 0;
                      return (
                        <div key={star} className="flex items-center gap-2 text-xs text-slate-400">
                          <span className="w-3 text-right">{star}</span>
                          <span className="text-amber-400">★</span>
                          <div className="flex-1 h-1.5 bg-slate-800 rounded-full overflow-hidden">
                            <div className="h-full bg-amber-400 rounded-full" style={{ width: `${pct}%` }} />
                          </div>
                          <span className="w-6 text-right">{count}</span>
                        </div>
                      );
                    })}
                  </div>
                </div>

                {/* Individual reviews */}
                {reviews.map((r, i) => (
                  <div key={i} className="bg-slate-900 border border-slate-800 rounded-2xl p-6">
                    <div className="flex items-start justify-between gap-4">
                      <div className="flex items-center gap-3">
                        <div className="w-9 h-9 rounded-full bg-emerald-500/20 flex items-center justify-center text-emerald-400 font-bold text-sm shrink-0">
                          {r.learner_name?.[0] || "?"}
                        </div>
                        <div>
                          <p className="text-white font-semibold text-sm">{r.learner_name || "Anonymous"}</p>
                          <StarDisplay rating={r.rating} />
                        </div>
                      </div>
                      <div className="text-right">
                        <span className="text-amber-400 font-bold">{r.rating}/5</span>
                        {r.created_at && (
                          <p className="text-slate-500 text-xs mt-0.5">
                            {new Date(r.created_at).toLocaleDateString("en-IN", { day: "numeric", month: "short", year: "numeric" })}
                          </p>
                        )}
                      </div>
                    </div>
                    {r.comment && (
                      <p className="text-slate-300 text-sm leading-relaxed mt-4 pl-12">
                        "{r.comment}"
                      </p>
                    )}
                  </div>
                ))}
              </div>
            )}
          </div>
        )}
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