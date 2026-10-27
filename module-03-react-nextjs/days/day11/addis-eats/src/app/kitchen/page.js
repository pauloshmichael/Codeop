"use client";

/**
 * @file app/kitchen/page.js
 * @description Kitchen staff dashboard — lists all orders and allows staff
 * to advance each order through the status pipeline.
 *
 * Client Component because:
 *  - Uses SWR for live order list (auto-refreshes every 10 seconds)
 *  - Calls PATCH /api/orders/:id to update status on button click
 *  - Manages local optimistic updates with useState
 */

import useSWR, { mutate } from "swr";
import { fetcher } from "@/lib/fetcher";
import Link from "next/link";
import SignOutButton from "@/components/SignOutButton";

/** Status progression — each status advances to the next. */
const NEXT_STATUS = {
  pending:    "preparing",
  preparing:  "ready",
  ready:      "delivering",
  delivering: "delivered",
};

const STATUS_COLORS = {
  pending:    { bg: "#fdebd0", color: "#a04000" },
  preparing:  { bg: "#d5f5e3", color: "#1e8449" },
  ready:      { bg: "#d6eaf8", color: "#1a5276" },
  delivering: { bg: "#e8daef", color: "#6c3483" },
  delivered:  { bg: "#eaecee", color: "#5d6d7e" },
  cancelled:  { bg: "#fde8e6", color: "#c0392b" },
};

function OrderCard({ order, onStatusChange, updating }) {
  const colors = STATUS_COLORS[order.status] ?? STATUS_COLORS.pending;
  const nextStatus = NEXT_STATUS[order.status];

  return (
    <div
      className="card"
      style={{ padding: "1.25rem", display: "flex", flexDirection: "column", gap: "0.75rem" }}
    >
      {/* Header row */}
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start", gap: "0.5rem" }}>
        <div>
          <p style={{ fontWeight: 700, fontSize: "0.95rem" }}>{order.customerName}</p>
          <p style={{ fontSize: "0.75rem", color: "var(--color-text-light)" }}>
            {order.id} · {new Date(order.createdAt).toLocaleTimeString()}
          </p>
        </div>
        <span
          className="badge"
          style={{ background: colors.bg, color: colors.color, whiteSpace: "nowrap" }}
        >
          {order.status}
        </span>
      </div>

      {/* Items */}
      <ul style={{ margin: 0, padding: 0, listStyle: "none", display: "flex", flexDirection: "column", gap: "0.25rem" }}>
        {order.items.map((item, i) => (
          <li key={i} style={{ fontSize: "0.825rem", color: "var(--color-text-muted)", display: "flex", justifyContent: "space-between" }}>
            <span>{item.name} ×{item.quantity}</span>
            <span>ETB {item.price * item.quantity}</span>
          </li>
        ))}
      </ul>

      {/* Total & address */}
      <div style={{ borderTop: "1px solid var(--color-border)", paddingTop: "0.6rem", fontSize: "0.825rem" }}>
        <p style={{ color: "var(--color-text-muted)" }}>📍 {order.deliveryAddress}</p>
        <p style={{ fontWeight: 700, marginTop: "0.2rem" }}>Total: ETB {order.total}</p>
      </div>

      {/* Actions */}
      {nextStatus && (
        <button
          onClick={() => onStatusChange(order.id, nextStatus)}
          disabled={updating === order.id}
          className="btn btn-primary"
          style={{ width: "100%", opacity: updating === order.id ? 0.6 : 1 }}
        >
          {updating === order.id
            ? "Updating…"
            : `Mark as ${nextStatus.charAt(0).toUpperCase() + nextStatus.slice(1)} →`}
        </button>
      )}

      {order.status !== "cancelled" && order.status !== "delivered" && (
        <button
          onClick={() => onStatusChange(order.id, "cancelled")}
          disabled={updating === order.id}
          className="btn btn-secondary"
          style={{ width: "100%", fontSize: "0.825rem" }}
        >
          Cancel Order
        </button>
      )}
    </div>
  );
}

export default function KitchenPage() {
  const { data, error, isLoading } = useSWR("/api/orders", fetcher, {
    refreshInterval: 10_000,
  });

  const [updating, setUpdating] = useState(null);

  async function handleStatusChange(id, newStatus) {
    setUpdating(id);
    try {
      await fetch(`/api/orders/${id}`, {
        method: "PATCH",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ status: newStatus }),
      });
      mutate("/api/orders"); // revalidate the list
    } finally {
      setUpdating(null);
    }
  }

  const orders = data?.orders ?? [];
  const active = orders.filter((o) => !["delivered", "cancelled"].includes(o.status));
  const done   = orders.filter((o) =>  ["delivered", "cancelled"].includes(o.status));

  return (
    <div style={{ padding: "2rem 1.5rem" }}>
      <div className="container">
        {/* Header */}
        <div
          style={{
            display: "flex",
            justifyContent: "space-between",
            alignItems: "center",
            flexWrap: "wrap",
            gap: "1rem",
            marginBottom: "2rem",
          }}
        >
          <div>
            <h1 style={{ fontSize: "1.75rem", fontWeight: 800 }}>👨‍🍳 Kitchen Dashboard</h1>
            <p style={{ color: "var(--color-text-muted)", fontSize: "0.875rem" }}>
              Auto-refreshes every 10 seconds · {active.length} active order{active.length !== 1 ? "s" : ""}
            </p>
          </div>
          <div style={{ display: "flex", gap: "0.75rem" }}>
            <Link href="/" className="btn btn-secondary">Home</Link>
            <SignOutButton />
          </div>
        </div>

        {isLoading && (
          <div style={{ textAlign: "center", padding: "3rem", color: "var(--color-text-muted)" }}>
            ⏳ Loading orders…
          </div>
        )}

        {error && (
          <div style={{ color: "#c0392b", textAlign: "center", padding: "2rem" }}>
            ❌ Failed to load orders: {error.message}
          </div>
        )}

        {/* Active orders */}
        {active.length > 0 && (
          <section style={{ marginBottom: "3rem" }}>
            <h2 style={{ fontWeight: 700, fontSize: "1.1rem", marginBottom: "1rem" }}>
              Active Orders ({active.length})
            </h2>
            <div
              style={{
                display: "grid",
                gridTemplateColumns: "repeat(auto-fill, minmax(280px, 1fr))",
                gap: "1rem",
              }}
            >
              {active.map((order) => (
                <OrderCard
                  key={order.id}
                  order={order}
                  onStatusChange={handleStatusChange}
                  updating={updating}
                />
              ))}
            </div>
          </section>
        )}

        {/* Completed/cancelled orders */}
        {done.length > 0 && (
          <section>
            <h2 style={{ fontWeight: 700, fontSize: "1.1rem", marginBottom: "1rem", color: "var(--color-text-muted)" }}>
              Completed / Cancelled ({done.length})
            </h2>
            <div
              style={{
                display: "grid",
                gridTemplateColumns: "repeat(auto-fill, minmax(280px, 1fr))",
                gap: "1rem",
                opacity: 0.65,
              }}
            >
              {done.map((order) => (
                <OrderCard
                  key={order.id}
                  order={order}
                  onStatusChange={handleStatusChange}
                  updating={updating}
                />
              ))}
            </div>
          </section>
        )}

        {!isLoading && orders.length === 0 && (
          <div style={{ textAlign: "center", padding: "4rem", color: "var(--color-text-muted)" }}>
            <div style={{ fontSize: "3rem", marginBottom: "1rem" }}>🎉</div>
            <p style={{ fontWeight: 600 }}>No orders yet — all clear!</p>
          </div>
        )}
      </div>
    </div>
  );
}

// useState import fix (we declared useState inside the component but forgot the import above)
import { useState } from "react";
