/**
 * @file app/menu/loading.js
 * @description Streaming loading UI for the /menu route.
 *
 * Next.js automatically renders this file while the Server Component
 * (menu/page.js) is fetching data. It uses React Suspense under the hood,
 * allowing the rest of the layout to render immediately while menu data loads.
 *
 * The skeleton cards match the approximate layout of real DishCards
 * to prevent layout shift when real content arrives.
 */

function SkeletonCard() {
  return (
    <div
      style={{
        background: "var(--color-surface)",
        border: "1px solid var(--color-border)",
        borderRadius: "var(--radius-lg)",
        padding: "1.25rem",
        overflow: "hidden",
      }}
    >
      {/* Thumbnail placeholder */}
      <div
        style={{
          height: "120px",
          background: "var(--color-surface-alt)",
          borderRadius: "var(--radius-md)",
          marginBottom: "1rem",
          animation: "pulse 1.5s ease-in-out infinite",
        }}
      />
      {/* Badge placeholder */}
      <div
        style={{
          height: "20px",
          width: "60px",
          background: "var(--color-surface-alt)",
          borderRadius: "9999px",
          marginBottom: "0.6rem",
          animation: "pulse 1.5s ease-in-out infinite",
        }}
      />
      {/* Name placeholder */}
      <div
        style={{
          height: "18px",
          width: "70%",
          background: "var(--color-surface-alt)",
          borderRadius: "var(--radius-sm)",
          marginBottom: "0.5rem",
          animation: "pulse 1.5s ease-in-out infinite",
        }}
      />
      {/* Description lines */}
      {[100, 85].map((w, i) => (
        <div
          key={i}
          style={{
            height: "13px",
            width: `${w}%`,
            background: "var(--color-surface-alt)",
            borderRadius: "var(--radius-sm)",
            marginBottom: "0.4rem",
            animation: "pulse 1.5s ease-in-out infinite",
          }}
        />
      ))}
      {/* Price placeholder */}
      <div
        style={{
          marginTop: "0.75rem",
          height: "20px",
          width: "40%",
          background: "var(--color-surface-alt)",
          borderRadius: "var(--radius-sm)",
          animation: "pulse 1.5s ease-in-out infinite",
        }}
      />

      <style>{`
        @keyframes pulse {
          0%, 100% { opacity: 1; }
          50%       { opacity: 0.45; }
        }
      `}</style>
    </div>
  );
}

export default function MenuLoading() {
  return (
    <div style={{ padding: "3rem 1.5rem" }}>
      <div className="container">
        {/* Heading placeholder */}
        <div
          style={{
            height: "36px",
            width: "200px",
            background: "var(--color-surface-alt)",
            borderRadius: "var(--radius-md)",
            marginBottom: "0.5rem",
            animation: "pulse 1.5s ease-in-out infinite",
          }}
        />
        <div
          style={{
            height: "18px",
            width: "140px",
            background: "var(--color-surface-alt)",
            borderRadius: "var(--radius-sm)",
            marginBottom: "2rem",
            animation: "pulse 1.5s ease-in-out infinite",
          }}
        />

        {/* Skeleton grid */}
        <div
          style={{
            display: "grid",
            gridTemplateColumns: "repeat(auto-fill, minmax(260px, 1fr))",
            gap: "1.5rem",
          }}
        >
          {Array.from({ length: 8 }).map((_, i) => (
            <SkeletonCard key={i} />
          ))}
        </div>
      </div>
    </div>
  );
}
