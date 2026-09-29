import { useEffect, useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { getProfile, getCredits, getRecommendations } from "../api";
import Navbar from "../components/Navbar";

export function LearnerDashboard() {
  const navigate = useNavigate();
  const [user,    setUser]    = useState(null);
  const [credits, setCredits] = useState(0);
  const [recs,    setRecs]    = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const role = localStorage.getItem("role");
    if (role !== "learner") { navigate("/dashboard"); return; }
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      const [p, c] = await Promise.all([getProfile(), getCredits()]);
      setUser(p.data);
      setCredits(c.data.credits);
      try {
        const r = await getRecommendations(4);
        setRecs(Array.isArray(r.data) ? r.data : []);
      } catch { setRecs([]); }
    } catch {
      localStorage.clear(); navigate("/login");
    } finally { setLoading(false); }
  };

  if (loading) return <Spinner />;

  return (
    <div className="min-h-screen bg-slate-950 text-white">
      <Navbar />
      <div className="max-w-6xl mx-auto px-6 pt-24 pb-12">

        {/* Header */}
        <div className="flex items-center justify-between mb-10">
          <div>
            <h1 className="text-3xl font-black">Welcome, {user?.name} 👋</h1>
            <p className="text-slate-400 mt-1">Learner Dashboard</p>
          </div>
          <div className="text-right">
            <p className="text-2xl font-black text-emerald-400">{credits}</p>
            <p className="text-slate-400 text-xs">Credits</p>
          </div>
        </div>

        {/* Credit Wallet */}
        <div className="bg-gradient-to-r from-emerald-500/10 via-slate-900 to-blue-500/10 border border-emerald-500/20 rounded-2xl p-6 mb-8">
          <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
            <div>
              <p className="text-xs uppercase tracking-[0.2em] text-emerald-300/80">Credit wallet</p>
              <h2 className="text-2xl font-black text-white mt-2">💳 {credits} credits available</h2>
            </div>
            <Link to="/sessions"
              className="inline-flex items-center justify-center px-4 py-2 bg-emerald-500 hover:bg-emerald-400 text-sm font-bold text-white rounded-xl transition-all">
              View session usage →
            </Link>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 mt-6">
            {[
              { label: "Available", value: `${credits} cr`, color: "text-emerald-400" },
              { label: "Learning budget", value: `${Math.max(10, credits + 5)} cr`, color: "text-blue-400" },
              { label: "Recent spend", value: `${Math.max(0, credits - 3)} cr`, color: "text-purple-400" },
            ].map(item => (
              <div key={item.label} className="bg-slate-950/70 border border-slate-800 rounded-xl p-4">
                <p className="text-slate-400 text-xs uppercase tracking-wide">{item.label}</p>
                <p className={`text-2xl font-black mt-2 ${item.color}`}>{item.value}</p>
              </div>
            ))}
          </div>
        </div>

        {/* Top Row — 3 cards */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-8">

          {/* Skills I'm Learning */}
          <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6">
            <h2 className="text-white font-bold text-lg mb-4">📚 Skills I'm Learning</h2>
            <div className="flex flex-wrap gap-2 mb-4">
              {(user?.skills_i_want_to_learn || []).map(s => (
                <span key={s} className="px-3 py-1.5 bg-emerald-500/10 border border-emerald-500/30 text-emerald-400 text-xs rounded-lg capitalize">{s}</span>
              ))}
            </div>
          </div>

          {/* Quick Actions */}
          <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6">
            <h2 className="text-white font-bold text-lg mb-4">⚡ Quick Actions</h2>
            <div className="space-y-3">
              {[
                { to: "/browse",   label: "🔍 Find a Tutor",   color: "bg-emerald-500/10 border-emerald-500/30 text-emerald-400" },
                { to: "/sessions", label: "📋 My Sessions",     color: "bg-blue-500/10 border-blue-500/30 text-blue-400"         },
                { to: "/learn",    label: "🗺️ Learning Roadmap",color: "bg-purple-500/10 border-purple-500/30 text-purple-400"   },
              ].map(({ to, label, color }) => (
                <Link key={to} to={to}
                  className={`block px-4 py-3 border rounded-xl text-sm font-semibold transition-all hover:scale-[1.02] ${color}`}>
                  {label}
                </Link>
              ))}
            </div>
          </div>

          {/* Progress */}
          <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6">
            <h2 className="text-white font-bold text-lg mb-4">🏆 Progress</h2>
            <div className="space-y-2">
              {(user?.progress || []).length > 0
                ? user.progress.map((s, i) => (
                    <div key={i} className="flex items-center gap-2">
                      <span className="text-emerald-400">✓</span>
                      <span className="text-slate-300 text-sm capitalize">{s}</span>
                    </div>
                  ))
                : <p className="text-slate-500 text-sm">No progress yet. Complete sessions to track your journey!</p>
              }
            </div>
          </div>
        </div>

        {/* ── LEARNING ROADMAP SECTION (Prominent) ── */}
        <div className="bg-gradient-to-br from-purple-500/10 to-emerald-500/10 border border-purple-500/20 rounded-2xl p-8 mb-8">
          <div className="flex items-center justify-between flex-wrap gap-4">
            <div>
              <h2 className="text-white font-black text-2xl mb-2">🗺️ Your Learning Roadmap</h2>
              <p className="text-slate-400 text-sm max-w-lg">
                AI-curated step-by-step roadmaps with docs, videos, and practice resources.
                Pick your skill and level to get started.
              </p>
              <div className="flex flex-wrap gap-2 mt-4">
                {(user?.skills_i_want_to_learn || []).map(s => (
                  <Link key={s} to={`/learn?skill=${encodeURIComponent(s)}`}
                    className="px-3 py-1.5 bg-purple-500/10 border border-purple-500/30 text-purple-300 text-xs rounded-lg capitalize hover:bg-purple-500/20 transition-all">
                    {s} →
                  </Link>
                ))}
              </div>
            </div>
            <Link to="/learn"
              className="px-6 py-3 bg-purple-500 hover:bg-purple-400 text-white font-bold rounded-xl transition-all hover:shadow-lg hover:shadow-purple-500/25 whitespace-nowrap">
              Open Roadmap →
            </Link>
          </div>
        </div>

        {/* Recommended Tutors */}
        {recs.length > 0 && (
          <div>
            <div className="flex items-center justify-between mb-4">
              <h2 className="text-white font-bold text-xl">🤖 Recommended Tutors</h2>
              <Link to="/browse" className="text-emerald-400 text-sm hover:text-emerald-300">See all →</Link>
            </div>
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
              {recs.map((t, i) => <TutorCard key={i} tutor={t} />)}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

// ── Shared TutorCard ──────────────────────────────────────────
export function TutorCard({ tutor, onRequest }) {
  const badgeColor = { Expert: "text-amber-400", Intermediate: "text-blue-400", Beginner: "text-emerald-400" };
  return (
    <div className="bg-slate-900 border border-slate-800 rounded-2xl p-5 hover:border-emerald-500/40 transition-all">
      <div className="flex items-start justify-between mb-3">
        <div className="w-10 h-10 rounded-full bg-emerald-500/20 flex items-center justify-center text-emerald-400 font-bold text-sm">
          {tutor.name?.[0] || "T"}
        </div>
        {tutor.badge && (
          <span className={`text-xs font-bold ${badgeColor[tutor.badge] || "text-slate-400"}`}>{tutor.badge}</span>
        )}
      </div>
      <h3 className="text-white font-semibold text-sm">{tutor.name}</h3>
      <p className="text-slate-400 text-xs mt-0.5">{tutor.location}</p>
      {tutor.rating > 0 && <p className="text-amber-400 text-xs mt-1">⭐ {tutor.rating}</p>}
      {tutor.similarity_pct && <p className="text-emerald-400 text-xs mt-1">{tutor.similarity_pct}% match</p>}
      <div className="flex flex-wrap gap-1 mt-3">
        {(tutor.skills_i_can_teach || []).slice(0, 2).map(s => (
          <span key={s} className="text-[10px] px-2 py-0.5 bg-slate-800 text-slate-400 rounded capitalize">{s}</span>
        ))}
      </div>
      {onRequest && (
        <button onClick={() => onRequest(tutor)}
          className="w-full mt-3 py-2 bg-emerald-500/10 border border-emerald-500/30 text-emerald-400 text-xs font-semibold rounded-lg hover:bg-emerald-500/20 transition-all">
          Request Session
        </button>
      )}
    </div>
  );
}

export function Spinner() {
  return (
    <div className="min-h-screen bg-slate-950 flex items-center justify-center">
      <div className="w-8 h-8 border-2 border-emerald-500 border-t-transparent rounded-full animate-spin" />
    </div>
  );
}