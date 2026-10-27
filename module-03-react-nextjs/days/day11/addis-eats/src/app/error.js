"use client";

/**
 * @file app/error.js
 * @description Global error boundary for Addis Eats.
 *
 * Next.js renders this component when an uncaught error is thrown inside
 * any Server or Client Component in the same layout segment.
 *
 * MUST be a Client Component ("use client") — Next.js requires error
 * boundaries to be client-side so they can use the `reset` callback.
 *
 * Props:
 *   error  — the Error object that was thrown
 *   reset  — function to retry rendering the erroring segment
 */

export default function GlobalError({ error, reset }) {
  return (
    <div
      style={{
        minHeight: "70vh",
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        justifyContent: "center",
        padding: "3rem 1.5rem",
        textAlign: "center",
      }}
    >
      <div style={{ fontSize: "4rem", marginBottom: "1rem" }}>😵</div>
      <h1 style={{ fontSize: "1.75rem", fontWeight: 800, marginBottom: "0.5rem" }}>
        Something went wrong
      </h1>
      <p style={{ color: "var(--color-text-muted)", maxWidth: "420px", lineHeight: 1.7, marginBottom: "0.5rem" }}>
        The kitchen ran into an unexpected problem. Our chefs are on it!
      </p>
      {process.env.NODE_ENV === "development" && (
        <pre
          style={{
            background: "var(--color-surface-alt)",
            border: "1px solid var(--color-border)",
            borderRadius: "var(--radius-md)",
            padding: "1rem",
            maxWidth: "600px",
            overflowX: "auto",
            fontSize: "0.75rem",
            textAlign: "left",
            marginBottom: "1.5rem",
            color: "#c0392b",
          }}
        >
          {error?.message}
        </pre>
      )}
      <div style={{ display: "flex", gap: "1rem", flexWrap: "wrap", justifyContent: "center", marginTop: "1rem" }}>
        <button onClick={reset} className="btn btn-primary">
          Try Again
        </button>
        <a href="/" className="btn btn-secondary">
          Go Home
        </a>
      </div>
    </div>
  );
}
