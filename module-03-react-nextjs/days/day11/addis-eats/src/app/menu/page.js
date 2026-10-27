/**
 * @file app/menu/page.js
 * @description Menu listing page with search and category filter.
 *
 * This is a Server Component. We read search params from the URL and
 * filter dishes server-side so the page is always SEO-friendly.
 *
 * URL: /menu?q=injera&category=Mains
 */

import Link from "next/link";
import { searchDishes, getCategories } from "@/lib/menu";

export const metadata = {
  title: "Menu",
  description:
    "Explore our full Ethiopian menu — doro wot, tibs, kitfo, beyaynetu, and more. Filter by category or search for your favourite dish.",
};

// ── Spice level indicator component ───────────────────────────────────────
function SpiceLevel({ level }) {
  return (
    <span title={`Spice level ${level}/3`} aria-label={`Spice level ${level} out of 3`}>
      {Array.from({ length: 3 }, (_, i) => (
        <span key={i} style={{ opacity: i < level ? 1 : 0.2 }}>
          🌶️
        </span>
      ))}
    </span>
  );
}

// ── Page component ─────────────────────────────────────────────────────────
export default async function MenuPage({ searchParams }) {
  const params = await searchParams;
  const query    = params.q        ?? "";
  const category = params.category ?? "All";

  const dishes     = searchDishes({ query, category });
  const categories = getCategories();

  return (
    <div style={{ padding: "3rem 1.5rem" }}>
      <div className="container">
        {/* Page heading */}
        <h1 style={{ fontSize: "2rem", fontWeight: 800, marginBottom: "0.5rem" }}>
          Our Menu
        </h1>
        <p style={{ color: "var(--color-text-muted)", marginBottom: "2rem" }}>
          {dishes.length} dish{dishes.length !== 1 ? "es" : ""} available
          {query && ` for "${query}"`}
          {category !== "All" && ` in ${category}`}
        </p>

        {/* Search bar */}
        <form method="GET" action="/menu" style={{ marginBottom: "1.5rem" }}>
          <div style={{ display: "flex", gap: "0.75rem", maxWidth: "480px" }}>
            <input
              type="search"
              name="q"
              defaultValue={query}
              placeholder="Search dishes…"
              style={{
                flex: 1,
                padding: "0.65rem 1rem",
                borderRadius: "var(--radius-md)",
                border: "1.5px solid var(--color-border)",
                background: "var(--color-surface)",
                color: "var(--color-text)",
                fontSize: "0.95rem",
                outline: "none",
              }}
            />
            {/* preserve category when searching */}
            <input type="hidden" name="category" value={category} />
            <button type="submit" className="btn btn-primary">
              Search
            </button>
          </div>
        </form>

        {/* Category tabs */}
        <div
          style={{
            display: "flex",
            gap: "0.5rem",
            flexWrap: "wrap",
            marginBottom: "2rem",
          }}
        >
          {categories.map((cat) => {
            const isActive = cat === category;
            return (
              <Link
                key={cat}
                href={`/menu?category=${encodeURIComponent(cat)}${query ? `&q=${encodeURIComponent(query)}` : ""}`}
                style={{
                  padding: "0.4rem 1rem",
                  borderRadius: "9999px",
                  fontWeight: isActive ? 700 : 500,
                  fontSize: "0.875rem",
                  background: isActive ? "var(--color-primary)" : "var(--color-surface)",
                  color: isActive ? "#fff" : "var(--color-text-muted)",
                  border: `1.5px solid ${isActive ? "var(--color-primary)" : "var(--color-border)"}`,
                  transition: "all 0.15s",
                }}
              >
                {cat}
              </Link>
            );
          })}
        </div>

        {/* Dish grid */}
        {dishes.length === 0 ? (
          <div style={{ textAlign: "center", padding: "4rem", color: "var(--color-text-muted)" }}>
            <div style={{ fontSize: "3rem", marginBottom: "1rem" }}>🔍</div>
            <p style={{ fontSize: "1.1rem", fontWeight: 600 }}>No dishes found.</p>
            <p>Try a different search term or category.</p>
          </div>
        ) : (
          <div
            style={{
              display: "grid",
              gridTemplateColumns: "repeat(auto-fill, minmax(260px, 1fr))",
              gap: "1.5rem",
            }}
          >
            {dishes.map((dish) => (
              <Link
                key={dish.id}
                href={`/menu/${dish.id}`}
                className="card"
                style={{ display: "block", padding: "1.25rem" }}
              >
                {/* Emoji thumbnail */}
                <div
                  style={{
                    fontSize: "3.5rem",
                    textAlign: "center",
                    padding: "1.25rem",
                    background: "var(--color-surface-alt)",
                    borderRadius: "var(--radius-md)",
                    marginBottom: "1rem",
                  }}
                >
                  {dish.emoji}
                </div>

                {/* Badges row */}
                <div style={{ display: "flex", gap: "0.4rem", marginBottom: "0.6rem", flexWrap: "wrap" }}>
                  <span className="badge badge-warning">{dish.category}</span>
                  {dish.popular && <span className="badge badge-primary">⭐ Popular</span>}
                </div>

                <h2
                  style={{
                    fontSize: "1.05rem",
                    fontWeight: 700,
                    marginBottom: "0.35rem",
                    color: "var(--color-text)",
                  }}
                >
                  {dish.name}
                </h2>

                <p
                  style={{
                    color: "var(--color-text-muted)",
                    fontSize: "0.825rem",
                    lineHeight: 1.5,
                    marginBottom: "1rem",
                    display: "-webkit-box",
                    WebkitLineClamp: 2,
                    WebkitBoxOrient: "vertical",
                    overflow: "hidden",
                  }}
                >
                  {dish.description}
                </p>

                <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between" }}>
                  <span style={{ fontWeight: 700, color: "var(--color-primary)", fontSize: "1.05rem" }}>
                    ETB {dish.price}
                  </span>
                  <SpiceLevel level={dish.spice} />
                </div>
              </Link>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
