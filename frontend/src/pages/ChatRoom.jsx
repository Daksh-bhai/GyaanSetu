import { useEffect, useRef, useState, useCallback } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { io } from "socket.io-client";
import Navbar from "../components/Navbar";
import { getAllRequests } from "../api";

// ── Fix for simple-peer in webpack 5 (CRA) ────────────────────
window.global = window.global || window;
window.process = window.process || { env: { NODE_ENV: "development" } };

const SOCKET_URL = "http://localhost:5000";

// ================================================================
// CHAT ROOM  —  Chat + Video in one page
// URL: /chat/:sessionId
// ================================================================

export default function ChatRoom() {
  const { sessionId } = useParams();
  const navigate      = useNavigate();

  const myEmail = localStorage.getItem("email") || "";
  const myName  = localStorage.getItem("name")  || "You";

  // ── Socket ────────────────────────────────────────────────────
  const socketRef = useRef(null);
  const [connected, setConnected] = useState(false);

  // ── Chat state ────────────────────────────────────────────────
  const [messages,   setMessages]   = useState([]);
  const [input,      setInput]      = useState("");
  const [typingText, setTypingText] = useState("");
  const messagesEndRef  = useRef(null);
  const typingTimerRef  = useRef(null);

  // ── Session / partner info ─────────────────────────────────────
  const [session, setSession] = useState(null);
  const [partner, setPartner] = useState(null);

  // ── Video / call state ─────────────────────────────────────────
  // "idle" | "calling" | "incoming" | "in_call"
  const [callState,    setCallState]    = useState("idle");
  const callStateRef   = useRef("idle"); // ref for socket handlers
  const [incomingFrom, setIncomingFrom] = useState("");
  const [micOn,        setMicOn]        = useState(true);
  const [camOn,        setCamOn]        = useState(true);
  const [localActive,  setLocalActive]  = useState(false);
  const [remoteActive, setRemoteActive] = useState(false);

  const localVideoRef   = useRef(null);
  const remoteVideoRef  = useRef(null);
  const localStreamRef  = useRef(null);
  const peerRef         = useRef(null);
  const isInitiatorRef  = useRef(false);

  // Keep callStateRef in sync
  const updateCallState = (s) => {
    callStateRef.current = s;
    setCallState(s);
  };

  // ── Load session info ─────────────────────────────────────────
  useEffect(() => {
    getAllRequests()
      .then((res) => {
        const list = Array.isArray(res.data) ? res.data : [];
        const s    = list.find((x) => (x._id || x.session_id) === sessionId);
        if (!s) return;
        setSession(s);
        setPartner(s.learner?.email === myEmail ? s.tutor : s.learner);
      })
      .catch(() => {});
  }, [sessionId, myEmail]);

  // ── WebRTC: get media ─────────────────────────────────────────
  const getMedia = useCallback(async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({
        video: true,
        audio: true,
      });
      localStreamRef.current = stream;
      if (localVideoRef.current) localVideoRef.current.srcObject = stream;
      setLocalActive(true);
      return stream;
    } catch {
      try {
        const stream = await navigator.mediaDevices.getUserMedia({
          video: false,
          audio: true,
        });
        localStreamRef.current = stream;
        setLocalActive(true);
        return stream;
      } catch {
        alert("Camera / microphone access denied.");
        return null;
      }
    }
  }, []);

  const stopMedia = useCallback(() => {
    localStreamRef.current?.getTracks().forEach((t) => t.stop());
    localStreamRef.current = null;
    if (localVideoRef.current)  localVideoRef.current.srcObject  = null;
    if (remoteVideoRef.current) remoteVideoRef.current.srcObject = null;
    setLocalActive(false);
    setRemoteActive(false);
  }, []);

  // ── WebRTC: create SimplePeer ─────────────────────────────────
  const startWebRTC = useCallback(
    async (initiator) => {
      const stream = localStreamRef.current;
      if (!stream) return;

      // Dynamic import avoids webpack 5 polyfill issues
      const SimplePeer = (await import("simple-peer")).default;

      const peer = new SimplePeer({
        initiator,
        trickle : true,
        stream,
        config  : {
          iceServers: [
            { urls: "stun:stun.l.google.com:19302"  },
            { urls: "stun:stun1.l.google.com:19302" },
          ],
        },
      });

      peer.on("signal", (signal) => {
        socketRef.current?.emit("relay_signal", {
          room   : sessionId,
          signal,
          sender : myEmail,
        });
      });

      peer.on("stream", (remoteStream) => {
        if (remoteVideoRef.current) {
          remoteVideoRef.current.srcObject = remoteStream;
        }
        setRemoteActive(true);
      });

      peer.on("error", (err) => {
        console.error("Peer error:", err);
        endCall(true);
      });

      peer.on("close", () => {
        if (callStateRef.current === "in_call") endCall(false);
      });

      peerRef.current = peer;
    },
    [sessionId, myEmail] // endCall will be defined below
  );

  // ── End call ──────────────────────────────────────────────────
  const endCall = useCallback(
    (emitEvent = true) => {
      if (emitEvent) {
        socketRef.current?.emit("end_call", {
          room    : sessionId,
          by_name : myName,
        });
      }
      peerRef.current?.destroy();
      peerRef.current = null;
      stopMedia();
      updateCallState("idle");
    },
    [sessionId, myName, stopMedia]
  );

  // ── Socket setup ──────────────────────────────────────────────
  useEffect(() => {
    const socket = io(SOCKET_URL, { transports: ["websocket"] });
    socketRef.current = socket;

    // Connection
    socket.on("connect", () => {
      setConnected(true);
      socket.emit("join_room", { room: sessionId, username: myName });
    });
    socket.on("disconnect", () => setConnected(false));

    // Chat
    socket.on("message_history", ({ messages: hist }) => {
      setMessages(hist || []);
    });

    socket.on("receive_message", (msg) => {
      setMessages((prev) => [...prev, msg]);
    });

    socket.on("user_typing", ({ username, typing }) => {
      setTypingText(typing ? `${username} is typing...` : "");
    });

    socket.on("user_joined", ({ username }) => {
      setMessages((prev) => [
        ...prev,
        { system: true, text: `${username} joined`, timestamp: new Date().toISOString() },
      ]);
    });

    socket.on("user_left", ({ username }) => {
      setMessages((prev) => [
        ...prev,
        { system: true, text: `${username} left`, timestamp: new Date().toISOString() },
      ]);
    });

    // Video signaling
    socket.on("incoming_call", ({ from_name }) => {
      setIncomingFrom(from_name);
      updateCallState("incoming");
    });

    socket.on("call_accepted", () => {
      // Caller side: partner accepted → now both do WebRTC
      updateCallState("in_call");
      startWebRTC(true); // caller = initiator
    });

    socket.on("call_rejected", () => {
      stopMedia();
      updateCallState("idle");
    });

    socket.on("relay_signal", ({ signal, sender }) => {
      if (sender === myEmail) return;
      try {
        peerRef.current?.signal(signal);
      } catch {}
    });

    socket.on("call_ended", () => {
      endCall(false);
    });

    return () => {
      socket.emit("leave_room", { room: sessionId, username: myName });
      socket.disconnect();
      peerRef.current?.destroy();
      stopMedia();
    };
  }, [sessionId, myName, myEmail, startWebRTC, endCall, stopMedia]);

  // ── Auto scroll ───────────────────────────────────────────────
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  // ── Chat: send ────────────────────────────────────────────────
  const sendMessage = () => {
    if (!input.trim() || !socketRef.current) return;
    socketRef.current.emit("send_message", {
      room        : sessionId,
      sender      : myEmail,
      sender_name : myName,
      text        : input.trim(),
    });
    setInput("");
    clearTimeout(typingTimerRef.current);
    socketRef.current.emit("typing", {
      room     : sessionId,
      username : myName,
      typing   : false,
    });
  };

  const onInputChange = (e) => {
    setInput(e.target.value);
    if (!socketRef.current) return;
    socketRef.current.emit("typing", {
      room     : sessionId,
      username : myName,
      typing   : true,
    });
    clearTimeout(typingTimerRef.current);
    typingTimerRef.current = setTimeout(() => {
      socketRef.current?.emit("typing", {
        room     : sessionId,
        username : myName,
        typing   : false,
      });
    }, 2000);
  };

  const onKeyDown = (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  // ── Video: start call ─────────────────────────────────────────
  const startCall = async () => {
    const stream = await getMedia();
    if (!stream) return;
    isInitiatorRef.current = true;
    updateCallState("calling");
    socketRef.current?.emit("call_user", {
      room       : sessionId,
      from_name  : myName,
      from_email : myEmail,
    });
  };

  // ── Video: accept call ─────────────────────────────────────────
  const acceptCall = async () => {
    const stream = await getMedia();
    if (!stream) return;
    isInitiatorRef.current = false;
    updateCallState("in_call");
    socketRef.current?.emit("call_accepted", {
      room    : sessionId,
      by_name : myName,
    });
    startWebRTC(false); // receiver = not initiator
  };

  // ── Video: reject call ─────────────────────────────────────────
  const rejectCall = () => {
    socketRef.current?.emit("call_rejected", {
      room    : sessionId,
      by_name : myName,
    });
    updateCallState("idle");
  };

  // ── Video: toggle mic / cam ────────────────────────────────────
  const toggleMic = () => {
    localStreamRef.current
      ?.getAudioTracks()
      .forEach((t) => (t.enabled = !micOn));
    setMicOn((p) => !p);
  };

  const toggleCam = () => {
    localStreamRef.current
      ?.getVideoTracks()
      .forEach((t) => (t.enabled = !camOn));
    setCamOn((p) => !p);
  };

  // ── Helpers ───────────────────────────────────────────────────
  const fmtTime = (iso) => {
    try {
      return new Date(iso).toLocaleTimeString("en-IN", {
        hour   : "2-digit",
        minute : "2-digit",
      });
    } catch {
      return "";
    }
  };

  // ================================================================
  // RENDER
  // ================================================================
  return (
    <div className="h-screen bg-slate-950 text-white flex flex-col overflow-hidden">
      <Navbar />

      {/* ── Top bar ── */}
      <div className="fixed top-16 left-0 right-0 z-40 bg-slate-900/95 backdrop-blur border-b border-slate-700/50 px-6 h-12 flex items-center justify-between">
        <div className="flex items-center gap-3">
          <button
            onClick={() => navigate("/sessions")}
            className="text-slate-400 hover:text-white text-sm transition-colors"
          >
            ← Back
          </button>
          <div className="w-px h-4 bg-slate-700" />
          <span className="text-white font-semibold text-sm capitalize">
            {session?.skill ? `${session.skill} Session` : "Chat Room"}
          </span>
          {partner && (
            <span className="text-slate-400 text-sm">with {partner.name}</span>
          )}
        </div>

        <div
          className={`text-xs px-2.5 py-1 rounded-full border flex items-center gap-1.5 ${
            connected
              ? "text-emerald-400 border-emerald-500/30 bg-emerald-500/10"
              : "text-amber-400 border-amber-500/30 bg-amber-500/10"
          }`}
        >
          <span
            className={`w-1.5 h-1.5 rounded-full ${
              connected ? "bg-emerald-400 animate-pulse" : "bg-amber-400"
            }`}
          />
          {connected ? "Live" : "Connecting..."}
        </div>
      </div>

      {/* ── Main layout (below navbar + topbar = 112px) ── */}
      <div className="flex flex-1 pt-28 gap-4 px-4 pb-4 overflow-hidden">

        {/* ════════════════════════════════════
            LEFT — Chat
        ════════════════════════════════════ */}
        <div className="flex-1 flex flex-col bg-slate-900 border border-slate-800 rounded-2xl overflow-hidden min-w-0">

          {/* Messages */}
          <div className="flex-1 overflow-y-auto p-4 space-y-2">
            {messages.length === 0 && (
              <div className="flex flex-col items-center justify-center h-full text-slate-500">
                <p className="text-4xl mb-3">💬</p>
                <p className="text-sm font-medium">No messages yet</p>
                <p className="text-xs mt-1">Say something to get started!</p>
              </div>
            )}

            {messages.map((msg, i) => {
              if (msg.system) {
                return (
                  <div key={i} className="flex justify-center">
                    <span className="text-xs text-slate-500 bg-slate-800/60 px-3 py-1 rounded-full">
                      {msg.text}
                    </span>
                  </div>
                );
              }

              const isMe = msg.sender === myEmail;
              return (
                <div
                  key={i}
                  className={`flex ${isMe ? "justify-end" : "justify-start"}`}
                >
                  <div
                    className={`flex flex-col gap-0.5 max-w-xs lg:max-w-sm ${
                      isMe ? "items-end" : "items-start"
                    }`}
                  >
                    {!isMe && (
                      <span className="text-xs text-slate-400 ml-2">
                        {msg.sender_name}
                      </span>
                    )}
                    <div
                      className={`px-4 py-2.5 rounded-2xl text-sm leading-relaxed ${
                        isMe
                          ? "bg-emerald-500 text-white rounded-br-md"
                          : "bg-slate-800 text-slate-100 rounded-bl-md"
                      }`}
                    >
                      {msg.text}
                    </div>
                    <span className="text-[10px] text-slate-500 mx-1">
                      {fmtTime(msg.timestamp)}
                    </span>
                  </div>
                </div>
              );
            })}

            {/* Typing indicator */}
            {typingText && (
              <div className="flex items-center gap-2">
                <div className="bg-slate-800 px-4 py-2.5 rounded-2xl rounded-bl-md flex gap-1 items-center">
                  {[0, 150, 300].map((delay) => (
                    <span
                      key={delay}
                      className="w-1.5 h-1.5 bg-slate-400 rounded-full animate-bounce"
                      style={{ animationDelay: `${delay}ms` }}
                    />
                  ))}
                </div>
                <span className="text-xs text-slate-500">{typingText}</span>
              </div>
            )}

            <div ref={messagesEndRef} />
          </div>

          {/* Input bar */}
          <div className="border-t border-slate-800 p-3 flex gap-3 items-end">
            <textarea
              value={input}
              onChange={onInputChange}
              onKeyDown={onKeyDown}
              placeholder="Type a message… (Enter to send)"
              rows={1}
              className="flex-1 bg-slate-800 border border-slate-700 text-white rounded-xl px-4 py-3 text-sm focus:outline-none focus:border-emerald-500 transition-colors placeholder-slate-500 resize-none"
              style={{ minHeight: "44px", maxHeight: "120px" }}
            />
            <button
              onClick={sendMessage}
              disabled={!input.trim()}
              className="px-5 h-11 bg-emerald-500 hover:bg-emerald-400 disabled:opacity-40 text-white text-sm font-bold rounded-xl transition-all shrink-0"
            >
              Send
            </button>
          </div>
        </div>

        {/* ════════════════════════════════════
            RIGHT — Video Call
        ════════════════════════════════════ */}
        <div className="w-72 flex flex-col gap-3 shrink-0">

          {/* Video feeds */}
          <div className="bg-slate-900 border border-slate-800 rounded-2xl overflow-hidden flex flex-col">

            {/* Remote video area */}
            <div className="relative bg-slate-950 aspect-video">
              {/* Remote video */}
              <video
                ref={remoteVideoRef}
                autoPlay
                playsInline
                className={`w-full h-full object-cover ${remoteActive ? "" : "hidden"}`}
              />

              {/* Placeholder when no remote stream */}
              {!remoteActive && (
                <div className="absolute inset-0 flex flex-col items-center justify-center gap-2">
                  <div className="w-14 h-14 rounded-full bg-slate-800 flex items-center justify-center text-xl font-black text-slate-400">
                    {partner?.name?.[0]?.toUpperCase() || "?"}
                  </div>
                  <p className="text-slate-400 text-xs">
                    {partner?.name || "Partner"}
                  </p>
                  {callState === "calling" && (
                    <p className="text-emerald-400 text-xs animate-pulse">
                      Calling…
                    </p>
                  )}
                  {callState === "in_call" && (
                    <p className="text-blue-400 text-xs animate-pulse">
                      Connecting video…
                    </p>
                  )}
                </div>
              )}

              {/* Local video (picture-in-picture) */}
              <div className="absolute bottom-2 right-2 w-16 aspect-video bg-slate-800 rounded-lg overflow-hidden border border-slate-600">
                {localActive ? (
                  <video
                    ref={localVideoRef}
                    autoPlay
                    playsInline
                    muted
                    className="w-full h-full object-cover"
                  />
                ) : (
                  <div className="w-full h-full flex items-center justify-center">
                    <span className="text-slate-500 text-[9px]">You</span>
                  </div>
                )}
              </div>
            </div>

            {/* Call controls */}
            <div className="p-4">

              {/* ── IDLE ── */}
              {callState === "idle" && (
                <button
                  onClick={startCall}
                  className="w-full py-2.5 bg-emerald-500 hover:bg-emerald-400 text-white text-sm font-bold rounded-xl transition-all flex items-center justify-center gap-2"
                >
                  📹 Start Video Call
                </button>
              )}

              {/* ── CALLING ── */}
              {callState === "calling" && (
                <div className="space-y-3">
                  <p className="text-center text-sm text-slate-400 animate-pulse">
                    Calling {partner?.name}…
                  </p>
                  <button
                    onClick={() => endCall(true)}
                    className="w-full py-2.5 bg-red-500 hover:bg-red-400 text-white text-sm font-bold rounded-xl transition-all"
                  >
                    Cancel
                  </button>
                </div>
              )}

              {/* ── INCOMING CALL ── */}
              {callState === "incoming" && (
                <div className="space-y-3">
                  <div className="text-center">
                    <p className="text-white font-semibold text-sm">
                      📞 Incoming Call
                    </p>
                    <p className="text-slate-400 text-xs mt-0.5 animate-pulse">
                      {incomingFrom} is calling…
                    </p>
                  </div>
                  <div className="flex gap-2">
                    <button
                      onClick={acceptCall}
                      className="flex-1 py-2.5 bg-emerald-500 hover:bg-emerald-400 text-white text-sm font-bold rounded-xl transition-all"
                    >
                      Accept ✓
                    </button>
                    <button
                      onClick={rejectCall}
                      className="flex-1 py-2.5 bg-red-500 hover:bg-red-400 text-white text-sm font-bold rounded-xl transition-all"
                    >
                      Reject ✗
                    </button>
                  </div>
                </div>
              )}

              {/* ── IN CALL ── */}
              {callState === "in_call" && (
                <div className="flex gap-2">
                  <button
                    onClick={toggleMic}
                    className={`flex-1 py-2 rounded-xl text-xs font-bold transition-all ${
                      micOn
                        ? "bg-slate-700 hover:bg-slate-600 text-white"
                        : "bg-red-500/20 border border-red-500/30 text-red-400"
                    }`}
                  >
                    {micOn ? "🎤 Mic" : "🔇 Muted"}
                  </button>
                  <button
                    onClick={toggleCam}
                    className={`flex-1 py-2 rounded-xl text-xs font-bold transition-all ${
                      camOn
                        ? "bg-slate-700 hover:bg-slate-600 text-white"
                        : "bg-red-500/20 border border-red-500/30 text-red-400"
                    }`}
                  >
                    {camOn ? "📹 Cam" : "📷 Off"}
                  </button>
                  <button
                    onClick={() => endCall(true)}
                    className="flex-1 py-2 bg-red-500 hover:bg-red-400 text-white rounded-xl text-xs font-bold transition-all"
                  >
                    End
                  </button>
                </div>
              )}
            </div>
          </div>

          {/* Session info card */}
          {session && (
            <div className="bg-slate-900 border border-slate-800 rounded-2xl p-4">
              <h3 className="text-white font-bold text-sm mb-3">
                📋 Session Details
              </h3>
              <div className="space-y-2">
                {[
                  ["Skill",    session.skill,    "capitalize"],
                  ["Duration", `${session.duration} min`, ""],
                  ["Partner",  partner?.name,    ""],
                  ["Status",   session.status,   "capitalize"],
                ].map(([label, val, extra]) => (
                  <div key={label} className="flex justify-between items-center">
                    <span className="text-slate-500 text-xs">{label}</span>
                    <span className={`text-white text-xs font-medium ${extra}`}>
                      {val || "—"}
                    </span>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* WebRTC info */}
          <div className="bg-slate-900/50 border border-slate-800/50 rounded-xl p-3">
            <p className="text-slate-500 text-[10px] leading-relaxed">
              🔒 Video calls are peer-to-peer (WebRTC). Your call is not recorded or stored on any server.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
