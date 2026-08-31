// ================================================================
// SMART MATCH (Tutor view)
// ================================================================
import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { getSmartMatch, sendRequest } from "../api";
import Navbar from "../components/Navbar";
import { getRoadmap, getSkillsList } from "../api";
import { startTest, submitTest, testStatus as getTestStatus } from "../api";

const DURATIONS = [30, 60, 120, 180];

export function SmartMatch() {
  const navigate = useNavigate();
  const [matches, setMatches] = useState([]);
  const [loading, setLoading] = useState(true);
  const [modal,   setModal]   = useState(null);
  const [skill,   setSkill]   = useState("");
  const [dur,     setDur]     = useState(60);
  const [msg,     setMsg]     = useState("");
  const [sending, setSending] = useState(false);

  useEffect(() => {
    getSmartMatch(20)
      .then(r => setMatches(Array.isArray(r.data) ? r.data : []))
      .catch(e => {
        if (e.response?.status === 401) { localStorage.clear(); navigate("/login"); }
      })
      .finally(() => setLoading(false));
  }, []);

  const submitRequest = async () => {
    setSending(true);
    try {
      await sendRequest(modal.email, { skill, duration: dur });
      setMsg("✅ Request sent!"); setSending(false);
      setTimeout(() => { setModal(null); navigate("/sessions"); }, 1500);
    } catch (e) {
      setMsg(e.response?.data?.error || "Failed"); setSending(false);
    }
  };

  const badgeColor = { Expert: "text-amber-400", Intermediate: "text-blue-400", Beginner: "text-emerald-400" };

  if (loading) return <Loader />;

  return (
    <div className="min-h-screen bg-slate-950 text-white">
      <Navbar />
      <div className="max-w-6xl mx-auto px-6 pt-24 pb-12">
        <div className="mb-8">
          <h1 className="text-3xl font-black">🎯 Smart Match</h1>
          <p className="text-slate-400 mt-1">AI-powered mutual skill exchange partners</p>
        </div>

        {matches.length === 0 ? (
          <div className="text-center py-24 text-slate-500">
            <p className="text-5xl mb-4">🤖</p>
            <p className="text-lg font-semibold">No matches found</p>
            <p className="text-sm mt-1">Make sure you have skills to learn and teach set in your profile.</p>
          </div>
        ) : (
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
            {matches.map((t, i) => (
              <div key={i}
                className={`bg-slate-900 rounded-2xl p-6 border transition-all hover:scale-[1.01] ${
                  t.match_type === "mutual"
                    ? "border-emerald-500/50 ring-1 ring-emerald-500/20"
                    : "border-slate-800"
                }`}>

                {t.match_type === "mutual" && (
                  <div className="text-[10px] bg-emerald-500/10 border border-emerald-500/30 text-emerald-400 font-bold px-2 py-0.5 rounded-full inline-block mb-3">
                    🔥 MUTUAL MATCH
                  </div>
                )}

                <div className="flex items-start justify-between mb-3">
                  <div className="w-11 h-11 rounded-full bg-gradient-to-br from-emerald-500/20 to-teal-500/20 flex items-center justify-center text-emerald-400 font-black">
                    {t.name?.[0]}
                  </div>
                  <div className="text-right">
                    {t.badge && <p className={`text-xs font-bold ${badgeColor[t.badge]}`}>{t.badge}</p>}
                    {t.score && <p className="text-slate-500 text-xs">Score: {t.score}</p>}
                    {t.rank  && <p className="text-slate-500 text-xs">#{t.rank}</p>}
                  </div>
                </div>

                <h3 className="text-white font-bold">{t.name}</h3>
                <p className="text-slate-500 text-xs mb-3">📍 {t.location}</p>
                {t.rating > 0 && <p className="text-amber-400 text-xs mb-3">⭐ {t.rating}</p>}

                <div className="flex flex-wrap gap-1 mb-4">
                  {(t.skills_i_can_teach || []).slice(0, 3).map(s => (
                    <span key={s} className="text-[10px] px-2 py-0.5 bg-emerald-500/10 border border-emerald-500/20 text-emerald-400 rounded capitalize">{s}</span>
                  ))}
                </div>

                <button onClick={() => { setModal(t); setSkill(t.skills_i_can_teach?.[0] || ""); setMsg(""); }}
                  className="w-full py-2 bg-emerald-500/10 border border-emerald-500/30 text-emerald-400 text-xs font-bold rounded-xl hover:bg-emerald-500/20 transition-all">
                  Request Session →
                </button>
              </div>
            ))}
          </div>
        )}
      </div>

      {modal && (
        <div className="fixed inset-0 bg-black/70 backdrop-blur-sm flex items-center justify-center z-50 px-4">
          <div className="bg-slate-900 border border-slate-700 rounded-2xl p-8 max-w-md w-full">
            <h3 className="text-white font-black text-xl mb-1">Request Session</h3>
            <p className="text-slate-400 text-sm mb-6">with <span className="text-emerald-400">{modal.name}</span></p>
            <div className="space-y-4">
              <div>
                <label className="text-slate-300 text-sm font-medium mb-2 block">Skill</label>
                <select value={skill} onChange={e => setSkill(e.target.value)}
                  className="w-full bg-slate-800 border border-slate-700 text-white rounded-xl px-4 py-3 text-sm focus:outline-none focus:border-emerald-500">
                  {(modal.skills_i_can_teach || []).map(s => <option key={s} value={s}>{s}</option>)}
                </select>
              </div>
              <div>
                <label className="text-slate-300 text-sm font-medium mb-2 block">Duration</label>
                <div className="grid grid-cols-4 gap-2">
                  {DURATIONS.map(d => (
                    <button key={d} onClick={() => setDur(d)}
                      className={`py-2.5 rounded-xl text-sm font-semibold border transition-all ${dur === d ? "border-emerald-500 bg-emerald-500/10 text-emerald-400" : "border-slate-700 text-slate-400"}`}>
                      {d}m
                    </button>
                  ))}
                </div>
                <p className="text-slate-500 text-xs mt-1">Cost: {dur / 60} credit(s)</p>
              </div>
              {msg && <p className="text-sm text-emerald-400">{msg}</p>}
              <div className="flex gap-3">
                <button onClick={() => setModal(null)} className="flex-1 py-3 border border-slate-700 text-slate-400 rounded-xl text-sm hover:border-slate-500 transition-all">Cancel</button>
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


// ================================================================
// LEARNING ROADMAP PAGE
// ================================================================


export function Roadmap() {
  const navigate = useNavigate();
  const [skills,   setSkills]   = useState([]);
  const [skill,    setSkill]    = useState("");
  const [level,    setLevel]    = useState("beginner");
  const [roadmap,  setRoadmap]  = useState(null);
  const [loading,  setLoading]  = useState(false);
  const [error,    setError]    = useState("");

  useEffect(() => {
    getSkillsList().then(r => setSkills(r.data.skills || []));
  }, []);

  const fetch = async () => {
    if (!skill) { setError("Select a skill"); return; }
    setLoading(true); setError(""); setRoadmap(null);
    try {
      const r = await getRoadmap(skill, level);
      setRoadmap(r.data);
    } catch (e) {
      setError(e.response?.data?.error || "Not found");
    } finally { setLoading(false); }
  };

  const LEVELS = ["beginner", "intermediate", "expert"];
  const levelColor = { beginner: "emerald", intermediate: "blue", expert: "amber" };

  return (
    <div className="min-h-screen bg-slate-950 text-white">
      <Navbar />
      <div className="max-w-4xl mx-auto px-6 pt-24 pb-12">
        <div className="mb-8">
          <h1 className="text-3xl font-black">📚 Learning Roadmap</h1>
          <p className="text-slate-400 mt-1">AI-curated roadmaps with docs & videos</p>
        </div>

        {/* Controls */}
        <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 mb-8">
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
            <div className="sm:col-span-2">
              <label className="text-slate-300 text-sm font-medium mb-2 block">Choose Skill</label>
              <select value={skill} onChange={e => setSkill(e.target.value)}
                className="w-full bg-slate-800 border border-slate-700 text-white rounded-xl px-4 py-3 text-sm focus:outline-none focus:border-emerald-500 capitalize">
                <option value="">-- Select Skill --</option>
                {skills.map(s => <option key={s} value={s} className="capitalize">{s}</option>)}
              </select>
            </div>
            <div>
              <label className="text-slate-300 text-sm font-medium mb-2 block">Level</label>
              <select value={level} onChange={e => setLevel(e.target.value)}
                className="w-full bg-slate-800 border border-slate-700 text-white rounded-xl px-4 py-3 text-sm focus:outline-none focus:border-emerald-500 capitalize">
                {LEVELS.map(l => <option key={l} value={l} className="capitalize">{l}</option>)}
              </select>
            </div>
          </div>
          {error && <p className="text-red-400 text-sm mt-3">{error}</p>}
          <button onClick={fetch} disabled={loading}
            className="mt-4 w-full py-3 bg-emerald-500 hover:bg-emerald-400 disabled:opacity-50 text-white font-bold rounded-xl transition-all">
            {loading ? "Loading..." : "Get Roadmap →"}
          </button>
        </div>

        {/* Roadmap Result */}
        {roadmap && (
          <div className="space-y-6">
            <div>
              <h2 className="text-2xl font-black text-white">{roadmap.skill}</h2>
              <p className="text-slate-400 mt-1">{roadmap.description}</p>
              <div className="flex items-center gap-4 mt-3">
                <span className="text-emerald-400 text-sm font-semibold capitalize">📊 {roadmap.level}</span>
                <span className="text-slate-400 text-sm">⏱️ {roadmap.duration}</span>
                <span className="text-slate-400 text-sm">📋 {roadmap.total_steps} steps</span>
              </div>
            </div>

            {/* Steps */}
            <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6">
              <h3 className="text-white font-bold text-lg mb-5">🗺️ Learning Path</h3>
              <div className="space-y-3">
                {roadmap.roadmap?.map((step, i) => (
                  <div key={i} className="flex items-start gap-4">
                    <div className="w-7 h-7 rounded-full bg-emerald-500/10 border border-emerald-500/30 flex items-center justify-center shrink-0 mt-0.5">
                      <span className="text-emerald-400 text-xs font-bold">{i + 1}</span>
                    </div>
                    <p className="text-slate-300 text-sm leading-relaxed">{step}</p>
                  </div>
                ))}
              </div>
            </div>

            {/* Resources */}
            <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6">
              <h3 className="text-white font-bold text-lg mb-5">📖 Resources</h3>
              <div className="space-y-3">
                {roadmap.resources?.map((r, i) => {
                  const icon = { docs: "📄", video: "🎥", practice: "💻" }[r.type] || "🔗";
                  return (
                    <a key={i} href={r.url} target="_blank" rel="noreferrer"
                      className="flex items-center gap-3 p-3 bg-slate-800 hover:bg-slate-700 border border-slate-700 hover:border-emerald-500/40 rounded-xl transition-all group">
                      <span className="text-lg">{icon}</span>
                      <div className="flex-1 min-w-0">
                        <p className="text-white text-sm font-medium group-hover:text-emerald-400 transition-colors truncate">{r.title}</p>
                        <p className="text-slate-500 text-xs capitalize">{r.type}</p>
                      </div>
                      <span className="text-slate-500 group-hover:text-emerald-400 transition-colors">↗</span>
                    </a>
                  );
                })}
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}


// ================================================================
// SKILL VERIFICATION TEST PAGE
// ================================================================


export function VerifySkill() {
  const navigate = useNavigate();
  const [phase,     setPhase]     = useState("form");   // form | test | result
  const [form,      setForm]      = useState({ domain: "IT", field: "Python", level: "beginner" });
  const [questions, setQuestions] = useState([]);
  const [answers,   setAnswers]   = useState([]);
  const [result,    setResult]    = useState(null);
  const [tStatus,   setTStatus]   = useState(null);
  const [loading,   setLoading]   = useState(false);
  const [error,     setError]     = useState("");

  const DOMAINS = { IT: ["Python", "Java", "C++", "Web Development", "Cybersecurity", "Cloud Computing"],
                    Communication: ["Verbal Communication", "English Grammar", "Psychology"],
                    "Social Science": ["Geography", "History", "Political Science", "Economics"] };
  const LEVELS = ["beginner", "intermediate", "expert"];

  useEffect(() => {
    getTestStatus().then(r => setTStatus(r.data)).catch(() => {});
  }, []);

  const begin = async () => {
    setLoading(true); setError("");
    try {
      const r = await startTest({ domain: form.domain, field: form.field, level: form.level });
      setQuestions(r.data.questions);
      setAnswers(new Array(r.data.questions.length).fill(""));
      setPhase("test");
    } catch (e) { setError(e.response?.data?.error || "Failed to start"); }
    finally { setLoading(false); }
  };

  const submit = async () => {
    if (answers.some(a => !a)) { setError("Please answer all questions"); return; }
    setLoading(true); setError("");
    try {
      const r = await submitTest({ answers, field: form.field, level: form.level });
      setResult(r.data);
      setPhase("result");
      if (r.data.result === "PASS") {
        localStorage.setItem("role", "tutor");
      }
    } catch (e) { setError(e.response?.data?.error || "Submission failed"); }
    finally { setLoading(false); }
  };

  return (
    <div className="min-h-screen bg-slate-950 text-white">
      <Navbar />
      <div className="max-w-3xl mx-auto px-6 pt-24 pb-12">

        {phase === "form" && (
          <div>
            <h1 className="text-3xl font-black mb-2">✅ Skill Verification</h1>
            <p className="text-slate-400 mb-8">Pass the test to become a verified tutor and earn 5 bonus credits.</p>

            {tStatus && (
              <div className="bg-slate-900 border border-slate-800 rounded-2xl p-5 mb-6 text-sm">
                <div className="flex items-center justify-between">
                  <span className="text-slate-400">Attempts</span>
                  <span className="text-white font-semibold">{tStatus.attempts_used}/{tStatus.max_attempts}</span>
                </div>
                {tStatus.cooldown_active && (
                  <p className="text-amber-400 mt-2">⏳ Cooldown active — wait {tStatus.wait_minutes} minutes</p>
                )}
                {tStatus.is_verified && (
                  <p className="text-emerald-400 mt-2">✅ Already verified: {tStatus.verified_skill} ({tStatus.verified_level})</p>
                )}
              </div>
            )}

            <div className="bg-slate-900 border border-slate-800 rounded-2xl p-8 space-y-5">
              <div>
                <label className="text-slate-300 text-sm font-medium mb-2 block">Domain</label>
                <select value={form.domain} onChange={e => setForm({ ...form, domain: e.target.value, field: Object.values(DOMAINS)[Object.keys(DOMAINS).indexOf(e.target.value)]?.[0] || "" })}
                  className="w-full bg-slate-800 border border-slate-700 text-white rounded-xl px-4 py-3 text-sm focus:outline-none focus:border-emerald-500">
                  {Object.keys(DOMAINS).map(d => <option key={d}>{d}</option>)}
                </select>
              </div>
              <div>
                <label className="text-slate-300 text-sm font-medium mb-2 block">Field / Skill</label>
                <select value={form.field} onChange={e => setForm({ ...form, field: e.target.value })}
                  className="w-full bg-slate-800 border border-slate-700 text-white rounded-xl px-4 py-3 text-sm focus:outline-none focus:border-emerald-500">
                  {(DOMAINS[form.domain] || []).map(f => <option key={f}>{f}</option>)}
                </select>
              </div>
              <div>
                <label className="text-slate-300 text-sm font-medium mb-2 block">Level</label>
                <div className="grid grid-cols-3 gap-3">
                  {LEVELS.map(l => (
                    <button key={l} onClick={() => setForm({ ...form, level: l })}
                      className={`py-2.5 rounded-xl border text-sm font-semibold capitalize transition-all ${form.level === l ? "border-emerald-500 bg-emerald-500/10 text-emerald-400" : "border-slate-700 text-slate-400"}`}>
                      {l}
                    </button>
                  ))}
                </div>
              </div>
              {error && <p className="text-red-400 text-sm">{error}</p>}
              <button onClick={begin} disabled={loading}
                className="w-full py-3 bg-emerald-500 hover:bg-emerald-400 disabled:opacity-50 text-white font-bold rounded-xl transition-all">
                {loading ? "Starting..." : "Start Test →"}
              </button>
            </div>
          </div>
        )}

        {phase === "test" && (
          <div>
            <h1 className="text-3xl font-black mb-2">📝 {form.field} Test</h1>
            <p className="text-slate-400 mb-8">Answer all {questions.length} questions. Score 7/10 to pass.</p>

            <div className="space-y-6">
              {questions.map((q, qi) => (
                <div key={qi} className="bg-slate-900 border border-slate-800 rounded-2xl p-6">
                  <p className="text-white font-semibold mb-4">Q{qi + 1}. {q.question}</p>
                  <div className="space-y-2">
                    {q.options.map((opt, oi) => {
                      const letter = ["A","B","C","D"][oi];
                      return (
                        <button key={oi} onClick={() => {
                          const a = [...answers]; a[qi] = letter; setAnswers(a);
                        }}
                          className={`w-full text-left px-4 py-3 rounded-xl border text-sm transition-all ${answers[qi] === letter ? "border-emerald-500 bg-emerald-500/10 text-emerald-400" : "border-slate-700 text-slate-300 hover:border-slate-500"}`}>
                          <span className="font-bold mr-2">{letter}.</span>{opt}
                        </button>
                      );
                    })}
                  </div>
                </div>
              ))}
            </div>

            {error && <p className="text-red-400 text-sm mt-4">{error}</p>}
            <button onClick={submit} disabled={loading}
              className="w-full mt-8 py-4 bg-emerald-500 hover:bg-emerald-400 disabled:opacity-50 text-white font-black text-lg rounded-2xl transition-all">
              {loading ? "Submitting..." : "Submit Answers →"}
            </button>
          </div>
        )}

        {phase === "result" && result && (
          <div className="text-center py-12">
            <div className={`text-7xl mb-6 ${result.result === "PASS" ? "animate-bounce" : ""}`}>
              {result.result === "PASS" ? "🎉" : "😔"}
            </div>
            <h1 className={`text-4xl font-black mb-2 ${result.result === "PASS" ? "text-emerald-400" : "text-red-400"}`}>
              {result.result}
            </h1>
            <p className="text-2xl text-white font-bold mb-2">{result.score}/{result.total}</p>
            <p className="text-slate-400 mb-6">{result.message}</p>
            {result.credits_awarded > 0 && (
              <div className="inline-block px-6 py-3 bg-emerald-500/10 border border-emerald-500/30 text-emerald-400 rounded-xl mb-6">
                🎁 +{result.credits_awarded} bonus credits awarded!
              </div>
            )}
            {result.suggestion && <p className="text-amber-400 text-sm mb-8">💡 {result.suggestion}</p>}
            <div className="flex gap-4 justify-center">
              {result.result === "FAIL" && (
                <button onClick={() => { setPhase("form"); setResult(null); setError(""); }}
                  className="px-6 py-3 border border-slate-700 text-slate-300 rounded-xl font-semibold hover:border-slate-500 transition-all">
                  Try Again
                </button>
              )}
              <button onClick={() => navigate("/dashboard")}
                className="px-6 py-3 bg-emerald-500 hover:bg-emerald-400 text-white rounded-xl font-bold transition-all">
                Go to Dashboard →
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

function Loader() {
  return (
    <div className="min-h-screen bg-slate-950 flex items-center justify-center">
      <div className="w-8 h-8 border-2 border-emerald-500 border-t-transparent rounded-full animate-spin" />
    </div>
  );
}
