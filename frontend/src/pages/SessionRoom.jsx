import { useEffect, useRef, useState, useCallback } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { io } from "socket.io-client";
import { getAllRequests, completeSession, cancelSession } from "../api";

const ICE_SERVERS = {
  iceServers: [
    { urls: "stun:stun.l.google.com:19302" },
    { urls: "stun:stun1.l.google.com:19302" },
  ]
};

const SOCKET_URL = "http://localhost:5000";

// ================================================================
// TIMER HOOK
// FIX: startedAt = when BOTH users joined the room (set by both_ready socket event).
//      NEVER loaded from DB (to avoid stale values from previous visits).
// ================================================================
function useSessionTimer(startedAt, durationMin) {
  const [elapsed, setElapsed] = useState(0);

  useEffect(() => {
    if (!startedAt) return;

    // FIX: Append Z if missing so it parses as UTC
    const str = (typeof startedAt === "string" && !startedAt.endsWith("Z") && !startedAt.includes("+"))
      ? startedAt + "Z"
      : startedAt;

    const start = new Date(str).getTime();
    if (isNaN(start)) return;

    const tick = () => {
      const diff = Math.floor((Date.now() - start) / 1000);
      setElapsed(Math.max(0, diff));
    };
    tick();
    const t = setInterval(tick, 1000);
    return () => clearInterval(t);
  }, [startedAt]);

  const total     = (durationMin || 60) * 60;
  const remaining = Math.max(0, total - elapsed);
  const isDone    = elapsed > 0 && elapsed >= total;
  const pct       = elapsed > 0 ? Math.min(100, (elapsed / total) * 100) : 0;

  const fmt = (s) => {
    const h   = Math.floor(s / 3600);
    const m   = Math.floor((s % 3600) / 60);
    const sec = s % 60;
    if (h > 0) return `${h}:${String(m).padStart(2,"0")}:${String(sec).padStart(2,"0")}`;
    return `${String(m).padStart(2,"0")}:${String(sec).padStart(2,"0")}`;
  };

  const hasTimer = !!startedAt && !isNaN(new Date(
    (typeof startedAt === "string" && !startedAt.endsWith("Z") && !startedAt.includes("+"))
      ? startedAt + "Z"
      : startedAt
  ).getTime());

  return {
    elapsed, remaining, isDone, pct,
    fmtRemaining : fmt(remaining),
    fmtElapsed   : fmt(elapsed),
    hasTimer
  };
}


export default function SessionRoom() {
  const { sessionId } = useParams();
  const navigate      = useNavigate();
  const token         = localStorage.getItem("token");
  const myEmail       = localStorage.getItem("email");
  const myName        = localStorage.getItem("name");

  const [session,    setSession]    = useState(null);
  const [isAccepter, setIsAccepter] = useState(false);
  const [loading,    setLoading]    = useState(true);

  const socketRef = useRef(null);

  const [messages,   setMessages]   = useState([]);
  const [chatInput,  setChatInput]  = useState("");
  const [peerName,   setPeerName]   = useState("");
  const [peerOnline, setPeerOnline] = useState(false);
  const chatEndRef = useRef(null);

  // ================================================================
  // Session timer start reference
  //
  // We keep a local copy in localStorage so refreshes don't reset the timer.
  // But when `both_ready` fires, we treat the server's `session_started_at`
  // as authoritative so stale local values can't make the countdown show
  // "Done!" immediately.
  // ================================================================
  const [sessionStartedAt, setSessionStartedAt] = useState(() => {
    const stored = localStorage.getItem(`session_start_${sessionId}`);
    if (!stored) return null;

    // Validate: if the stored value + session duration is in the far past
    // (> 24 hours ago), it's definitely stale — clear it.
    try {
      const storedMs = new Date(stored.endsWith("Z") ? stored : stored + "Z").getTime();
      const ageMs    = Date.now() - storedMs;
      if (ageMs > 24 * 60 * 60 * 1000) {
        localStorage.removeItem(`session_start_${sessionId}`);
        return null;
      }
    } catch {
      localStorage.removeItem(`session_start_${sessionId}`);
      return null;
    }
    return stored;
  });

  // ── WebRTC refs ────────────────────────────────────────────
  const pcRef          = useRef(null);
  const localStream    = useRef(null);
  const remoteStream   = useRef(null);
  const localVideo     = useRef(null);
  const remoteVideo    = useRef(null);

  const [callState, setCallState] = useState("idle");
  const [camOn,     setCamOn]     = useState(true);
  const [micOn,     setMicOn]     = useState(true);

  const [activePanel, setActivePanel] = useState("chat");
  const [toast,       setToast]       = useState({ msg: "", type: "" });
  const [endModal,    setEndModal]    = useState(false);
  const [ending,      setEnding]      = useState(false);

  const timer = useSessionTimer(sessionStartedAt, session?.duration);

  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  useEffect(() => {
    if (activePanel !== "video") return;
    const t = setTimeout(() => {
      if (localVideo.current && localStream.current?.active) {
        localVideo.current.srcObject = localStream.current;
      }
      if (remoteVideo.current && remoteStream.current) {
        remoteVideo.current.srcObject = remoteStream.current;
      }
    }, 100);
    return () => clearTimeout(t);
  }, [activePanel]);

  // ── Load session ───────────────────────────────────────────
  useEffect(() => {
    const load = async () => {
      try {
        const res  = await getAllRequests();
        const list = Array.isArray(res.data) ? res.data : [];
        const s    = list.find(x => (x._id || x.session_id) === sessionId);
        if (!s || s.status !== "accepted") { navigate("/sessions"); return; }
        setSession(s);
        setIsAccepter(s.tutor?.email === myEmail);
        setPeerName(s.tutor?.email === myEmail ? s.learner?.name : s.tutor?.name);

        // ================================================================
        // FIX: DO NOT load session_started_at from DB here.
        //
        // Previously, loading s.session_started_at from DB caused the timer
        // to show as fully elapsed immediately because the DB value was from
        // a previous room visit (e.g., accepted at 6:10 AM, users join at 11:40 AM).
        //
        // The timer is ONLY set by the `both_ready` socket event below.
        // localStorage provides persistence across page refreshes.
        // ================================================================

      } catch {
        navigate("/sessions");
      } finally { setLoading(false); }
    };
    load();
  }, [sessionId, myEmail, navigate]);

  // ── Validate stored start time (avoid stale localStorage) ──
  useEffect(() => {
    if (!session || !sessionStartedAt) return;

    const parseMs = (v) => {
      try {
        if (typeof v !== "string") return NaN;
        const s = (!v.endsWith("Z") && !v.includes("+")) ? v + "Z" : v;
        return new Date(s).getTime();
      } catch {
        return NaN;
      }
    };

    const startMs = parseMs(sessionStartedAt);
    if (!startMs || isNaN(startMs)) {
      localStorage.removeItem(`session_start_${sessionId}`);
      setSessionStartedAt(null);
      return;
    }

    const durationMin = Number(session.duration || 60);
    const totalMs     = durationMin * 60 * 1000;
    const elapsedMs   = Date.now() - startMs;

    if (elapsedMs > totalMs * 2) {
      localStorage.removeItem(`session_start_${sessionId}`);
      setSessionStartedAt(null);
    }
  }, [session, sessionStartedAt, sessionId]);

  // ── Socket setup ───────────────────────────────────────────
  useEffect(() => {
    if (!session) return;

    const socket = io(SOCKET_URL, { transports: ["websocket"] });
    socketRef.current = socket;

    socket.on("connect", () => {
      socket.emit("join_session", { session_id: sessionId, token });
    });

    socket.on("user_joined", (data) => {
      if (data.name !== myName) {
        setPeerOnline(true);
        addSystemMsg(`${data.name} joined`);
      }
    });

    socket.on("user_left", (data) => {
      if (data.name !== myName) {
        setPeerOnline(false);
        addSystemMsg(`${data.name} left`);
      }
    });

    // ================================================================
    // FIX: both_ready → start timer using backend `session_started_at`.
    // This prevents stale localStorage values from instantly showing
    // "Done!" when the 2nd user joins late.
    // ================================================================
    socket.on("both_ready", (payload) => {
      setPeerOnline(true);
      addSystemMsg("Both participants connected — session timer started! ✅");

      const normalizeServerStartedAt = (v) => {
        if (!v) return null;
        if (typeof v !== "string") return null;
        const s = (!v.endsWith("Z") && !v.includes("+")) ? v + "Z" : v;
        const ms = new Date(s).getTime();
        if (!ms || isNaN(ms)) return null;
        return new Date(ms).toISOString();
      };

      const serverStartedAt = normalizeServerStartedAt(payload?.session_started_at);

      setSessionStartedAt((prev) => {
        const key = `session_start_${sessionId}`;

        // Fallback: if server doesn't send a value, don't reset an existing
        // local timer (but start one if we have nothing).
        if (!serverStartedAt) {
          if (prev) return prev;
          const startTime = new Date().toISOString();
          localStorage.setItem(key, startTime);
          return startTime;
        }

        if (!prev) {
          localStorage.setItem(key, serverStartedAt);
          return serverStartedAt;
        }

        const prevS = (!prev.endsWith("Z") && !prev.includes("+")) ? prev + "Z" : prev;
        const prevMs = new Date(prevS).getTime();
        const newMs  = new Date(serverStartedAt).getTime();

        // Overwrite if local timer differs a lot (stale localStorage).
        const shouldOverwrite = isNaN(prevMs) || Math.abs(newMs - prevMs) > 2 * 60 * 1000;
        if (shouldOverwrite) {
          localStorage.setItem(key, serverStartedAt);
          return serverStartedAt;
        }

        return prev;
      });
    });

    socket.on("chat_message", (data) => {
      setMessages(prev => [...prev, { ...data, type: "chat" }]);
    });

    // ── WebRTC ──
    socket.on("webrtc_offer", async ({ offer }) => {
      try {
        const pc = buildPeerConnection();
        await pc.setRemoteDescription(new RTCSessionDescription(offer));

        const stream = await getLocalMedia();
        if (stream) {
          stream.getTracks().forEach(track => {
            const exists = pc.getSenders().some(s => s.track?.id === track.id);
            if (!exists) pc.addTrack(track, stream);
          });
        }

        const answer = await pc.createAnswer();
        await pc.setLocalDescription(answer);
        socket.emit("webrtc_answer", { session_id: sessionId, token, answer });
        setCallState("in-call");
      } catch (e) {
        console.error("Answer error:", e);
        showToast("Failed to answer call", "error");
      }
    });

    socket.on("webrtc_answer", async ({ answer }) => {
      try {
        if (pcRef.current?.signalingState === "have-local-offer") {
          await pcRef.current.setRemoteDescription(new RTCSessionDescription(answer));
          setCallState("in-call");
        }
      } catch (e) { console.error("Set answer error:", e); }
    });

    socket.on("webrtc_ice", async ({ candidate }) => {
      try {
        if (pcRef.current && candidate) {
          await pcRef.current.addIceCandidate(new RTCIceCandidate(candidate));
        }
      } catch { /* ignore stale ICE */ }
    });

    socket.on("call_started", ({ name }) => {
      if (name !== myName) {
        addSystemMsg(`${name} started the video call 📹`);
        setActivePanel("video");
      }
    });

    socket.on("call_ended", ({ name }) => {
      if (name !== myName) {
        addSystemMsg(`${name} ended the call`);
        stopCall(false);
      }
    });

    socket.on("error", ({ message }) => showToast(message, "error"));

    return () => {
      socket.emit("leave_session", { session_id: sessionId, token });
      socket.disconnect();
      stopLocalStream();
      pcRef.current?.close();
    };
  // eslint-disable-next-line
  }, [session]);

  // ── Build PeerConnection ───────────────────────────────────
  const buildPeerConnection = useCallback(() => {
    if (pcRef.current) {
      pcRef.current.close();
      pcRef.current = null;
    }

    const pc = new RTCPeerConnection(ICE_SERVERS);

    pc.onicecandidate = (e) => {
      if (e.candidate) {
        socketRef.current?.emit("webrtc_ice", { session_id: sessionId, token, candidate: e.candidate });
      }
    };

    pc.ontrack = (e) => {
      if (e.streams?.[0]) {
        remoteStream.current = e.streams[0];
        if (remoteVideo.current) {
          remoteVideo.current.srcObject = e.streams[0];
        }
      }
    };

    pc.onconnectionstatechange = () => {
      if (["disconnected", "failed", "closed"].includes(pc.connectionState)) {
        addSystemMsg("Peer disconnected");
        setCallState("idle");
      }
    };

    pcRef.current = pc;
    return pc;
  }, [sessionId, token]);

  // ── Get camera/mic ─────────────────────────────────────────
  const getLocalMedia = async () => {
    if (localStream.current?.active) {
      if (localVideo.current) localVideo.current.srcObject = localStream.current;
      return localStream.current;
    }
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ video: true, audio: true });
      localStream.current = stream;
      if (localVideo.current) localVideo.current.srcObject = stream;
      return stream;
    } catch {
      showToast("Camera/mic access denied. Check browser permissions.", "error");
      return null;
    }
  };

  const stopLocalStream = () => {
    localStream.current?.getTracks().forEach(t => t.stop());
    localStream.current = null;
  };

  const stopCall = useCallback((emitEvent = true) => {
    if (emitEvent) {
      socketRef.current?.emit("call_ended", { session_id: sessionId, token });
    }
    pcRef.current?.close();
    pcRef.current = null;
    stopLocalStream();
    remoteStream.current = null;
    if (remoteVideo.current) remoteVideo.current.srcObject = null;
    if (localVideo.current)  localVideo.current.srcObject  = null;
    setCallState("idle");
  }, [sessionId, token]);

  // ── Start call (CALLER) ────────────────────────────────────
  const startCall = async () => {
    if (!peerOnline) { showToast("Wait for the other participant to join", "warn"); return; }
    if (callState !== "idle") return;

    setActivePanel("video");
    setCallState("calling");

    const stream = await getLocalMedia();
    if (!stream) { setCallState("idle"); return; }

    const pc = buildPeerConnection();
    stream.getTracks().forEach(track => pc.addTrack(track, stream));

    try {
      const offer = await pc.createOffer();
      await pc.setLocalDescription(offer);
      socketRef.current?.emit("webrtc_offer",   { session_id: sessionId, token, offer });
      socketRef.current?.emit("call_started",   { session_id: sessionId, token });
    } catch (e) {
      console.error("Offer error:", e);
      showToast("Failed to start call", "error");
      setCallState("idle");
      stopLocalStream();
    }
  };

  const toggleCam = () => {
    const vt = localStream.current?.getVideoTracks()[0];
    if (vt) { vt.enabled = !vt.enabled; setCamOn(p => !p); }
  };

  const toggleMic = () => {
    const at = localStream.current?.getAudioTracks()[0];
    if (at) { at.enabled = !at.enabled; setMicOn(p => !p); }
  };

  // ── Chat ───────────────────────────────────────────────────
  const sendChat = (e) => {
    e.preventDefault();
    if (!chatInput.trim()) return;
    socketRef.current?.emit("chat_message", { session_id: sessionId, token, message: chatInput.trim() });
    setChatInput("");
  };

  // ── End session ────────────────────────────────────────────
  const handleEndSession = async (type) => {
    setEnding(true);
    try {
      if (type === "complete") await completeSession(sessionId);
      else                     await cancelSession(sessionId);
      // Clear localStorage timer key on session end
      localStorage.removeItem(`session_start_${sessionId}`);
      stopLocalStream();
      pcRef.current?.close();
      socketRef.current?.emit("leave_session", { session_id: sessionId, token });
      navigate("/sessions");
    } catch (e) {
      showToast(e.response?.data?.error || "Action failed", "error");
    } finally { setEnding(false); setEndModal(false); }
  };

  const addSystemMsg = (text) => setMessages(prev => [...prev, {
    type: "system", message: text,
    time: new Date().toLocaleTimeString("en-IN", { hour: "2-digit", minute: "2-digit" })
  }]);

  const showToast = (msg, type = "info") => {
    setToast({ msg, type });
    setTimeout(() => setToast({ msg: "", type: "" }), 3500);
  };

  if (loading) return <Spinner />;
  if (!session) return null;

  return (
    <div className="h-screen bg-slate-950 text-white flex flex-col overflow-hidden">

      {/* ── TOP BAR ──────────────────────────────────────────── */}
      <header className="h-14 bg-slate-900 border-b border-slate-800 flex items-center justify-between px-6 shrink-0 gap-4">
        <div className="flex items-center gap-4 min-w-0">
          <button onClick={() => navigate("/sessions")}
            className="text-slate-400 hover:text-white transition-colors text-sm shrink-0">← Back</button>
          <div className="h-5 w-px bg-slate-700 shrink-0" />
          <div className="min-w-0">
            <span className="text-white font-bold capitalize">{session.skill}</span>
            <span className="text-slate-400 text-xs ml-2">with {peerName}</span>
          </div>
          <div className={`flex items-center gap-1.5 text-xs shrink-0 ${peerOnline ? "text-emerald-400" : "text-slate-500"}`}>
            <span className={`w-1.5 h-1.5 rounded-full ${peerOnline ? "bg-emerald-400 animate-pulse" : "bg-slate-600"}`} />
            {peerOnline ? "Online" : "Waiting for other person..."}
          </div>
        </div>

        <div className="flex items-center gap-3 shrink-0">
          {/* Timer — shows only after both joined (both_ready fired) */}
          {timer.hasTimer ? (
            <div className={`flex items-center gap-2 px-3 py-1.5 rounded-lg border text-sm font-mono font-bold ${
              timer.isDone  ? "bg-emerald-500/10 border-emerald-500/30 text-emerald-400"
              : timer.pct > 75 ? "bg-amber-500/10 border-amber-500/30 text-amber-400"
              : "bg-slate-800 border-slate-700 text-white"
            }`}>
              <span>{timer.isDone ? "⏰" : "⏱"}</span>
              <span>{timer.isDone ? "Done!" : timer.fmtRemaining}</span>
            </div>
          ) : (
            <div className="px-3 py-1.5 rounded-lg border border-slate-700 bg-slate-800 text-slate-500 text-xs flex items-center gap-1.5">
              <span className="w-1.5 h-1.5 rounded-full bg-slate-600 animate-pulse" />
              {fmt(session.duration || 60)} min · waiting for both to join
            </div>
          )}

          {/* Panel toggle */}
          <div className="flex bg-slate-800 rounded-lg p-0.5 gap-0.5">
            {["chat", "video"].map(p => (
              <button key={p} onClick={() => setActivePanel(p)}
                className={`px-3 py-1.5 rounded-md text-xs font-semibold capitalize transition-all ${
                  activePanel === p ? "bg-emerald-500/20 text-emerald-400" : "text-slate-400 hover:text-white"
                }`}>
                {p === "chat" ? "💬 Chat" : "📹 Video"}
                {p === "video" && callState === "in-call" && (
                  <span className="ml-1 w-1.5 h-1.5 bg-red-500 rounded-full inline-block animate-pulse" />
                )}
              </button>
            ))}
          </div>

          {/* End session — accepter only */}
          {isAccepter && (
            <button onClick={() => setEndModal(true)}
              className="px-4 py-1.5 bg-red-500/10 border border-red-500/30 text-red-400 hover:bg-red-500/20 text-xs font-bold rounded-lg transition-all">
              End Session
            </button>
          )}
        </div>
      </header>

      {/* Progress bar — only when timer is running */}
      {timer.hasTimer && (
        <div className="h-0.5 bg-slate-900 shrink-0">
          <div className={`h-full transition-all duration-1000 ${
            timer.isDone ? "bg-emerald-500" : timer.pct > 75 ? "bg-amber-500" : "bg-blue-500"
          }`} style={{ width: `${timer.pct}%` }} />
        </div>
      )}

      {/* Toast */}
      {toast.msg && (
        <div className={`fixed top-16 left-1/2 -translate-x-1/2 z-50 px-5 py-2.5 rounded-xl text-sm font-semibold shadow-xl border ${
          toast.type === "error" ? "bg-red-500/20 border-red-500/40 text-red-300"
          : toast.type === "warn" ? "bg-amber-500/20 border-amber-500/40 text-amber-300"
          : "bg-slate-800 border-slate-700 text-white"
        }`}>{toast.msg}</div>
      )}

      {/* ── MAIN ─────────────────────────────────────────────── */}
      <div className="flex-1 flex overflow-hidden relative">

        {/* Floating call controls when in call but on chat panel */}
        {callState === "in-call" && activePanel === "chat" && (
          <div className="absolute bottom-16 left-1/2 -translate-x-1/2 z-40 flex items-center gap-2
                          bg-slate-900/95 backdrop-blur border border-slate-700 rounded-2xl px-4 py-2 shadow-2xl">
            <button onClick={toggleMic}
              className={`flex flex-col items-center gap-0.5 px-3 py-2 rounded-xl text-xs transition-all ${
                micOn ? "text-white hover:bg-slate-800" : "text-red-400 bg-red-500/10 border border-red-500/30"
              }`}>
              <span className="text-xl">{micOn ? "🎙️" : "🔇"}</span>
              <span>{micOn ? "Mute" : "Unmuted"}</span>
            </button>
            <button onClick={toggleCam}
              className={`flex flex-col items-center gap-0.5 px-3 py-2 rounded-xl text-xs transition-all ${
                camOn ? "text-white hover:bg-slate-800" : "text-red-400 bg-red-500/10 border border-red-500/30"
              }`}>
              <span className="text-xl">{camOn ? "📹" : "📷"}</span>
              <span>{camOn ? "Stop Cam" : "Cam Off"}</span>
            </button>
            <button onClick={() => setActivePanel("video")}
              className="flex flex-col items-center gap-0.5 px-3 py-2 rounded-xl text-xs text-blue-400 hover:bg-blue-500/10 transition-all">
              <span className="text-xl">🖥️</span>
              <span>Video</span>
            </button>
            <button onClick={() => stopCall(true)}
              className="flex flex-col items-center gap-0.5 px-3 py-2 rounded-xl text-xs bg-red-500 hover:bg-red-400 text-white transition-all">
              <span className="text-xl">📵</span>
              <span>End Call</span>
            </button>
          </div>
        )}

        {/* Chat panel */}
        <div className={`flex flex-col ${activePanel === "video" ? "w-72 border-r border-slate-800" : "flex-1"}`}>
          <div className="flex-1 overflow-y-auto p-4 space-y-3">
            {messages.length === 0 && (
              <div className="text-center text-slate-600 py-12">
                <p className="text-3xl mb-2">💬</p>
                <p className="text-sm">No messages yet. Say hi!</p>
              </div>
            )}
            {messages.map((m, i) => {
              if (m.type === "system") return (
                <div key={i} className="text-center">
                  <span className="text-xs text-slate-600 bg-slate-900 px-3 py-1 rounded-full">{m.message}</span>
                </div>
              );
              const isMe = m.name === myName;
              return (
                <div key={i} className={`flex ${isMe ? "justify-end" : "justify-start"}`}>
                  <div className={`max-w-[78%] flex flex-col gap-0.5 ${isMe ? "items-end" : "items-start"}`}>
                    {!isMe && <span className="text-xs text-slate-500 px-1">{m.name}</span>}
                    <div className={`px-4 py-2.5 rounded-2xl text-sm leading-relaxed ${
                      isMe ? "bg-emerald-500 text-white rounded-br-sm" : "bg-slate-800 text-slate-200 rounded-bl-sm"
                    }`}>{m.message}</div>
                    <span className="text-[10px] text-slate-600 px-1">{m.time}</span>
                  </div>
                </div>
              );
            })}
            <div ref={chatEndRef} />
          </div>

          <form onSubmit={sendChat} className="p-3 border-t border-slate-800 flex gap-2 shrink-0">
            <input value={chatInput} onChange={e => setChatInput(e.target.value)}
              placeholder="Type a message..."
              className="flex-1 bg-slate-800 border border-slate-700 text-white rounded-xl px-4 py-2.5 text-sm focus:outline-none focus:border-emerald-500 transition-colors placeholder-slate-500"
            />
            <button type="submit"
              className="px-4 py-2.5 bg-emerald-500 hover:bg-emerald-400 text-white rounded-xl text-sm font-bold transition-all">↑</button>
          </form>
        </div>

        {/* Video panel */}
        <div className={`flex-1 flex-col bg-black relative ${activePanel === "video" ? "flex" : "hidden"}`}>

          <div className="flex-1 relative flex items-center justify-center bg-slate-900">
            <video ref={remoteVideo} autoPlay playsInline className="w-full h-full object-cover" />
            {callState !== "in-call" && (
              <div className="absolute inset-0 flex items-center justify-center bg-slate-900">
                <div className="text-center">
                  <div className="w-20 h-20 rounded-full bg-slate-800 border border-slate-700 flex items-center justify-center text-3xl mx-auto mb-4">
                    {peerName?.[0]?.toUpperCase() || "?"}
                  </div>
                  <p className="text-white font-semibold">{peerName}</p>
                  <p className="text-slate-400 text-sm mt-1">
                    {callState === "calling" ? "⏳ Calling..." : "Not in call"}
                  </p>
                </div>
              </div>
            )}
          </div>

          <div className="absolute bottom-20 right-4 w-36 h-24 rounded-xl overflow-hidden border-2 border-slate-700 bg-slate-800 shadow-2xl">
            <video ref={localVideo} autoPlay playsInline muted className="w-full h-full object-cover" />
            {!camOn && (
              <div className="absolute inset-0 bg-slate-900 flex items-center justify-center">
                <span className="text-slate-500 text-xs">Cam off</span>
              </div>
            )}
            <div className="absolute bottom-1 left-1/2 -translate-x-1/2 text-[9px] text-slate-400 bg-black/50 px-1.5 py-0.5 rounded">You</div>
          </div>

          <div className="h-16 bg-slate-900/95 backdrop-blur border-t border-slate-800 flex items-center justify-center gap-4 shrink-0">
            {callState === "idle" && (
              <button onClick={startCall}
                className="px-6 py-2.5 bg-emerald-500 hover:bg-emerald-400 text-white font-bold rounded-xl text-sm transition-all flex items-center gap-2">
                📹 Start Video Call
              </button>
            )}
            {callState === "calling" && (
              <div className="flex items-center gap-2 text-amber-400 text-sm font-semibold">
                <span className="animate-pulse text-lg">📞</span> Calling {peerName}...
              </div>
            )}
            {callState === "in-call" && (
              <>
                <CtrlBtn onClick={toggleMic} active={micOn} icon={micOn ? "🎙️" : "🔇"} label={micOn ? "Mute" : "Unmuted"} />
                <CtrlBtn onClick={toggleCam} active={camOn} icon={camOn ? "📹" : "📷"} label={camOn ? "Stop Cam" : "Cam Off"} />
                <button onClick={() => stopCall(true)}
                  className="px-5 py-2 bg-red-500 hover:bg-red-400 text-white text-sm font-bold rounded-xl transition-all flex items-center gap-2">
                  📵 End Call
                </button>
              </>
            )}
          </div>
        </div>
      </div>

      {/* ── END SESSION MODAL ────────────────────────────────── */}
      {endModal && (
        <div className="fixed inset-0 bg-black/80 backdrop-blur-sm flex items-center justify-center z-50 px-4">
          <div className="bg-slate-900 border border-slate-700 rounded-2xl p-8 max-w-sm w-full">
            <h3 className="text-white font-black text-xl mb-3">End Session?</h3>

            {!timer.hasTimer ? (
              <div className="mb-6 p-3 bg-slate-800 border border-slate-700 rounded-xl">
                <p className="text-slate-400 text-sm">
                  ⚠️ Session timer hasn't started yet (waiting for both to join).
                  Ending now will refund credits to the learner.
                </p>
              </div>
            ) : timer.isDone ? (
              <div className="mb-6 p-3 bg-emerald-500/10 border border-emerald-500/30 rounded-xl">
                <p className="text-emerald-400 text-sm font-semibold">✅ Full duration completed!</p>
                <p className="text-slate-400 text-xs mt-1">You'll receive {session.escrow_credits} credit(s).</p>
              </div>
            ) : (
              <div className="mb-6 p-3 bg-amber-500/10 border border-amber-500/30 rounded-xl">
                <p className="text-amber-400 text-sm font-semibold">
                  ⚠️ Early end ({timer.fmtElapsed} / {session.duration} min)
                </p>
                <p className="text-slate-400 text-xs mt-1">
                  Early end = <span className="text-red-400 font-semibold">no credits for you</span>. Credits refunded to requester.
                </p>
              </div>
            )}

            <div className="space-y-3">
              <button onClick={() => handleEndSession("complete")} disabled={ending || !timer.hasTimer || !timer.isDone}
                className={`w-full py-3 font-bold rounded-xl text-sm transition-all disabled:opacity-50 ${
                  !timer.hasTimer || timer.isDone
                    ? "bg-emerald-500 hover:bg-emerald-400 text-white"
                    : "bg-amber-500/10 border border-amber-500/30 text-amber-400 hover:bg-amber-500/20"
                }`}>
                {ending
                  ? "Processing..."
                  : (!timer.hasTimer)
                    ? "⏳ Complete after both joined"
                    : timer.isDone
                      ? "✅ Complete & Receive Credits"
                      : "⏳ Complete after timer ends"}
              </button>
              <button onClick={() => handleEndSession("cancel")} disabled={ending}
                className="w-full py-3 bg-red-500/10 border border-red-500/30 text-red-400 hover:bg-red-500/20 font-bold rounded-xl text-sm transition-all disabled:opacity-50">
                Cancel Session (Refund Requester)
              </button>
              <button onClick={() => setEndModal(false)}
                className="w-full py-3 border border-slate-700 text-slate-400 hover:text-white rounded-xl text-sm transition-all">
                Keep Going
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

// ── Helper: format minutes ────────────────────────────────────
function fmt(minutes) {
  const h = Math.floor(minutes / 60);
  const m = minutes % 60;
  if (h > 0) return `${h}h ${m}m`;
  return `${m}m`;
}

function CtrlBtn({ onClick, active, icon, label }) {
  return (
    <button onClick={onClick}
      className={`flex flex-col items-center gap-0.5 px-4 py-2 rounded-xl text-xs transition-all ${
        active ? "text-white hover:bg-slate-800" : "text-red-400 bg-red-500/10 border border-red-500/30"
      }`}>
      <span className="text-xl">{icon}</span>
      <span>{label}</span>
    </button>
  );
}

function Spinner() {
  return (
    <div className="h-screen bg-slate-950 flex items-center justify-center">
      <div className="w-8 h-8 border-2 border-emerald-500 border-t-transparent rounded-full animate-spin" />
    </div>
  );
}