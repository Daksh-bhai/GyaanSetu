import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import { ThemeProvider } from "./ThemeContext";

import Landing from "./pages/Landing";
import Login from "./pages/Login";
import Register from "./pages/Register";
import Sessions from "./pages/Sessions";
import SessionRoom from "./pages/SessionRoom";
import TutorDashboard from "./pages/TutorDashboard";
import { LearnerDashboard } from "./pages/LearnerDashboard";
import BrowseTutors from "./pages/BrowseTutors";
import { SmartMatch, Roadmap, VerifySkill } from "./pages/SmartMatch";
import ChatRoom from "./pages/ChatRoom";

function Protected({ children }) {
  const token = localStorage.getItem("token");
  if (!token) return <Navigate to="/login" replace />;
  return children;
}

function DashboardRouter() {
  const role = (localStorage.getItem("role") || "").toLowerCase();
  if (role === "tutor") return <TutorDashboard />;
  return <LearnerDashboard />;
}

export default function App() {
  return (
    <ThemeProvider>
      <BrowserRouter>
      <Routes>
        <Route path="/" element={<Landing />} />
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />

        <Route
          path="/dashboard"
          element={
            <Protected>
              <DashboardRouter />
            </Protected>
          }
        />

        <Route
          path="/sessions"
          element={
            <Protected>
              <Sessions />
            </Protected>
          }
        />

        <Route
          path="/session/:sessionId"
          element={
            <Protected>
              <SessionRoom />
            </Protected>
          }
        />

        <Route
          path="/chat/:sessionId"
          element={
            <Protected>
              <ChatRoom />
            </Protected>
          }
        />

        <Route
          path="/browse"
          element={
            <Protected>
              <BrowseTutors />
            </Protected>
          }
        />

        <Route
          path="/smart-match"
          element={
            <Protected>
              <SmartMatch />
            </Protected>
          }
        />

        <Route
          path="/learn"
          element={
            <Protected>
              <Roadmap />
            </Protected>
          }
        />

        <Route
          path="/verify"
          element={
            <Protected>
              <VerifySkill />
            </Protected>
          }
        />

        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </BrowserRouter>
    </ThemeProvider>
  );
}