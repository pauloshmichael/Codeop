/**
 * @file app/page.js
 * @description Addis Eats home page — hero, featured dishes, and about section.
 *
 * This is a Server Component. It imports the dish catalog directly
 * (no network round-trip needed) and renders a static, SEO-friendly page.
 */

import Link from "next/link";
import { dishes } from "@/lib/menu";

export const metadata = {
  title: "Home",
  description:
    "Order authentic Ethiopian cuisine — injera, doro wot, tibs, kitfo and more — delivered fresh to your door in Addis Ababa.",
};

export default function HomePage() {
  // Pick three popular dishes for the featured section
  const featured = dishes.filter((d) => d.popular).slice(0, 3);

  return (
    <>
      {/* ── Hero ──────────────────────────────────────────────────────── */}
      <section
        style={{
          background: "linear-gradient(135deg, #c0392b 0%, #96281b 50%, #6d1a12 100%)",
          color: "#fff",
          padding: "5rem 1.5rem",
          textAlign: "center",
        }}
      >
        <div style={{ maxWidth: "700px", margin: "0 auto" }}>
          <div style={{ fontSize: "4rem", marginBottom: "1rem" }}>🍛</div>
          <h1
            style={{
              fontSize: "clamp(2rem, 5vw, 3.5rem)",
              fontWeight: 800,
              lineHeight: 1.1,
              marginBottom: "1.25rem",
              letterSpacing: "-0.02em",
            }}
          >
            Authentic Ethiopian
            <br />
            Food, Delivered Fresh
          </h1>
          <p
            style={{
              fontSize: "1.15rem",
              opacity: 0.9,
              maxWidth: "520px",
              margin: "0 auto 2.5rem",
              lineHeight: 1.7,
            }}
          >
            From slow-simmered doro wot to the grand beyaynetu platter — every dish
            crafted with traditional spices and served on house-made injera.
          </p>
          <div style={{ display: "flex", gap: "1rem", justifyContent: "center", flexWrap: "wrap" }}>
            <Link
              href="/menu"
              style={{
                background: "#fff",
                color: "#c0392b",
                fontWeight: 700,
                padding: "0.85rem 2rem",
                borderRadius: "9999px",
                fontSize: "1rem",
                transition: "transform 0.2s",
                display: "inline-block",
              }}
            >
              Browse Menu →
            </Link>
            <Link
              href="/auth/signin"
              style={{
                background: "transparent",
                color: "#fff",
                fontWeight: 600,
                padding: "0.85rem 2rem",
                borderRadius: "9999px",
                fontSize: "1rem",
                border: "2px solid rgba(255,255,255,0.5)",
                display: "inline-block",
              }}
            >
              Sign In
            </Link>
          </div>
        </div>
      </section>

      {/* ── Feature Badges ─────────────────────────────────────────────── */}
      <section style={{ background: "var(--color-surface-alt)", padding: "2rem 1.5rem" }}>
        <div
          className="container"
          style={{
            display: "flex",
            justifyContent: "center",
            gap: "2.5rem",
            flexWrap: "wrap",
            textAlign: "center",
          }}
        >
          {[
            { icon: "⚡", label: "30-min delivery" },
            { icon: "🌿", label: "Fresh ingredients" },
            { icon: "🫓", label: "House-made injera" },
            { icon: "🌶️", label: "Customisable spice" },
          ].map(({ icon, label }) => (
            <div key={label} style={{ display: "flex", alignItems: "center", gap: "0.5rem" }}>
              <span style={{ fontSize: "1.4rem" }}>{icon}</span>
              <span style={{ fontWeight: 600, color: "var(--color-text-muted)" }}>{label}</span>
            </div>
          ))}
        </div>
      </section>

      {/* ── Featured Dishes ────────────────────────────────────────────── */}
      <section style={{ padding: "4rem 1.5rem" }}>
        <div className="container">
          <h2
            style={{
              fontSize: "1.75rem",
              fontWeight: 700,
              marginBottom: "0.5rem",
              color: "var(--color-text)",
            }}
          >
            Popular Right Now
          </h2>
          <p style={{ color: "var(--color-text-muted)", marginBottom: "2rem" }}>
            Our most-loved Ethiopian classics, ready to order.
          </p>

          <div
            style={{
              display: "grid",
              gridTemplateColumns: "repeat(auto-fill, minmax(260px, 1fr))",
              gap: "1.5rem",
            }}
          >
            {featured.map((dish) => (
              <Link
                key={dish.id}
                href={`/menu/${dish.id}`}
                className="card"
                style={{ display: "block", padding: "1.5rem" }}
              >
                <div style={{ fontSize: "3rem", marginBottom: "1rem", textAlign: "center" }}>
                  {dish.emoji}
                </div>
                <h3 style={{ fontWeight: 700, fontSize: "1.1rem", marginBottom: "0.35rem" }}>
                  {dish.name}
                </h3>
                <p
                  style={{
                    color: "var(--color-text-muted)",
                    fontSize: "0.875rem",
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
                  <span
                    style={{ fontWeight: 700, color: "var(--color-primary)", fontSize: "1.1rem" }}
                  >
                    ETB {dish.price}
                  </span>
                  <span className="badge badge-primary">⭐ Popular</span>
                </div>
              </Link>
            ))}
          </div>

          <div style={{ textAlign: "center", marginTop: "2.5rem" }}>
            <Link href="/menu" className="btn btn-primary">
              View Full Menu →
            </Link>
          </div>
        </div>
      </section>

      {/* ── About ──────────────────────────────────────────────────────── */}
      <section
        style={{
          background: "var(--color-surface-alt)",
          borderTop: "1px solid var(--color-border)",
          padding: "4rem 1.5rem",
        }}
      >
        <div
          className="container"
          style={{ display: "flex", gap: "3rem", alignItems: "center", flexWrap: "wrap" }}
        >
          <div style={{ flex: "1 1 280px", fontSize: "5rem", textAlign: "center" }}>
            🫕
          </div>
          <div style={{ flex: "2 1 320px" }}>
            <h2 style={{ fontSize: "1.75rem", fontWeight: 700, marginBottom: "1rem" }}>
              Cooked with Love in Addis
            </h2>
            <p style={{ color: "var(--color-text-muted)", lineHeight: 1.8, marginBottom: "1rem" }}>
              Every dish on our menu follows time-honoured recipes passed down through
              generations. We use hand-ground berbere spice blends, slow-fermented teff
              injera, and fresh local produce sourced daily from Merkato market.
            </p>
            <p style={{ color: "var(--color-text-muted)", lineHeight: 1.8 }}>
              Whether you are celebrating a special occasion with a full beyaynetu platter
              or craving the comfort of firfir on a lazy morning, Addis Eats brings the
              taste of Ethiopia to your doorstep.
            </p>
          </div>
        </div>
      </section>
    </>
  );
}
