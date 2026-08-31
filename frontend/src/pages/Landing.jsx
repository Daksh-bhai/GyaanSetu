import { Link } from "react-router-dom";
import { useEffect, useState } from "react";
import { useTheme } from "../ThemeContext";

function SunIcon() {
  return (
    <svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <circle cx="12" cy="12" r="5" />
      <line x1="12" y1="1" x2="12" y2="3" /><line x1="12" y1="21" x2="12" y2="23" />
      <line x1="4.22" y1="4.22" x2="5.64" y2="5.64" /><line x1="18.36" y1="18.36" x2="19.78" y2="19.78" />
      <line x1="1" y1="12" x2="3" y2="12" /><line x1="21" y1="12" x2="23" y2="12" />
      <line x1="4.22" y1="19.78" x2="5.64" y2="18.36" /><line x1="18.36" y1="5.64" x2="19.78" y2="4.22" />
    </svg>
  );
}
function MoonIcon() {
  return (
    <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z" />
    </svg>
  );
}
function GyanSetuLogo({ size = 28 }) {
  return (
    <svg width={size} height={size} viewBox="0 0 40 40" fill="none" xmlns="http://www.w3.org/2000/svg">
      <rect x="4" y="28" width="32" height="3" rx="1.5" fill="#10b981" />
      <rect x="7" y="16" width="4" height="12" rx="1" fill="#10b981" />
      <rect x="29" y="16" width="4" height="12" rx="1" fill="#10b981" />
      <path d="M11 16 Q20 4 29 16" stroke="#10b981" strokeWidth="2.5" strokeLinecap="round" fill="none" />
      <line x1="16" y1="9.5" x2="16" y2="28" stroke="#6ee7b7" strokeWidth="1.2" strokeLinecap="round" />
      <line x1="20" y1="6"   x2="20" y2="28" stroke="#6ee7b7" strokeWidth="1.2" strokeLinecap="round" />
      <line x1="24" y1="9.5" x2="24" y2="28" stroke="#6ee7b7" strokeWidth="1.2" strokeLinecap="round" />
      <circle cx="20" cy="5.5" r="2" fill="#34d399" opacity="0.9" />
    </svg>
  );
}

const features = [
  { icon: "🎓", title: "Skill Verification", desc: "AI-powered tests verify tutor expertise before teaching" },
  { icon: "🤝", title: "Smart Matching",     desc: "ML algorithm finds your perfect skill exchange partner" },
  { icon: "💰", title: "Credit Economy",     desc: "Teach to earn, spend to learn — fair barter system" },
  { icon: "⭐", title: "Trust System",       desc: "Ratings, badges & fraud detection keep platform safe" },
  { icon: "📚", title: "Learning Roadmaps",  desc: "AI-curated roadmaps with docs & video resources" },
  { icon: "🛡️", title: "Fraud Detection",    desc: "Real-time ML models detect and block suspicious activity" },
];

const skills = ["Python", "Web Dev", "Java", "C++", "Psychology", "Economics", "Cybersecurity", "Cloud", "History"];

export default function Landing() {
  const [tick, setTick] = useState(0);
  const isLogged = !!localStorage.getItem("token");
  const { theme, toggle } = useTheme();

  useEffect(() => {
    const t = setInterval(() => setTick(p => p + 1), 2000);
    return () => clearInterval(t);
  }, []);

  return (
    <div className="min-h-screen bg-slate-950 text-white overflow-x-hidden">

      {/* ── NAV ── */}
      <nav className="fixed top-0 left-0 right-0 z-50 bg-slate-950/80 backdrop-blur border-b border-slate-800">
        <div className="max-w-6xl mx-auto px-6 h-16 flex items-center justify-between">
          <div className="flex items-center gap-2.5">
            <div className="w-9 h-9 bg-emerald-500/10 border border-emerald-500/30 rounded-xl flex items-center justify-center">
              <GyanSetuLogo size={26} />
            </div>
            <div className="leading-none">
              <span className="font-black text-lg text-white">Gyaan<span className="text-emerald-400">Setu</span></span>
              <p className="text-[9px] text-slate-500 font-medium tracking-widest uppercase">Skill Exchange</p>
            </div>
          </div>
          <div className="flex items-center gap-3">
            <button onClick={toggle}
              className={`w-9 h-9 rounded-xl border flex items-center justify-center transition-all ${
                theme === "dark"
                  ? "border-slate-600 text-amber-400 hover:bg-slate-800"
                  : "border-slate-300 text-slate-600 hover:bg-slate-100"
              }`}>
              {theme === "dark" ? <SunIcon /> : <MoonIcon />}
            </button>
            {isLogged ? (
              <Link to="/dashboard" className="px-5 py-2 bg-emerald-500 hover:bg-emerald-400 text-white rounded-lg text-sm font-semibold transition-all">
                Dashboard →
              </Link>
            ) : (
              <>
                <Link to="/login"    className="text-slate-300 hover:text-white text-sm transition-colors px-4 py-2">Login</Link>
                <Link to="/register" className="px-5 py-2 bg-emerald-500 hover:bg-emerald-400 text-white rounded-lg text-sm font-semibold transition-all">
                  Get Started
                </Link>
              </>
            )}
          </div>
        </div>
      </nav>

      {/* ── HERO ── */}
      <section className="min-h-screen flex items-center justify-center relative px-6 pt-16">

        {/* Background glow */}
        <div className="absolute inset-0 overflow-hidden pointer-events-none">
          <div className="absolute top-1/4 left-1/2 -translate-x-1/2 w-[600px] h-[600px] bg-emerald-500/10 rounded-full blur-3xl" />
          <div className="absolute top-1/3 left-1/4 w-[300px] h-[300px] bg-teal-500/10 rounded-full blur-3xl" />
        </div>

        <div className="max-w-4xl mx-auto text-center relative z-10">

          {/* Badge */}
          <div className="inline-flex items-center gap-2 px-4 py-2 bg-emerald-500/10 border border-emerald-500/30 rounded-full text-emerald-400 text-sm font-medium mb-8">
            <span className="w-2 h-2 bg-emerald-400 rounded-full animate-pulse" />
            Peer-to-Peer Skill Exchange Platform
          </div>

          <h1 className="text-5xl sm:text-7xl font-black leading-none tracking-tight mb-6">
            Exchange Skills,<br />
            <span className="text-emerald-400">Build Futures</span>
          </h1>

          <p className="text-slate-400 text-lg sm:text-xl max-w-2xl mx-auto mb-10 leading-relaxed">
            GyaanSetu connects learners and tutors through an intelligent skill-exchange economy.
            Teach what you know, learn what you don't.
          </p>

          {/* Scrolling skills */}
          <div className="flex flex-wrap justify-center gap-2 mb-10">
            {skills.map((s, i) => (
              <span
                key={s}
                className="px-3 py-1 rounded-full text-xs font-medium border transition-all duration-500"
                style={{
                  borderColor: i % 3 === 0 ? "#10b981" : i % 3 === 1 ? "#0ea5e9" : "#8b5cf6",
                  color:       i % 3 === 0 ? "#10b981" : i % 3 === 1 ? "#0ea5e9" : "#8b5cf6",
                  background:  i % 3 === 0 ? "#10b98115" : i % 3 === 1 ? "#0ea5e915" : "#8b5cf615",
                }}
              >
                {s}
              </span>
            ))}
          </div>

          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Link
              to="/register"
              className="px-8 py-4 bg-emerald-500 hover:bg-emerald-400 text-white font-bold rounded-xl text-lg transition-all hover:scale-105 hover:shadow-lg hover:shadow-emerald-500/25"
            >
              Start Exchanging Skills →
            </Link>
            <Link
              to="/login"
              className="px-8 py-4 border border-slate-600 hover:border-emerald-500 text-slate-300 hover:text-white font-semibold rounded-xl text-lg transition-all"
            >
              Already a member
            </Link>
          </div>
        </div>
      </section>

      {/* ── STATS ── */}
      <section className="py-16 border-y border-slate-800">
        <div className="max-w-4xl mx-auto px-6 grid grid-cols-2 sm:grid-cols-4 gap-8 text-center">
          {[
            { n: "13+",  l: "Skills Available" },
            { n: "3",    l: "Badge Levels" },
            { n: "100%", l: "Verified Tutors" },
            { n: "AI",   l: "Powered Matching" },
          ].map(({ n, l }) => (
            <div key={l}>
              <p className="text-3xl font-black text-emerald-400">{n}</p>
              <p className="text-slate-400 text-sm mt-1">{l}</p>
            </div>
          ))}
        </div>
      </section>

      {/* ── FEATURES ── */}
      <section className="py-24 px-6">
        <div className="max-w-6xl mx-auto">
          <div className="text-center mb-16">
            <h2 className="text-4xl font-black mb-4">Everything You Need</h2>
            <p className="text-slate-400 text-lg">Built with AI at every layer</p>
          </div>
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
            {features.map((f) => (
              <div
                key={f.title}
                className="p-6 bg-slate-900 border border-slate-800 rounded-2xl hover:border-emerald-500/50 hover:bg-slate-800/50 transition-all group"
              >
                <span className="text-3xl mb-4 block">{f.icon}</span>
                <h3 className="text-white font-bold text-lg mb-2 group-hover:text-emerald-400 transition-colors">{f.title}</h3>
                <p className="text-slate-400 text-sm leading-relaxed">{f.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* ── HOW IT WORKS ── */}
      <section className="py-24 px-6 bg-slate-900/50">
        <div className="max-w-4xl mx-auto text-center">
          <h2 className="text-4xl font-black mb-16">How It Works</h2>
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-8">
            {[
              { step: "01", title: "Register & Verify", desc: "Sign up, take a skill test and get verified as a trusted tutor" },
              { step: "02", title: "Match & Connect",   desc: "AI finds your perfect skill exchange partners automatically" },
              { step: "03", title: "Learn & Earn",      desc: "Conduct sessions, earn credits, learn from others in return" },
            ].map((s) => (
              <div key={s.step} className="relative">
                <div className="text-6xl font-black text-emerald-500/20 mb-4">{s.step}</div>
                <h3 className="text-white font-bold text-lg mb-2">{s.title}</h3>
                <p className="text-slate-400 text-sm">{s.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* ── CTA ── */}
      <section className="py-24 px-6">
        <div className="max-w-2xl mx-auto text-center">
          <h2 className="text-4xl font-black mb-4">Ready to Start?</h2>
          <p className="text-slate-400 mb-8">Join GyaanSetu and be part of India's first peer-to-peer skill exchange economy.</p>
          <Link
            to="/register"
            className="inline-block px-10 py-4 bg-emerald-500 hover:bg-emerald-400 text-white font-bold rounded-xl text-lg transition-all hover:scale-105"
          >
            Create Free Account →
          </Link>
        </div>
      </section>

      {/* ── FOOTER ── */}
      <footer className="border-t border-slate-800 py-8 px-6 text-center text-slate-500 text-sm">
        <p>© 2025 GyaanSetu — Peer-to-Peer Skill Exchange</p>
      </footer>
    </div>
  );
}