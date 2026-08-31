import axios from "axios";

const BASE = "http://localhost:5000/api";

const token = () => localStorage.getItem("token");
const auth  = () => ({ headers: { Authorization: `Bearer ${token()}` } });

// ── AUTH ─────────────────────────────────────────────────────
export const registerUser  = (data)         => axios.post(`${BASE}/auth/register`, data);
export const loginUser     = (data)         => axios.post(`${BASE}/auth/login`, data);
export const getProfile    = ()             => axios.get(`${BASE}/auth/profile`, auth());
export const getTutors     = ()             => axios.get(`${BASE}/auth/tutors`);
export const getSmartMatch = (limit = 10)  => axios.get(`${BASE}/auth/smart_match?limit=${limit}`, auth());
export const getCredits    = ()             => axios.get(`${BASE}/auth/credits`, auth());
export const updateBio     = (bio)          => axios.put(`${BASE}/auth/update_bio`, { bio }, auth());
export const updateSkills  = (data)         => axios.put(`${BASE}/auth/update_skills`, data, auth());
export const rateTutor     = (email, data)  => axios.post(`${BASE}/auth/rate_tutor/${email}`, data, auth());
export const getReviews    = (email)        => axios.get(`${BASE}/auth/reviews/${email}`);
export const getRecommendations = (top_n=5)=> axios.get(`${BASE}/auth/recommendations?top_n=${top_n}`, auth());
export const getSimilarTutors   = (email, top_n=4) => axios.get(`${BASE}/auth/similar_tutors/${email}?top_n=${top_n}`);

// ── SESSIONS ─────────────────────────────────────────────────
export const sendRequest     = (email, data) => axios.post(`${BASE}/sessions/send_request/${email}`, data, auth());
export const getMyRequests   = ()            => axios.get(`${BASE}/sessions/my_requests`, auth());
export const getAllRequests   = ()            => axios.get(`${BASE}/sessions/requests`, auth());
export const acceptRequest   = (id)          => axios.put(`${BASE}/sessions/accept-request/${id}`, {}, auth());
export const rejectRequest   = (id)          => axios.put(`${BASE}/sessions/reject-request/${id}`, {}, auth());
export const completeSession = (id)          => axios.put(`${BASE}/sessions/complete-session/${id}`, {}, auth());
export const cancelSession   = (id)          => axios.put(`${BASE}/sessions/cancel/${id}`, {}, auth());
export const deleteSession   = (id)          => axios.delete(`${BASE}/sessions/delete/${id}`, auth());

// ── TEST ─────────────────────────────────────────────────────
export const startTest  = (data) => axios.post(`${BASE}/test/start`, data, auth());
export const submitTest = (data) => axios.post(`${BASE}/test/submit`, data, auth());
export const testStatus = ()     => axios.get(`${BASE}/test/status`, auth());

// ── LEARNING ─────────────────────────────────────────────────
export const getRoadmap     = (skill, level) => axios.get(`${BASE}/learn/roadmap?skill=${skill}&level=${level}`, auth());
export const getMyRoadmap   = (level)        => axios.get(`${BASE}/learn/my_roadmap?level=${level}`, auth());
export const getSkillsList  = ()             => axios.get(`${BASE}/learn/skills`);

// ── REPORT ───────────────────────────────────────────────────
export const reportUser     = (email, data)  => axios.post(`${BASE}/report/user/${email}`, data, auth());
export const getMyReports   = ()             => axios.get(`${BASE}/report/my_reports`, auth());
export const getReportsAgainstMe = ()        => axios.get(`${BASE}/report/against_me`, auth());

// ── ADMIN ─────────────────────────────────────────────────────
const ADMIN_KEY = "gyaansetu_admin_2025";
const adminAuth = () => ({ headers: { "X-Admin-Key": ADMIN_KEY } });

export const adminStats       = ()              => axios.get(`${BASE}/admin/stats`, adminAuth());
export const adminGetUsers    = (role="")       => axios.get(`${BASE}/admin/users?role=${role}`, adminAuth());
export const adminBanUser     = (email, reason) => axios.put(`${BASE}/admin/ban/${email}`, { reason }, adminAuth());
export const adminUnbanUser   = (email)         => axios.put(`${BASE}/admin/unban/${email}`, {}, adminAuth());
export const adminAddCredits  = (email, amount) => axios.put(`${BASE}/admin/credits/add/${email}`, { amount }, adminAuth());
export const adminGetSessions = (status="")     => axios.get(`${BASE}/admin/sessions?status=${status}`, adminAuth());
export const adminFraudLogs   = ()              => axios.get(`${BASE}/admin/fraud_logs`, adminAuth());