import { useEffect, useState } from "react";
import { getOrders, getRevenueByProduct, getSummary } from "./api";
import SummaryCards from "./components/SummaryCards";
import RevenueChart from "./components/RevenueChart";
import OrdersTable from "./components/OrdersTable";

function App() {
  const [summary, setSummary] = useState(null);
  const [revenue, setRevenue] = useState(null);
  const [orders, setOrders] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    Promise.all([getSummary(), getRevenueByProduct(), getOrders()])
      .then(([summaryData, revenueData, ordersData]) => {
        setSummary(summaryData);
        setRevenue(revenueData);
        setOrders(ordersData);
      })
      .catch((err) => setError(err.message));
  }, []);

  return (
    <>
      <h1 style={{ fontSize: 24, marginBottom: 24 }}>Sales dashboard</h1>

      {error && (
        <p style={{ color: "#d03b3b" }}>
          Couldn't load data from the API: {error}. Is the backend running on
          http://localhost:8000?
        </p>
      )}

      {!error && !summary && <p>Loading…</p>}

      {summary && <SummaryCards summary={summary} />}
      {revenue && <RevenueChart data={revenue} />}
      {orders && <OrdersTable orders={orders} />}
    </>
  );
}

export default App;
