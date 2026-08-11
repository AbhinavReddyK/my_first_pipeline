const API_BASE = "http://localhost:8000";

async function getJSON(path) {
  const res = await fetch(`${API_BASE}${path}`);
  if (!res.ok) throw new Error(`${path} failed: ${res.status}`);
  return res.json();
}

export const getSummary = () => getJSON("/api/summary");
export const getOrders = () => getJSON("/api/orders");
export const getRevenueByProduct = () => getJSON("/api/revenue-by-product");
