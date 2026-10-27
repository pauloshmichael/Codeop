/**
 * @file app/not-found.js
 * @description Custom 404 page for Addis Eats.
 *
 * Next.js automatically renders this file when notFound() is called
 * from a Server Component, or when the URL doesn't match any route.
 *
 * This is a Server Component (no "use client" needed).
 */

import Link from "next/link";

export const metadata = {
  title: "404 — Page not found",
};

export default function NotFound() {
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
      <div style={{ fontSize: "5rem", marginBottom: "1rem" }}>🍛</div>
      <h1
        style={{
          fontSize: "5rem",
          fontWeight: 900,
          color: "var(--color-primary)",
          lineHeight: 1,
          marginBottom: "0.5rem",
        }}
      >
        404
      </h1>
      <h2 style={{ fontSize: "1.5rem", fontWeight: 700, marginBottom: "0.75rem" }}>
        Dish Not Found
      </h2>
      <p style={{ color: "var(--color-text-muted)", maxWidth: "400px", lineHeight: 1.7, marginBottom: "2rem" }}>
        It looks like the page you're looking for has left the kitchen. 
        Head back to our menu to find something delicious.
      </p>
      <div style={{ display: "flex", gap: "1rem", flexWrap: "wrap", justifyContent: "center" }}>
        <Link href="/" className="btn btn-primary">Go Home</Link>
        <Link href="/menu" className="btn btn-secondary">Browse Menu</Link>
      </div>
    </div>
  );
}
