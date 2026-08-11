import "./SummaryCards.css";

const currency = new Intl.NumberFormat("en-US", {
  style: "currency",
  currency: "USD",
});

export default function SummaryCards({ summary }) {
  return (
    <div className="summary-cards">
      <div className="stat-card">
        <p className="label">Total orders</p>
        <p className="value">{summary.total_orders.toLocaleString()}</p>
      </div>
      <div className="stat-card">
        <p className="label">Total revenue</p>
        <p className="value">{currency.format(summary.total_revenue)}</p>
      </div>
      <div className="stat-card">
        <p className="label">Products</p>
        <p className="value">{summary.product_count.toLocaleString()}</p>
      </div>
    </div>
  );
}
