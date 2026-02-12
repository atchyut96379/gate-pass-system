let currentRole = "RESIDENT";

function selectRole(role, element) {
  currentRole = role;

  document.getElementById("loginTitle").innerText = role + " Login";

  document.querySelectorAll(".tab").forEach(btn =>
    btn.classList.remove("active")
  );

  if (element) element.classList.add("active");
}

async function login() {
  const email = document.getElementById("email").value.trim();
  const password = document.getElementById("password").value.trim();

  try {
    const response = await fetch(`${API_BASE}/login`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        email,
        password
      })
    });

    const data = await response.json();

    if (!response.ok) {
      alert(data.detail || "Invalid login credentials");
      return;
    }

    localStorage.setItem("userRole", data.role);
    localStorage.setItem("userName", data.name);

    if (data.role === "ADMIN") {
      window.location.href = "admin.html";
    } else if (data.role === "RESIDENT") {
      window.location.href = "resident.html";
    } else if (data.role === "SECURITY") {
      window.location.href = "security.html";
    }

  } catch (error) {
    console.error("Login error:", error);
    alert("Server connection failed.");
  }
}

window.onload = function () {
  selectRole("RESIDENT");
};