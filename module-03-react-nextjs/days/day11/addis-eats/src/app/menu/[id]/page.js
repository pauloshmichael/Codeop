/**
 * @file app/menu/[id]/page.js
 * @description Individual dish detail page.
 *
 * Dynamic route: /menu/doro-wot, /menu/tibs, etc.
 *
 * Demonstrates:
 *  - Dynamic route segments with `params`
 *  - generateMetadata for per-page SEO titles
 *  - generateStaticParams to pre-render all dish pages at build time
 *  - notFound() for unknown dish IDs
 */

import Link from "next/link";
import { notFound } from "next/navigation";
import { getDishById, dishes } from "@/lib/menu";

// ── Static Generation ──────────────────────────────────────────────────────
/**
 * Pre-generates a static page for every dish at build time.
 * Next.js will call this function to get the list of all possible params.
 */
export function generateStaticParams() {
  return dishes.map((dish) => ({ id: dish.id }));
}

// ── Per-page SEO metadata ──────────────────────────────────────────────────
export async function generateMetadata({ params }) {
  const { id } = await params;
  const dish = getDishById(id);
  if (!dish) return { title: "Dish not found" };

  return {
    title: dish.name,
    description: dish.description,
  };
}

// ── Spice level display ────────────────────────────────────────────────────
const SPICE_LABELS = ["Not spicy", "Mild", "Medium", "Hot 🔥"];

// ── Page ───────────────────────────────────────────────────────────────────
export default async function DishDetailPage({ params }) {
  const { id } = await params;
  const dish = getDishById(id);

  if (!dish) notFound();

  return (
    <div style={{ padding: "3rem 1.5rem" }}>
      <div className="container" style={{ maxWidth: "760px" }}>
        {/* Back link */}
        <Link
          href="/menu"
          style={{
            color: "var(--color-text-muted)",
            fontSize: "0.9rem",
            display: "inline-flex",
            alignItems: "center",
            gap: "0.25rem",
            marginBottom: "1.5rem",
          }}
        >
          ← Back to Menu
        </Link>

        {/* Card */}
        <div className="card" style={{ padding: "2rem" }}>
          {/* Emoji hero */}
          <div
            style={{
              fontSize: "6rem",
              textAlign: "center",
              padding: "2.5rem",
              background: "var(--color-surface-alt)",
              borderRadius: "var(--radius-lg)",
              marginBottom: "1.5rem",
            }}
          >
            {dish.emoji}
          </div>

          {/* Badges */}
          <div style={{ display: "flex", gap: "0.5rem", flexWrap: "wrap", marginBottom: "0.75rem" }}>
            <span className="badge badge-warning">{dish.category}</span>
            {dish.popular && <span className="badge badge-primary">⭐ Popular</span>}
          </div>

          {/* Name & price */}
          <div
            style={{
              display: "flex",
              alignItems: "flex-start",
              justifyContent: "space-between",
              gap: "1rem",
              flexWrap: "wrap",
              marginBottom: "1rem",
            }}
          >
            <h1 style={{ fontSize: "1.75rem", fontWeight: 800 }}>{dish.name}</h1>
            <span
              style={{
                fontSize: "1.6rem",
                fontWeight: 800,
                color: "var(--color-primary)",
                whiteSpace: "nowrap",
              }}
            >
              ETB {dish.price}
            </span>
          </div>

          {/* Description */}
          <p
            style={{
              color: "var(--color-text-muted)",
              lineHeight: 1.8,
              fontSize: "1rem",
              marginBottom: "1.5rem",
            }}
          >
            {dish.description}
          </p>

          {/* Stats row */}
          <div
            style={{
              display: "flex",
              gap: "2rem",
              flexWrap: "wrap",
              paddingBlock: "1rem",
              borderTop: "1px solid var(--color-border)",
              borderBottom: "1px solid var(--color-border)",
              marginBottom: "1.5rem",
            }}
          >
            <div>
              <p style={{ fontSize: "0.75rem", color: "var(--color-text-light)", marginBottom: "0.2rem", textTransform: "uppercase", letterSpacing: "0.06em" }}>
                Spice Level
              </p>
              <p style={{ fontWeight: 600 }}>{SPICE_LABELS[dish.spice]}</p>
            </div>
            <div>
              <p style={{ fontSize: "0.75rem", color: "var(--color-text-light)", marginBottom: "0.2rem", textTransform: "uppercase", letterSpacing: "0.06em" }}>
                Prep Time
              </p>
              <p style={{ fontWeight: 600 }}>⏱ {dish.time} min</p>
            </div>
            <div>
              <p style={{ fontSize: "0.75rem", color: "var(--color-text-light)", marginBottom: "0.2rem", textTransform: "uppercase", letterSpacing: "0.06em" }}>
                Category
              </p>
              <p style={{ fontWeight: 600 }}>{dish.category}</p>
            </div>
          </div>

          {/* Actions */}
          <div style={{ display: "flex", gap: "1rem", flexWrap: "wrap" }}>
            <Link href="/checkout" className="btn btn-primary" style={{ flex: "1", justifyContent: "center" }}>
              Order Now — ETB {dish.price}
            </Link>
            <Link href="/menu" className="btn btn-secondary">
              ← Menu
            </Link>
          </div>
        </div>
      </div>
    </div>
  );
}
