let allData = [];
let currentPage = 1;
const recordsPerPage = 10;

async function loadHistory() {
  try {
    const response = await fetch(`${API_BASE}/admin-security/visitor-history`);
    const data = await response.json();

    allData = data.reverse();
    renderTable();
    renderPagination();

  } catch (error) {
    console.error("Error loading history:", error);
  }
}