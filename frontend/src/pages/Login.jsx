import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { loginUser } from "../api";

export default function Login() {
  const navigate = useNavigate();
  const [form,    setForm]    = useState({ email: "", password: "" });
  const [error,   setError]   = useState("");
  const [loading, setLoading] = useState(false);

  const handle = (e) => setForm({ ...form, [e.target.name]: e.target.value });

  const submit = async (e) => {
    e.preventDefault();
    setError("");
    setLoading(true);
    try {
      const res = await loginUser(form);
      localStorage.setItem("token", res.data.token);
      localStorage.setItem("role",  res.data.role);
      localStorage.setItem("name",  res.data.name);
      localStorage.setItem("email", res.data.email); // ← Added for session role detection
      navigate("/dashboard");
    } catch (err) {
      setError(err.response?.data?.error || "Login failed");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-slate-950 flex items-center justify-center px-4">
      <div className="absolute inset-0 overflow-hidden pointer-events-none">
        <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[500px] h-[500px] bg-emerald-500/8 rounded-full blur-3xl" />
      </div>

      <div className="w-full max-w-md relative z-10">
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
          <h1 className="text-2xl font-black text-white mt-6 mb-1">Welcome back</h1>
          <p className="text-slate-400 text-sm">Login to continue your learning journey</p>
        </div>

        <div className="bg-slate-900 border border-slate-800 rounded-2xl p-8">
          <form onSubmit={submit} className="space-y-5">
            <div>
              <label className="block text-slate-300 text-sm font-medium mb-2">Email</label>
              <input
                name="email" type="email" value={form.email} onChange={handle} required
                placeholder="aisha@gmail.com"
                className="w-full bg-slate-800 border border-slate-700 text-white rounded-xl px-4 py-3 text-sm focus:outline-none focus:border-emerald-500 transition-colors placeholder-slate-500"
              />
            </div>
            <div>
              <label className="block text-slate-300 text-sm font-medium mb-2">Password</label>
              <input
                name="password" type="password" value={form.password} onChange={handle} required
                placeholder="••••••••"
                className="w-full bg-slate-800 border border-slate-700 text-white rounded-xl px-4 py-3 text-sm focus:outline-none focus:border-emerald-500 transition-colors placeholder-slate-500"
              />
            </div>
            {error && (
              <div className="bg-red-500/10 border border-red-500/30 text-red-400 text-sm px-4 py-3 rounded-xl">{error}</div>
            )}
            <button type="submit" disabled={loading}
              className="w-full py-3 bg-emerald-500 hover:bg-emerald-400 disabled:opacity-50 text-white font-bold rounded-xl transition-all hover:shadow-lg hover:shadow-emerald-500/25">
              {loading ? "Logging in..." : "Login →"}
            </button>
          </form>
        </div>

        <p className="text-center text-slate-400 text-sm mt-6">
          Don't have an account?{" "}
          <Link to="/register" className="text-emerald-400 hover:text-emerald-300 font-medium">Register here</Link>
        </p>
      </div>
    </div>
  );
}