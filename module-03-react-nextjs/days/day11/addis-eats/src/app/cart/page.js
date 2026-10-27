"use client";

/**
 * @file app/cart/page.js
 * @description Shopping cart page — displays current cart items,
 * allows quantity adjustment, and links to checkout.
 *
 * For Day 36 the cart is a hard-coded demo (same as checkout).
 * In a real app the cart state would live in React Context or Zustand,
 * persisted to localStorage.
 */

import { useState } from "react";
import Link from "next/link";

const INITIAL_CART = [
  { dishId: "doro-wot",  name: "Doro Wot",       emoji: "🍗", price: 280, quantity: 2 },
  { dishId: "shiro-wot", name: "Shiro Wot",       emoji: "🫘", price: 180, quantity: 1 },
  { dishId: "injera",    name: "Injera",           emoji: "🫓", price: 30,  quantity: 4 },
  { dishId: "buna",      name: "Ethiopian Buna",   emoji: "☕", price: 50,  quantity: 2 },
];

const DELIVERY_FEE = 50;

export default function CartPage() {
  const [cart, setCart] = useState(INITIAL_CART);

  function updateQty(dishId, delta) {
    setCart((prev) =>
      prev
        .map((item) =>
          item.dishId === dishId
            ? { ...item, quantity: Math.max(0, item.quantity + delta) }
            : item
        )
        .filter((item) => item.quantity > 0)
    );
  }

  function removeItem(dishId) {
    setCart((prev) => prev.filter((item) => item.dishId !== dishId));
  }

  const subtotal = cart.reduce((s, i) => s + i.price * i.quantity, 0);
  const total    = subtotal + DELIVERY_FEE;

  // ── Empty cart ─────────────────────────────────────────────────────────
  if (cart.length === 0) {
    return (
      <div style={{ padding: "6rem 1.5rem", textAlign: "center" }}>
        <div style={{ fontSize: "4rem", marginBottom: "1rem" }}>🛒</div>
        <h1 style={{ fontSize: "1.5rem", fontWeight: 700, marginBottom: "0.5rem" }}>
          Your cart is empty
        </h1>
        <p style={{ color: "var(--color-text-muted)", marginBottom: "2rem" }}>
          Browse the menu and add your favourite Ethiopian dishes.
        </p>
        <Link href="/menu" className="btn btn-primary">Browse Menu →</Link>
      </div>
    );
  }

  return (
    <div style={{ padding: "3rem 1.5rem" }}>
      <div
        className="container"
        style={{
          display: "grid",
          gridTemplateColumns: "1fr min(360px, 100%)",
          gap: "2rem",
          alignItems: "start",
          maxWidth: "900px",
        }}
      >
        {/* ── Left: Cart items ──────────────────────────────────────── */}
        <div>
          <h1 style={{ fontSize: "1.75rem", fontWeight: 800, marginBottom: "1.5rem" }}>
            🛒 Your Cart
          </h1>

          <div style={{ display: "flex", flexDirection: "column", gap: "1rem" }}>
            {cart.map((item) => (
              <div
                key={item.dishId}
                className="card"
                style={{
                  padding: "1rem 1.25rem",
                  display: "flex",
                  alignItems: "center",
                  gap: "1rem",
                }}
              >
                {/* Emoji */}
                <div
                  style={{
                    fontSize: "2.5rem",
                    padding: "0.5rem",
                    background: "var(--color-surface-alt)",
                    borderRadius: "var(--radius-md)",
                    minWidth: "3.5rem",
                    textAlign: "center",
                  }}
                >
                  {item.emoji}
                </div>

                {/* Name & price */}
                <div style={{ flex: 1 }}>
                  <p style={{ fontWeight: 600, marginBottom: "0.15rem" }}>{item.name}</p>
                  <p style={{ fontSize: "0.875rem", color: "var(--color-text-muted)" }}>
                    ETB {item.price} each
                  </p>
                </div>

                {/* Quantity controls */}
                <div style={{ display: "flex", alignItems: "center", gap: "0.5rem" }}>
                  <button
                    onClick={() => updateQty(item.dishId, -1)}
                    aria-label={`Decrease quantity of ${item.name}`}
                    style={{
                      width: "2rem",
                      height: "2rem",
                      borderRadius: "50%",
                      border: "1.5px solid var(--color-border)",
                      background: "var(--color-surface)",
                      cursor: "pointer",
                      fontWeight: 700,
                      fontSize: "1rem",
                    }}
                  >
                    −
                  </button>
                  <span style={{ minWidth: "1.5rem", textAlign: "center", fontWeight: 600 }}>
                    {item.quantity}
                  </span>
                  <button
                    onClick={() => updateQty(item.dishId, +1)}
                    aria-label={`Increase quantity of ${item.name}`}
                    style={{
                      width: "2rem",
                      height: "2rem",
                      borderRadius: "50%",
                      border: "1.5px solid var(--color-border)",
                      background: "var(--color-surface)",
                      cursor: "pointer",
                      fontWeight: 700,
                      fontSize: "1rem",
                    }}
                  >
                    +
                  </button>
                </div>

                {/* Line total */}
                <p style={{ fontWeight: 700, minWidth: "5rem", textAlign: "right", color: "var(--color-primary)" }}>
                  ETB {item.price * item.quantity}
                </p>

                {/* Remove */}
                <button
                  onClick={() => removeItem(item.dishId)}
                  aria-label={`Remove ${item.name} from cart`}
                  style={{
                    background: "none",
                    border: "none",
                    cursor: "pointer",
                    color: "var(--color-text-light)",
                    fontSize: "1.1rem",
                    padding: "0.25rem",
                  }}
                >
                  ✕
                </button>
              </div>
            ))}
          </div>

          <Link
            href="/menu"
            style={{
              display: "inline-flex",
              alignItems: "center",
              gap: "0.3rem",
              color: "var(--color-text-muted)",
              fontSize: "0.875rem",
              marginTop: "1.25rem",
            }}
          >
            + Add more dishes
          </Link>
        </div>

        {/* ── Right: Order summary ─────────────────────────────────── */}
        <div className="card" style={{ padding: "1.5rem", position: "sticky", top: "6rem" }}>
          <h2 style={{ fontWeight: 700, fontSize: "1.05rem", marginBottom: "1rem" }}>
            Summary
          </h2>

          <div style={{ display: "flex", flexDirection: "column", gap: "0.5rem", fontSize: "0.9rem", marginBottom: "1rem" }}>
            <div style={{ display: "flex", justifyContent: "space-between" }}>
              <span style={{ color: "var(--color-text-muted)" }}>
                {cart.length} item{cart.length !== 1 ? "s" : ""}
              </span>
              <span>ETB {subtotal}</span>
            </div>
            <div style={{ display: "flex", justifyContent: "space-between" }}>
              <span style={{ color: "var(--color-text-muted)" }}>Delivery</span>
              <span>ETB {DELIVERY_FEE}</span>
            </div>
          </div>

          <div
            style={{
              borderTop: "1px solid var(--color-border)",
              paddingTop: "0.75rem",
              display: "flex",
              justifyContent: "space-between",
              fontWeight: 700,
              fontSize: "1.05rem",
              marginBottom: "1.25rem",
            }}
          >
            <span>Total</span>
            <span style={{ color: "var(--color-primary)" }}>ETB {total}</span>
          </div>

          <Link href="/checkout" className="btn btn-primary" style={{ width: "100%", display: "flex", justifyContent: "center" }}>
            Proceed to Checkout →
          </Link>
        </div>
      </div>
    </div>
  );
}
