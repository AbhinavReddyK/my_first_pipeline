import "./OrdersTable.css";

const currency = new Intl.NumberFormat("en-US", {
  style: "currency",
  currency: "USD",
});

export default function OrdersTable({ orders }) {
  return (
    <div className="table-card">
      <h2>Orders ({orders.length})</h2>
      <div className="table-scroll">
        <table>
          <thead>
            <tr>
              <th>Order ID</th>
              <th>Customer</th>
              <th>Product</th>
              <th className="numeric">Qty</th>
              <th className="numeric">Price</th>
              <th>Date</th>
              <th className="numeric">Total</th>
            </tr>
          </thead>
          <tbody>
            {orders.map((order) => (
              <tr key={order.order_id}>
                <td>{order.order_id}</td>
                <td>{order.customer}</td>
                <td>{order.product}</td>
                <td className="numeric">{order.quantity}</td>
                <td className="numeric">{currency.format(order.price)}</td>
                <td>{order.order_date}</td>
                <td className="numeric">{currency.format(order.total_price)}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
