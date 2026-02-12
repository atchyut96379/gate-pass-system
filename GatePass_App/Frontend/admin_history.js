let allData = [];
let currentPage = 1;
const recordsPerPage = 10;

async function loadHistory() {
  try {
    const response = await fetch(`${API_BASE}/admin-security/visitor-history`);
    const data = await response.json();

    const tableBody = document.getElementById("historyTable");
    tableBody.innerHTML = "";

    data.forEach(item => {
      const row = `
        <tr>
          <td>${item.visitor_name}</td>
          <td>${item.visitor_phone}</td>
          <td>${item.purpose}</td>
          <td>${item.flat_number}</td>
          <td>${item.status}</td>
          <td>${new Date(item.created_at).toLocaleString()}</td>
        </tr>
      `;
      tableBody.innerHTML += row;
    });

  } catch (error) {
    console.error("Error loading history:", error);
  }
}

loadHistory();