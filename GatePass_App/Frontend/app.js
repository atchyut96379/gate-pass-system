let currentRole = "RESIDENT"; // default role

function selectRole(role, element) {

  currentRole = role;

  document.getElementById("loginTitle").innerText = role + " Login";

  document.querySelectorAll(".tab").forEach(btn =>
    btn.classList.remove("active")
  );

  element.classList.add("active");
}

async function login() {
  const email = document.getElementById("email").value;
  const password = document.getElementById("password").value;

  const response = await fetch("http://127.0.0.1:8000/login", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({
      email: email,
      password: password
    })
  });

  if (!response.ok) {
    alert("Invalid login credentials");
    return;
  }

  const data = await response.json();

  // ✅ SAVE LOGIN DATA (THIS WAS MISSING)
  localStorage.setItem("userRole", data.role);
  localStorage.setItem("userName", data.name);

  console.log("Saved role:", localStorage.getItem("userRole"));

  // ✅ REDIRECT BASED ON ROLE
  if (data.role === "ADMIN") {
    window.location.href = "admin.html";
  } else if (data.role === "RESIDENT") {
    window.location.href = "resident.html";
  } else if (data.role === "SECURITY") {
    window.location.href = "security.html";
  }
}
// localStorage.setItem("userRole",data.role);
// localStorage.setItem("userName",data.name);
window.onload = function () {
  selectRole("RESIDENT");
};