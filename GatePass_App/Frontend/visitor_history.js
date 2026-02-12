async function loadHistory() {
  const res = await fetch(`${API_BASE}/admin-security/visitor-history`);
  const data = await res.json();
  const table = document.getElementById("historyTable");

  table.innerHTML = "";

  data.forEach(v => {
    table.innerHTML += `
      <tr>
        <td>${v.visitor_name}</td>
        <td>${v.visitor_phone}</td>
        <td>${v.purpose}</td>
        <td>${v.flat_number}</td>
        <td>${v.status}</td>
        <td>${new Date(v.created_at).toLocaleString()}</td>
      </tr>
    `;
  });
}

loadHistory();