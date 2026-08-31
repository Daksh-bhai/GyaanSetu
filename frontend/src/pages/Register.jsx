import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { registerUser } from "../api";

const SKILLS_OPTIONS = [
  "python","java","c++","web development","cybersecurity","cloud computing",
  "verbal communication","english grammar","psychology","economics","geography","history","political science"
];

export default function Register() {
  const navigate = useNavigate();
  const [step,    setStep]    = useState(1); // 1 = basic info, 2 = skills
  const [form,    setForm]    = useState({
    name: "", email: "", password: "", role: "learner", location: "",
    skills_i_can_teach: [], skills_i_want_to_learn: []
  });
  const [error,   setError]   = useState("");
  const [loading, setLoading] = useState(false);

  const handle = (e) => setForm({ ...form, [e.target.name]: e.target.value });

  const toggleSkill = (skill, type) => {
    const curr = form[type];
    setForm({
      ...form,
      [type]: curr.includes(skill) ? curr.filter(s => s !== skill) : [...curr, skill]
    });
  };

  const nextStep = (e) => {
    e.preventDefault();
    if (!form.name || !form.email || !form.password || !form.location) {
      setError("All fields required"); return;
    }
    setError("");
    setStep(2);
  };

  const submit = async (e) => {
    e.preventDefault();
    setError("");

    if (form.skills_i_want_to_learn.length === 0) {
      setError("Select at least one skill to learn"); return;
    }
    if (form.role === "tutor" && form.skills_i_can_teach.length === 0) {
      setError("Tutors must select at least one skill to teach"); return;
    }

    setLoading(true);
    try {
      await registerUser(form);
      navigate("/login");
    } catch (err) {
      setError(err.response?.data?.error || "Registration failed");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-slate-950 flex items-center justify-center px-4 py-12">
      <div className="absolute inset-0 overflow-hidden pointer-events-none">
        <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[600px] h-[600px] bg-emerald-500/8 rounded-full blur-3xl" />
      </div>

      <div className="w-full max-w-lg relative z-10">

        {/* Logo */}
        <div className="text-center mb-8">
          <Link to="/" className="inline-flex items-center gap-2.5">
            <div className="w-10 h-10 bg-emerald-500/10 border border-emerald-500/30 rounded-xl flex items-center justify-center">
              <svg width="28" height="28" viewBox="0 0 40 40" fill="none"><rect x="4" y="28" width="32" height="3" rx="1.5" fill="#10b981"/><rect x="7" y="16" width="4" height="12" rx="1" fill="#10b981"/><rect x="29" y="16" width="4" height="12" rx="1" fill="#10b981"/><path d="M11 16 Q20 4 29 16" stroke="#10b981" strokeWidth="2.5" strokeLinecap="round" fill="none"/><line x1="16" y1="9.5" x2="16" y2="28" stroke="#6ee7b7" strokeWidth="1.2" strokeLinecap="round"/><line x1="20" y1="6" x2="20" y2="28" stroke="#6ee7b7" strokeWidth="1.2" strokeLinecap="round"/><line x1="24" y1="9.5" x2="24" y2="28" stroke="#6ee7b7" strokeWidth="1.2" strokeLinecap="round"/><circle cx="20" cy="5.5" r="2" fill="#34d399" opacity="0.9"/></svg>
            </div>
            <div className="leading-none">
              <span className="text-white font-black text-xl">Gyaan<span className="text-emerald-400">Setu</span></span>
              <p className="text-[9px] text-slate-500 font-medium tracking-widest uppercase">Skill Exchange</p>
            </div>
          </Link>
          <h1 className="text-2xl font-black text-white mt-6 mb-1">Create Account</h1>
          <p className="text-slate-400 text-sm">Step {step} of 2</p>
        </div>

        {/* Progress bar */}
        <div className="h-1 bg-slate-800 rounded-full mb-8 overflow-hidden">
          <div
            className="h-full bg-emerald-500 rounded-full transition-all duration-500"
            style={{ width: step === 1 ? "50%" : "100%" }}
          />
        </div>

        <div className="bg-slate-900 border border-slate-800 rounded-2xl p-8">

          {step === 1 && (
            <form onSubmit={nextStep} className="space-y-5">
              <h2 className="text-white font-bold text-lg mb-4">Basic Information</h2>

              <div className="grid grid-cols-2 gap-4">
                <div className="col-span-2">
                  <label className="block text-slate-300 text-sm font-medium mb-2">Full Name</label>
                  <input name="name" value={form.name} onChange={handle} required placeholder="Aisha Khan"
                    className="w-full bg-slate-800 border border-slate-700 text-white rounded-xl px-4 py-3 text-sm focus:outline-none focus:border-emerald-500 transition-colors placeholder-slate-500" />
                </div>

                <div className="col-span-2">
                  <label className="block text-slate-300 text-sm font-medium mb-2">Email</label>
                  <input name="email" type="email" value={form.email} onChange={handle} required placeholder="aisha@gmail.com"
                    className="w-full bg-slate-800 border border-slate-700 text-white rounded-xl px-4 py-3 text-sm focus:outline-none focus:border-emerald-500 transition-colors placeholder-slate-500" />
                </div>

                <div>
                  <label className="block text-slate-300 text-sm font-medium mb-2">Password</label>
                  <input name="password" type="password" value={form.password} onChange={handle} required placeholder="Min 8 chars"
                    className="w-full bg-slate-800 border border-slate-700 text-white rounded-xl px-4 py-3 text-sm focus:outline-none focus:border-emerald-500 transition-colors placeholder-slate-500" />
                </div>

                <div>
                  <label className="block text-slate-300 text-sm font-medium mb-2">Location</label>
                  <input name="location" value={form.location} onChange={handle} required placeholder="Delhi"
                    className="w-full bg-slate-800 border border-slate-700 text-white rounded-xl px-4 py-3 text-sm focus:outline-none focus:border-emerald-500 transition-colors placeholder-slate-500" />
                </div>

                <div className="col-span-2">
                  <label className="block text-slate-300 text-sm font-medium mb-3">I want to join as</label>
                  <div className="grid grid-cols-2 gap-3">
                    {["learner", "tutor"].map(r => (
                      <button
                        key={r} type="button"
                        onClick={() => setForm({ ...form, role: r })}
                        className={`py-3 rounded-xl border text-sm font-semibold capitalize transition-all ${
                          form.role === r
                            ? "border-emerald-500 bg-emerald-500/10 text-emerald-400"
                            : "border-slate-700 text-slate-400 hover:border-slate-500"
                        }`}
                      >
                        {r === "learner" ? "🎓 Learner" : "🧑‍🏫 Tutor"}
                      </button>
                    ))}
                  </div>
                </div>
              </div>

              {error && (
                <div className="bg-red-500/10 border border-red-500/30 text-red-400 text-sm px-4 py-3 rounded-xl">{error}</div>
              )}

              <button type="submit" className="w-full py-3 bg-emerald-500 hover:bg-emerald-400 text-white font-bold rounded-xl transition-all">
                Next: Select Skills →
              </button>
            </form>
          )}

          {step === 2 && (
            <form onSubmit={submit} className="space-y-6">
              <h2 className="text-white font-bold text-lg">Select Your Skills</h2>

              {/* Skills to learn */}
              <div>
                <label className="block text-slate-300 text-sm font-medium mb-3">
                  Skills I want to <span className="text-emerald-400">learn</span> *
                </label>
                <div className="flex flex-wrap gap-2">
                  {SKILLS_OPTIONS.map(s => (
                    <button
                      key={s} type="button"
                      onClick={() => toggleSkill(s, "skills_i_want_to_learn")}
                      className={`px-3 py-1.5 rounded-lg text-xs font-medium border capitalize transition-all ${
                        form.skills_i_want_to_learn.includes(s)
                          ? "border-emerald-500 bg-emerald-500/10 text-emerald-400"
                          : "border-slate-700 text-slate-400 hover:border-slate-500"
                      }`}
                    >
                      {s}
                    </button>
                  ))}
                </div>
              </div>

              {/* Skills to teach (only for tutor) */}
              {form.role === "tutor" && (
                <div>
                  <label className="block text-slate-300 text-sm font-medium mb-3">
                    Skills I can <span className="text-amber-400">teach</span> *
                  </label>
                  <div className="flex flex-wrap gap-2">
                    {SKILLS_OPTIONS.map(s => (
                      <button
                        key={s} type="button"
                        onClick={() => toggleSkill(s, "skills_i_can_teach")}
                        className={`px-3 py-1.5 rounded-lg text-xs font-medium border capitalize transition-all ${
                          form.skills_i_can_teach.includes(s)
                            ? "border-amber-500 bg-amber-500/10 text-amber-400"
                            : "border-slate-700 text-slate-400 hover:border-slate-500"
                        }`}
                      >
                        {s}
                      </button>
                    ))}
                  </div>
                </div>
              )}

              {error && (
                <div className="bg-red-500/10 border border-red-500/30 text-red-400 text-sm px-4 py-3 rounded-xl">{error}</div>
              )}

              <div className="flex gap-3">
                <button
                  type="button" onClick={() => { setStep(1); setError(""); }}
                  className="flex-1 py-3 border border-slate-700 text-slate-300 hover:border-slate-500 font-semibold rounded-xl transition-all"
                >
                  ← Back
                </button>
                <button
                  type="submit" disabled={loading}
                  className="flex-1 py-3 bg-emerald-500 hover:bg-emerald-400 disabled:opacity-50 text-white font-bold rounded-xl transition-all"
                >
                  {loading ? "Creating..." : "Create Account →"}
                </button>
              </div>
            </form>
          )}
        </div>

        <p className="text-center text-slate-400 text-sm mt-6">
          Already have an account?{" "}
          <Link to="/login" className="text-emerald-400 hover:text-emerald-300 font-medium">Login here</Link>
        </p>
      </div>
    </div>
  );
}