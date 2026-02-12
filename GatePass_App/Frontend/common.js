// common.js

// ✅ Central API URL (ONLY declare here)
const API_BASE = "https://gate-pass-system-auhy.onrender.com";

// Logout
function logout() {
  localStorage.clear();
  window.location.href = "index.html";
}

function goBack() {
  window.history.back();
}