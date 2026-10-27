"use client";

/**
 * @file app/auth/signin/page.js
 * @description Sign-in page — client component that submits credentials
 * to POST /api/auth/signin and redirects on success.
 *
 * "use client" is required because we use React state and browser
 * event handlers (form submit, useState, useRouter).
 */

import { useState } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";

export default function SignInPage() {
  const router = useRouter();

  const [name,     setName]     = useState("");
  const [password, setPassword] = useState("");
  const [error,    setError]    = useState(null);
  const [loading,  setLoading]  = useState(false);

  async function handleSubmit(e) {
    e.preventDefault();
    setError(null);
    setLoading(true);

    try {
      const res = await fetch("/api/auth/signin", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ name, password }),
      });

      const data = await res.json();

      if (!res.ok) {
        setError(data.error ?? "Sign-in failed. Please try again.");
        return;
      }

      // Redirect based on role
      if (data.role === "staff") {
        router.push("/kitchen");
      } else {
        router.push("/menu");
      }
      router.refresh(); // re-render server components to pick up new cookie
    } catch {
      setError("Network error. Please check your connection.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div
      style={{
        minHeight: "80vh",
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        padding: "2rem 1.5rem",
      }}
    >
      <div style={{ width: "100%", maxWidth: "400px" }}>
        {/* Logo */}
        <div style={{ textAlign: "center", marginBottom: "2rem" }}>
          <div style={{ fontSize: "3rem", marginBottom: "0.5rem" }}>🍛</div>
          <h1 style={{ fontSize: "1.5rem", fontWeight: 800 }}>Sign in to Addis Eats</h1>
          <p style={{ color: "var(--color-text-muted)", marginTop: "0.35rem" }}>
            Access your orders or the kitchen dashboard.
          </p>
        </div>

        {/* Demo credentials hint */}
        <div
          style={{
            background: "var(--color-surface-alt)",
            border: "1px solid var(--color-border)",
            borderRadius: "var(--radius-md)",
            padding: "0.85rem 1rem",
            marginBottom: "1.5rem",
            fontSize: "0.825rem",
            color: "var(--color-text-muted)",
          }}
        >
          <strong>Demo credentials:</strong>
          <br />
          Customer: <code>customer / customer123</code>
          <br />
          Staff: <code>staff / kitchen456</code>
        </div>

        {/* Error message */}
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
              fontWeight: 500,
            }}
          >
            ⚠ {error}
          </div>
        )}

        {/* Sign-in form */}
        <form
          onSubmit={handleSubmit}
          className="card"
          style={{ padding: "1.75rem", display: "flex", flexDirection: "column", gap: "1rem" }}
        >
          <div>
            <label
              htmlFor="signin-name"
              style={{ display: "block", fontWeight: 600, marginBottom: "0.4rem", fontSize: "0.9rem" }}
            >
              Username
            </label>
            <input
              id="signin-name"
              type="text"
              value={name}
              onChange={(e) => setName(e.target.value)}
              required
              autoComplete="username"
              placeholder="customer or staff"
              style={{
                width: "100%",
                padding: "0.65rem 0.9rem",
                borderRadius: "var(--radius-md)",
                border: "1.5px solid var(--color-border)",
                background: "var(--color-surface)",
                color: "var(--color-text)",
                fontSize: "0.95rem",
              }}
            />
          </div>

          <div>
            <label
              htmlFor="signin-password"
              style={{ display: "block", fontWeight: 600, marginBottom: "0.4rem", fontSize: "0.9rem" }}
            >
              Password
            </label>
            <input
              id="signin-password"
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
              autoComplete="current-password"
              placeholder="••••••••"
              style={{
                width: "100%",
                padding: "0.65rem 0.9rem",
                borderRadius: "var(--radius-md)",
                border: "1.5px solid var(--color-border)",
                background: "var(--color-surface)",
                color: "var(--color-text)",
                fontSize: "0.95rem",
              }}
            />
          </div>

          <button
            type="submit"
            disabled={loading}
            className="btn btn-primary"
            style={{ width: "100%", opacity: loading ? 0.7 : 1, cursor: loading ? "not-allowed" : "pointer" }}
          >
            {loading ? "Signing in…" : "Sign In"}
          </button>
        </form>

        <p style={{ textAlign: "center", marginTop: "1.25rem", fontSize: "0.875rem", color: "var(--color-text-muted)" }}>
          <Link href="/" style={{ color: "var(--color-primary)" }}>← Back to Home</Link>
        </p>
      </div>
    </div>
  );
}
