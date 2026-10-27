"use client";

/**
 * @file app/orders/[id]/page.js
 * @description Live order tracking page — polls /api/orders/:id every 5 seconds
 * using SWR to show real-time status updates.
 *
 * Demonstrates:
 *  - SWR for client-side data fetching with automatic revalidation
 *  - SWR `refreshInterval` option for live polling
 *  - Dynamic route params with useParams (client component)
 *  - Conditional rendering for loading / error / data states
 */

import { useParams } from "next/navigation";
import useSWR from "swr";
import { fetcher } from "@/lib/fetcher";
import Link from "next/link";

/** Visual timeline step data. */
const STATUS_STEPS = [
  { key: "pending",    label: "Order Received",    icon: "📋" },
  { key: "preparing",  label: "Being Prepared",    icon: "👨‍🍳" },
  { key: "ready",      label: "Ready for Pickup",  icon: "✅" },
  { key: "delivering", label: "Out for Delivery",  icon: "🛵" },
  { key: "delivered",  label: "Delivered!",         icon: "🏠" },
];

function getStepIndex(status) {
  return STATUS_STEPS.findIndex((s) => s.key === status);
}

export default function OrderTrackingPage() {
  const { id } = useParams();

  // Poll every 5 seconds for live updates
  const { data, error, isLoading } = useSWR(
    id ? `/api/orders/${id}` : null,
    fetcher,
    { refreshInterval: 5000 }
  );

  // ── Loading state ──────────────────────────────────────────────────────
  if (isLoading) {
    return (
      <div style={{ padding: "4rem", textAlign: "center", color: "var(--color-text-muted)" }}>
        <div style={{ fontSize: "2rem", marginBottom: "1rem" }}>⏳</div>
        <p>Loading order details…</p>
      </div>
    );
  }

  // ── Error state ────────────────────────────────────────────────────────
  if (error) {
    return (
      <div style={{ padding: "4rem", textAlign: "center" }}>
        <div style={{ fontSize: "2rem", marginBottom: "1rem" }}>❌</div>
        <p style={{ color: "var(--color-primary)", fontWeight: 600, marginBottom: "1rem" }}>
          {error.status === 404
            ? `Order "${id}" was not found.`
            : `Error: ${error.message}`}
        </p>
        <Link href="/menu" className="btn btn-primary">Back to Menu</Link>
      </div>
    );
  }

  const order = data?.order;
  if (!order) return null;

  const currentStepIndex = getStepIndex(order.status);
  const isCancelled = order.status === "cancelled";

  return (
    <div style={{ padding: "3rem 1.5rem" }}>
      <div className="container" style={{ maxWidth: "680px" }}>
        {/* Header */}
        <h1 style={{ fontSize: "1.75rem", fontWeight: 800, marginBottom: "0.35rem" }}>
          Order Tracking
        </h1>
        <p style={{ color: "var(--color-text-muted)", marginBottom: "2rem", fontSize: "0.9rem" }}>
          Order ID: <code style={{ background: "var(--color-surface-alt)", padding: "0.1rem 0.4rem", borderRadius: "0.25rem" }}>{order.id}</code>
          {" · "}Auto-refreshes every 5 seconds
        </p>

        {/* Current status badge */}
        <div
          style={{
            background: isCancelled ? "#fde8e6" : "var(--color-surface-alt)",
            border: `1px solid ${isCancelled ? "#c0392b" : "var(--color-border)"}`,
            borderRadius: "var(--radius-lg)",
            padding: "1.5rem",
            textAlign: "center",
            marginBottom: "2rem",
          }}
        >
          <div style={{ fontSize: "3.5rem", marginBottom: "0.5rem" }}>
            {isCancelled ? "❌" : STATUS_STEPS[currentStepIndex]?.icon ?? "📋"}
          </div>
          <h2 style={{ fontWeight: 700, fontSize: "1.25rem", color: isCancelled ? "#c0392b" : "var(--color-text)" }}>
            {isCancelled ? "Order Cancelled" : STATUS_STEPS[currentStepIndex]?.label ?? order.status}
          </h2>
        </div>

        {/* Progress timeline */}
        {!isCancelled && (
          <div style={{ marginBottom: "2rem" }}>
            {STATUS_STEPS.map((step, index) => {
              const isDone    = index <= currentStepIndex;
              const isCurrent = index === currentStepIndex;
              return (
                <div
                  key={step.key}
                  style={{
                    display: "flex",
                    alignItems: "center",
                    gap: "1rem",
                    paddingBlock: "0.6rem",
                    opacity: isDone ? 1 : 0.35,
                  }}
                >
                  {/* Circle indicator */}
                  <div
                    style={{
                      width: "2rem",
                      height: "2rem",
                      borderRadius: "50%",
                      background: isDone ? "var(--color-primary)" : "var(--color-border)",
                      display: "flex",
                      alignItems: "center",
                      justifyContent: "center",
                      fontSize: "0.8rem",
                      color: "#fff",
                      fontWeight: 700,
                      flexShrink: 0,
                      boxShadow: isCurrent ? "0 0 0 3px #f5b7b1" : "none",
                    }}
                  >
                    {isDone ? "✓" : index + 1}
                  </div>
                  <div>
                    <span style={{ fontWeight: isCurrent ? 700 : 500 }}>
                      {step.icon} {step.label}
                    </span>
                    {isCurrent && (
                      <span
                        style={{
                          marginLeft: "0.5rem",
                          fontSize: "0.75rem",
                          background: "var(--color-primary)",
                          color: "#fff",
                          padding: "0.1rem 0.5rem",
                          borderRadius: "9999px",
                          fontWeight: 600,
                        }}
                      >
                        Current
                      </span>
                    )}
                  </div>
                </div>
              );
            })}
          </div>
        )}

        {/* Order details card */}
        <div className="card" style={{ padding: "1.5rem" }}>
          <h3 style={{ fontWeight: 700, marginBottom: "1rem", fontSize: "0.95rem" }}>
            Order Details
          </h3>
          <p style={{ fontSize: "0.875rem", color: "var(--color-text-muted)", marginBottom: "0.35rem" }}>
            <strong>Customer:</strong> {order.customerName}
          </p>
          <p style={{ fontSize: "0.875rem", color: "var(--color-text-muted)", marginBottom: "0.35rem" }}>
            <strong>Address:</strong> {order.deliveryAddress}
          </p>
          <p style={{ fontSize: "0.875rem", color: "var(--color-text-muted)", marginBottom: "1rem" }}>
            <strong>Placed:</strong> {new Date(order.createdAt).toLocaleString()}
          </p>

          <ul style={{ listStyle: "none", padding: 0, margin: "0 0 1rem 0", display: "flex", flexDirection: "column", gap: "0.4rem" }}>
            {order.items.map((item, i) => (
              <li key={i} style={{ display: "flex", justifyContent: "space-between", fontSize: "0.875rem" }}>
                <span style={{ color: "var(--color-text-muted)" }}>{item.name} ×{item.quantity}</span>
                <span style={{ fontWeight: 600 }}>ETB {item.price * item.quantity}</span>
              </li>
            ))}
          </ul>

          <div
            style={{
              borderTop: "1px solid var(--color-border)",
              paddingTop: "0.75rem",
              display: "flex",
              justifyContent: "space-between",
              fontWeight: 700,
            }}
          >
            <span>Total</span>
            <span style={{ color: "var(--color-primary)" }}>ETB {order.total}</span>
          </div>
        </div>

        <div style={{ marginTop: "1.5rem" }}>
          <Link href="/menu" className="btn btn-secondary">← Order More</Link>
        </div>
      </div>
    </div>
  );
}
