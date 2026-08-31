import { Link, useNavigate, useLocation } from "react-router-dom";
import { useTheme } from "../ThemeContext";

// ── GyaanSetu SVG Logo ────────────────────────────────────────
function GyanSetuLogo({ size = 32 }) {
  return (
    <svg
      width={size}
      height={size}
      viewBox="0 0 40 40"
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
    >
      {/* Bridge base plate */}
      <rect x="4" y="28" width="32" height="3" rx="1.5" fill="#10b981" />

      {/* Left pillar */}
      <rect x="7" y="16" width="4" height="12" rx="1" fill="#10b981" />

      {/* Right pillar */}
      <rect x="29" y="16" width="4" height="12" rx="1" fill="#10b981" />

      {/* Bridge arch */}
      <path
        d="M11 16 Q20 4 29 16"
        stroke="#10b981"
        strokeWidth="2.5"
        strokeLinecap="round"
        fill="none"
      />

      {/* Suspender lines */}
      <line x1="16" y1="9.5" x2="16" y2="28" stroke="#6ee7b7" strokeWidth="1.2" strokeLinecap="round" />
      <line x1="20" y1="6"   x2="20" y2="28" stroke="#6ee7b7" strokeWidth="1.2" strokeLinecap="round" />
      <line x1="24" y1="9.5" x2="24" y2="28" stroke="#6ee7b7" strokeWidth="1.2" strokeLinecap="round" />

      {/* Book spark on top */}
      <circle cx="20" cy="5.5" r="2" fill="#34d399" opacity="0.9" />
    </svg>
  );
}

// ── Sun icon ─────────────────────────────────────────────────
function SunIcon() {
  return (
    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <circle cx="12" cy="12" r="5" />
      <line x1="12" y1="1" x2="12" y2="3" />
      <line x1="12" y1="21" x2="12" y2="23" />
      <line x1="4.22" y1="4.22" x2="5.64" y2="5.64" />
      <line x1="18.36" y1="18.36" x2="19.78" y2="19.78" />
      <line x1="1" y1="12" x2="3" y2="12" />
      <line x1="21" y1="12" x2="23" y2="12" />
      <line x1="4.22" y1="19.78" x2="5.64" y2="18.36" />
      <line x1="18.36" y1="5.64" x2="19.78" y2="4.22" />
    </svg>
  );
}

// ── Moon icon ─────────────────────────────────────────────────
function MoonIcon() {
  return (
    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z" />
    </svg>
  );
}

export default function Navbar() {
  const navigate  = useNavigate();
  const location  = useLocation();
  const { theme, toggle } = useTheme();

  const role      = localStorage.getItem("role");
  const name      = localStorage.getItem("name");
  const isLogged  = !!localStorage.getItem("token");

  const logout = () => {
    localStorage.clear();
    navigate("/login");
  };

  const active = (path) =>
    location.pathname === path
      ? "text-emerald-500 font-semibold"
      : "text-slate-300 hover:text-white transition-colors";

  if (!isLogged) return null;

  return (
    <nav className="fixed top-0 left-0 right-0 z-50 bg-slate-900/95 backdrop-blur border-b border-slate-700/50">
      <div className="max-w-7xl mx-auto px-6 h-16 flex items-center justify-between">

        {/* ── Logo ── */}
        <Link to="/" className="flex items-center gap-2.5 group">
          <div className="relative">
            <div className="w-9 h-9 bg-emerald-500/10 border border-emerald-500/30 rounded-xl flex items-center justify-center group-hover:bg-emerald-500/20 transition-all">
              <GyanSetuLogo size={26} />
            </div>
            {/* pulse dot */}
            <span className="absolute -top-0.5 -right-0.5 w-2 h-2 bg-emerald-400 rounded-full border-2 border-slate-900 animate-pulse" />
          </div>
          <div className="leading-none">
            <span className="text-white font-black text-lg tracking-tight">
              Gyaan<span className="text-emerald-400">Setu</span>
            </span>
            <p className="text-[9px] text-slate-500 font-medium tracking-widest uppercase">
              Skill Exchange
            </p>
          </div>
        </Link>

        {/* ── Nav Links ── */}
        <div className="flex items-center gap-6 text-sm">
          {role === "tutor" && (
            <>
              <Link to="/dashboard"   className={active("/dashboard")}>Dashboard</Link>
              <Link to="/smart-match" className={active("/smart-match")}>Smart Match</Link>
              <Link to="/sessions"    className={active("/sessions")}>Sessions</Link>
            </>
          )}
          {role === "learner" && (
            <>
              <Link to="/dashboard" className={active("/dashboard")}>Dashboard</Link>
              <Link to="/browse"    className={active("/browse")}>Find Tutors</Link>
              <Link to="/sessions"  className={active("/sessions")}>Sessions</Link>
              <Link to="/learn"     className={active("/learn")}>Learn</Link>
            </>
          )}
        </div>

        {/* ── Right side ── */}
        <div className="flex items-center gap-3">

          {/* Theme Toggle */}
          <button
            onClick={toggle}
            title={theme === "dark" ? "Switch to Light Mode" : "Switch to Dark Mode"}
            className={`
              w-9 h-9 rounded-xl border flex items-center justify-center transition-all
              ${theme === "dark"
                ? "border-slate-600 text-amber-400 hover:bg-slate-800 hover:border-amber-500/50"
                : "border-slate-300 text-slate-600 hover:bg-slate-100 hover:border-slate-400"
              }
            `}
          >
            {theme === "dark" ? <SunIcon /> : <MoonIcon />}
          </button>

          {/* User info */}
          <div className="text-right hidden sm:block">
            <p className="text-white text-sm font-semibold leading-tight">{name}</p>
            <p className="text-emerald-400 text-[10px] capitalize tracking-wide">{role}</p>
          </div>

          {/* Logout */}
          <button
            onClick={logout}
            className="px-4 py-1.5 text-sm text-slate-300 border border-slate-600 rounded-lg hover:border-red-500/60 hover:text-red-400 hover:bg-red-500/5 transition-all"
          >
            Logout
          </button>
        </div>
      </div>
    </nav>
  );
}