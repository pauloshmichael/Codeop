"use client";

/**
 * @file app/checkout/page.js
 * @description Checkout page — customer fills in delivery details and places an order.
 *
 * Client Component because it manages form state and posts to /api/orders.
 * After a successful order it shows a confirmation with the order ID and
 * provides a link to the live order tracking page.
 *
 * For simplicity the "cart" is a hard-coded sample order.
 * In a real app you would read from a cart context or global store.
 */

import { useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";

// Sample cart items used for the checkout demo
const SAMPLE_CART = [
  { dishId: "doro-wot",  name: "Doro Wot",       price: 280, quantity: 2 },
  { dishId: "shiro-wot", name: "Shiro Wot",       price: 180, quantity: 1 },
  { dishId: "injera",    name: "Injera (×4)",      price: 30,  quantity: 4 },
  { dishId: "buna",      name: "Ethiopian Buna",   price: 50,  quantity: 2 },
];

const subtotal    = SAMPLE_CART.reduce((s, i) => s + i.price * i.quantity, 0);
const deliveryFee = 50;
const total       = subtotal + deliveryFee;

export default function CheckoutPage() {
  const router = useRouter();

  const [name,    setName]    = useState("");
  const [phone,   setPhone]   = useState("");
  const [address, setAddress] = useState("");
  const [notes,   setNotes]   = useState("");
  const [error,   setError]   = useState(null);
  const [loading, setLoading] = useState(false);
  const [orderId, setOrderId] = useState(null); // set after success

  async function handleSubmit(e) {
    e.preventDefault();
    setError(null);
    setLoading(true);

    try {
      const res = await fetch("/api/orders", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          customerName:    name,
          customerPhone:   phone,
          deliveryAddress: address,
          notes,
          items: SAMPLE_CART,
        }),
      });

      const data = await res.json();

      if (!res.ok) {
        setError(data.error ?? "Failed to place order. Please try again.");
        return;
      }

      setOrderId(data.order.id);
    } catch {
      setError("Network error. Please check your connection and try again.");
    } finally {
      setLoading(false);
    }
  }

  // ── Order Confirmation screen ────────────────────────────────────────────
  if (orderId) {
    return (
      <div style={{ padding: "4rem 1.5rem", textAlign: "center" }}>
        <div className="container" style={{ maxWidth: "480px", margin: "0 auto" }}>
          <div style={{ fontSize: "4rem", marginBottom: "1rem" }}>✅</div>
          <h1 style={{ fontSize: "1.75rem", fontWeight: 800, marginBottom: "0.5rem" }}>
            Order Placed!
          </h1>
          <p style={{ color: "var(--color-text-muted)", marginBottom: "0.5rem" }}>
            Your order <strong>{orderId}</strong> has been received and is being prepared.
          </p>
          <p style={{ color: "var(--color-text-muted)", marginBottom: "2rem" }}>
            Estimated delivery time: <strong>30–45 minutes</strong>.
          </p>
          <div style={{ display: "flex", gap: "1rem", justifyContent: "center", flexWrap: "wrap" }}>
            <Link href={`/orders/${orderId}`} className="btn btn-primary">
              Track Your Order →
            </Link>
            <Link href="/menu" className="btn btn-secondary">
              Order More
            </Link>
          </div>
        </div>
      </div>
    );
  }

  // ── Checkout Form ────────────────────────────────────────────────────────
  const inputStyle = {
    width: "100%",
    padding: "0.65rem 0.9rem",
    borderRadius: "var(--radius-md)",
    border: "1.5px solid var(--color-border)",
    background: "var(--color-surface)",
    color: "var(--color-text)",
    fontSize: "0.95rem",
  };

  const labelStyle = {
    display: "block",
    fontWeight: 600,
    marginBottom: "0.4rem",
    fontSize: "0.875rem",
  };

  return (
    <div style={{ padding: "3rem 1.5rem" }}>
      <div
        className="container"
        style={{
          display: "grid",
          gridTemplateColumns: "1fr min(380px, 100%)",
          gap: "2rem",
          alignItems: "start",
          maxWidth: "900px",
        }}
      >
        {/* ── Left: Form ─────────────────────────────────────────────── */}
        <div>
          <h1 style={{ fontSize: "1.75rem", fontWeight: 800, marginBottom: "1.5rem" }}>
            Checkout
          </h1>

          {error && (
            <div
              role="alert"
              style={{
                background: "#fde8e6",
                color: "#c0392b",
                borderRadius: "var(--radius-md)",
                padding: "0.75rem 1rem",
                marginBottom: "1rem",
                fontSize: "0.9rem",
              }}
            >
              ⚠ {error}
            </div>
          )}

          <form
            onSubmit={handleSubmit}
            style={{ display: "flex", flexDirection: "column", gap: "1.1rem" }}
          >
            <div>
              <label htmlFor="co-name" style={labelStyle}>Full Name *</label>
              <input
                id="co-name"
                type="text"
                value={name}
                onChange={(e) => setName(e.target.value)}
                required
                placeholder="Your full name"
                style={inputStyle}
              />
            </div>

            <div>
              <label htmlFor="co-phone" style={labelStyle}>Phone Number</label>
              <input
                id="co-phone"
                type="tel"
                value={phone}
                onChange={(e) => setPhone(e.target.value)}
                placeholder="09XXXXXXXX"
                style={inputStyle}
              />
            </div>

            <div>
              <label htmlFor="co-address" style={labelStyle}>Delivery Address *</label>
              <input
                id="co-address"
                type="text"
                value={address}
                onChange={(e) => setAddress(e.target.value)}
                required
                placeholder="Kebele, sub-city, Addis Ababa"
                style={inputStyle}
              />
            </div>

            <div>
              <label htmlFor="co-notes" style={labelStyle}>Order Notes (optional)</label>
              <textarea
                id="co-notes"
                value={notes}
                onChange={(e) => setNotes(e.target.value)}
                rows={3}
                placeholder="Extra injera, no onions, etc."
                style={{ ...inputStyle, resize: "vertical" }}
              />
            </div>

            <button
              type="submit"
              disabled={loading}
              className="btn btn-primary"
              style={{ width: "100%", opacity: loading ? 0.7 : 1 }}
            >
              {loading ? "Placing order…" : `Place Order — ETB ${total}`}
            </button>
          </form>
        </div>

        {/* ── Right: Order Summary ─────────────────────────────────────── */}
        <div className="card" style={{ padding: "1.5rem", position: "sticky", top: "6rem" }}>
          <h2 style={{ fontWeight: 700, fontSize: "1.05rem", marginBottom: "1rem" }}>
            Order Summary
          </h2>

          <ul style={{ listStyle: "none", padding: 0, margin: 0, display: "flex", flexDirection: "column", gap: "0.6rem" }}>
            {SAMPLE_CART.map((item) => (
              <li
                key={item.dishId}
                style={{ display: "flex", justifyContent: "space-between", fontSize: "0.9rem" }}
              >
                <span style={{ color: "var(--color-text-muted)" }}>
                  {item.name} ×{item.quantity}
                </span>
                <span style={{ fontWeight: 600 }}>ETB {item.price * item.quantity}</span>
              </li>
            ))}
          </ul>

          <div
            style={{
              borderTop: "1px solid var(--color-border)",
              marginTop: "1rem",
              paddingTop: "1rem",
              display: "flex",
              flexDirection: "column",
              gap: "0.4rem",
              fontSize: "0.9rem",
            }}
          >
            <div style={{ display: "flex", justifyContent: "space-between" }}>
              <span style={{ color: "var(--color-text-muted)" }}>Subtotal</span>
              <span>ETB {subtotal}</span>
            </div>
            <div style={{ display: "flex", justifyContent: "space-between" }}>
              <span style={{ color: "var(--color-text-muted)" }}>Delivery fee</span>
              <span>ETB {deliveryFee}</span>
            </div>
            <div
              style={{
                display: "flex",
                justifyContent: "space-between",
                fontWeight: 700,
                fontSize: "1rem",
                marginTop: "0.35rem",
              }}
            >
              <span>Total</span>
              <span style={{ color: "var(--color-primary)" }}>ETB {total}</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
