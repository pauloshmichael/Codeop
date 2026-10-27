/**
 * @file components/DishCard.jsx
 * @description Reusable dish card component used on the menu listing page.
 *
 * Renders a card with:
 *  - Emoji thumbnail with coloured background
 *  - Category and "Popular" badges
 *  - Dish name, truncated description
 *  - Price (in ETB) and spice level indicator
 *
 * Props:
 *   dish    — dish object from src/lib/menu.js
 *   href    — link destination (defaults to /menu/:id)
 *
 * This is a Server Component by default (no "use client").
 * If you need click handlers, wrap it in a client component.
 */

import Link from "next/link";

function SpiceDots({ level }) {
  return (
    <span aria-label={`Spice level ${level} of 3`} title={`Spice: ${level}/3`}>
      {[0, 1, 2].map((i) => (
        <span key={i} style={{ opacity: i < level ? 1 : 0.2, fontSize: "0.8rem" }}>
          🌶️
        </span>
      ))}
    </span>
  );
}

export default function DishCard({ dish, href }) {
  const destination = href ?? `/menu/${dish.id}`;

  return (
    <Link
      href={destination}
      className="card"
      style={{ display: "flex", flexDirection: "column", padding: "1.25rem" }}
    >
      {/* Emoji thumbnail */}
      <div
        style={{
          fontSize: "3.5rem",
          textAlign: "center",
          padding: "1.25rem 1rem",
          background: "var(--color-surface-alt)",
          borderRadius: "var(--radius-md)",
          marginBottom: "1rem",
          lineHeight: 1,
        }}
      >
        {dish.emoji}
      </div>

      {/* Badges */}
      <div
        style={{
          display: "flex",
          gap: "0.4rem",
          flexWrap: "wrap",
          marginBottom: "0.6rem",
        }}
      >
        <span className="badge badge-warning" style={{ fontSize: "0.7rem" }}>
          {dish.category}
        </span>
        {dish.popular && (
          <span className="badge badge-primary" style={{ fontSize: "0.7rem" }}>
            ⭐ Popular
          </span>
        )}
      </div>

      {/* Name */}
      <h3
        style={{
          fontWeight: 700,
          fontSize: "1rem",
          marginBottom: "0.35rem",
          color: "var(--color-text)",
        }}
      >
        {dish.name}
      </h3>

      {/* Description — clamped to 2 lines */}
      <p
        style={{
          color: "var(--color-text-muted)",
          fontSize: "0.825rem",
          lineHeight: 1.55,
          marginBottom: "1rem",
          flex: 1,
          display: "-webkit-box",
          WebkitLineClamp: 2,
          WebkitBoxOrient: "vertical",
          overflow: "hidden",
        }}
      >
        {dish.description}
      </p>

      {/* Footer: price + spice */}
      <div
        style={{
          display: "flex",
          alignItems: "center",
          justifyContent: "space-between",
          marginTop: "auto",
        }}
      >
        <span
          style={{
            fontWeight: 700,
            color: "var(--color-primary)",
            fontSize: "1.05rem",
          }}
        >
          ETB {dish.price}
        </span>
        <SpiceDots level={dish.spice} />
      </div>

      {/* Prep time */}
      <p
        style={{
          fontSize: "0.75rem",
          color: "var(--color-text-light)",
          marginTop: "0.4rem",
        }}
      >
        ⏱ {dish.time} min
      </p>
    </Link>
  );
}
