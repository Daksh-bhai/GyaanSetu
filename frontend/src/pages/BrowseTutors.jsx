import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { getTutors, sendRequest } from "../api";
import Navbar from "../components/Navbar";

const DURATIONS = [30, 60, 120, 180];

export default function BrowseTutors() {
  const navigate  = useNavigate();
  const [tutors,  setTutors]  = useState([]);
  const [search,  setSearch]  = useState("");
  const [loading, setLoading] = useState(true);

  // Request modal
  const [modal,    setModal]    = useState(null);
  const [skill,    setSkill]    = useState("");
  const [duration, setDuration] = useState(60);
  const [sending,  setSending]  = useState(false);
  const [msg,      setMsg]      = useState("");

  useEffect(() => {
    getTutors()
      .then(r => setTutors(r.data.filter(t => t.is_verified)))
      .catch(() => { localStorage.clear(); navigate("/login"); })
      .finally(() => setLoading(false));
  }, []);

  const filtered = tutors.filter(t =>
    !search ||
    t.name?.toLowerCase().includes(search.toLowerCase()) ||
    t.skills_i_can_teach?.some(s => s.toLowerCase().includes(search.toLowerCase()))
  );

  const openRequest = (tutor) => {
    setModal(tutor);
    setSkill(tutor.skills_i_can_teach?.[0] || "");
    setMsg("");
  };

  const submitRequest = async () => {
    if (!skill) { setMsg("Select a skill"); return; }
    setSending(true);
    try {
      await sendRequest(modal.email, { skill, duration });
      setMsg("✅ Request sent!");
      setTimeout(() => { setModal(null); navigate("/sessions"); }, 1500);
    } catch (e) {
      setMsg(e.response?.data?.error || "Failed to send request");
    } finally { setSending(false); }
  };

  const badgeColor = { Expert: "text-amber-400", Intermediate: "text-blue-400", Beginner: "text-emerald-400" };

  if (loading) return (
    <div className="min-h-screen bg-slate-950 flex items-center justify-center">
      <div className="w-8 h-8 border-2 border-emerald-500 border-t-transparent rounded-full animate-spin" />
    </div>
  );

  return (
    <div className="min-h-screen bg-slate-950 text-white">
      <Navbar />
      <div className="max-w-6xl mx-auto px-6 pt-24 pb-12">

        <div className="mb-8">
          <h1 className="text-3xl font-black mb-1">Find Tutors</h1>
          <p className="text-slate-400">{filtered.length} verified tutors available</p>
        </div>

        {/* Search */}
        <div className="relative mb-8">
          <input
            value={search}
            onChange={e => setSearch(e.target.value)}
            placeholder="Search by name or skill..."
            className="w-full bg-slate-900 border border-slate-700 text-white rounded-2xl px-5 py-4 pr-12 focus:outline-none focus:border-emerald-500 transition-colors placeholder-slate-500"
          />
          <span className="absolute right-5 top-1/2 -translate-y-1/2 text-slate-500">🔍</span>
        </div>

        {/* Grid */}
        {filtered.length === 0 ? (
          <div className="text-center py-24 text-slate-500">
            <p className="text-5xl mb-4">🔍</p>
            <p className="text-lg font-semibold">No tutors found</p>
            <p className="text-sm mt-1">Try a different search term</p>
          </div>
        ) : (
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
            {filtered.map((tutor, i) => (
              <div key={i} className="bg-slate-900 border border-slate-800 hover:border-emerald-500/40 rounded-2xl p-6 transition-all group">

                {/* Header */}
                <div className="flex items-start justify-between mb-4">
                  <div className="w-12 h-12 rounded-full bg-gradient-to-br from-emerald-500/30 to-teal-500/30 flex items-center justify-center text-emerald-400 font-black text-lg">
                    {tutor.name?.[0] || "T"}
                  </div>
                  <div className="text-right">
                    {tutor.badge && (
                      <p className={`text-xs font-bold ${badgeColor[tutor.badge] || "text-slate-400"}`}>{tutor.badge}</p>
                    )}
                    {tutor.rating > 0 && (
                      <p className="text-amber-400 text-xs mt-0.5">⭐ {tutor.rating} ({tutor.rating_count})</p>
                    )}
                  </div>
                </div>

                <h3 className="text-white font-bold text-lg mb-0.5">{tutor.name}</h3>
                <p className="text-slate-500 text-xs mb-1">📍 {tutor.location}</p>
                {tutor.sessions_completed > 0 && (
                  <p className="text-slate-500 text-xs mb-3">✅ {tutor.sessions_completed} sessions</p>
                )}

                {/* Bio */}
                {tutor.bio && (
                  <p className="text-slate-400 text-sm mb-4 leading-relaxed line-clamp-2">{tutor.bio}</p>
                )}

                {/* Skills */}
                <div className="flex flex-wrap gap-1.5 mb-5">
                  {(tutor.skills_i_can_teach || []).map(s => (
                    <span key={s} className="text-[10px] px-2.5 py-1 bg-emerald-500/10 border border-emerald-500/20 text-emerald-400 rounded-lg capitalize">{s}</span>
                  ))}
                </div>

                <button
                  onClick={() => openRequest(tutor)}
                  className="w-full py-2.5 bg-emerald-500/10 border border-emerald-500/30 text-emerald-400 text-sm font-bold rounded-xl hover:bg-emerald-500/20 group-hover:border-emerald-500/60 transition-all"
                >
                  Request Session →
                </button>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Request Modal */}
      {modal && (
        <div className="fixed inset-0 bg-black/70 backdrop-blur-sm flex items-center justify-center z-50 px-4">
          <div className="bg-slate-900 border border-slate-700 rounded-2xl p-8 max-w-md w-full">
            <h3 className="text-white font-black text-xl mb-1">Request Session</h3>
            <p className="text-slate-400 text-sm mb-6">with <span className="text-emerald-400">{modal.name}</span></p>

            <div className="space-y-5">
              <div>
                <label className="block text-slate-300 text-sm font-medium mb-2">Skill</label>
                <select
                  value={skill}
                  onChange={e => setSkill(e.target.value)}
                  className="w-full bg-slate-800 border border-slate-700 text-white rounded-xl px-4 py-3 text-sm focus:outline-none focus:border-emerald-500"
                >
                  {(modal.skills_i_can_teach || []).map(s => (
                    <option key={s} value={s} className="capitalize">{s}</option>
                  ))}
                </select>
              </div>

              <div>
                <label className="block text-slate-300 text-sm font-medium mb-2">Duration</label>
                <div className="grid grid-cols-4 gap-2">
                  {DURATIONS.map(d => (
                    <button
                      key={d} type="button"
                      onClick={() => setDuration(d)}
                      className={`py-2.5 rounded-xl text-sm font-semibold border transition-all ${
                        duration === d
                          ? "border-emerald-500 bg-emerald-500/10 text-emerald-400"
                          : "border-slate-700 text-slate-400 hover:border-slate-500"
                      }`}
                    >
                      {d}m
                    </button>
                  ))}
                </div>
                <p className="text-slate-500 text-xs mt-2">Cost: {duration / 60} credit(s)</p>
              </div>

              {msg && (
                <p className={`text-sm px-4 py-3 rounded-xl border ${
                  msg.startsWith("✅")
                    ? "bg-emerald-500/10 border-emerald-500/30 text-emerald-400"
                    : "bg-red-500/10 border-red-500/30 text-red-400"
                }`}>{msg}</p>
              )}

              <div className="flex gap-3">
                <button onClick={() => setModal(null)}
                  className="flex-1 py-3 border border-slate-700 text-slate-400 rounded-xl text-sm font-semibold hover:border-slate-500 transition-all">
                  Cancel
                </button>
                <button onClick={submitRequest} disabled={sending}
                  className="flex-1 py-3 bg-emerald-500 hover:bg-emerald-400 disabled:opacity-50 text-white rounded-xl text-sm font-bold transition-all">
                  {sending ? "Sending..." : "Send Request →"}
                </button>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
