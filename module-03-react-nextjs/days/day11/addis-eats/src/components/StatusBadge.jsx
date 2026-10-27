/**
 * @file components/StatusBadge.jsx
 * @description Reusable order status badge component.
 *
 * Renders a coloured pill badge for an order status string.
 * Used by the kitchen dashboard, order tracking page, and any other
 * place that displays order status.
 *
 * Supported statuses:
 *   pending | preparing | ready | delivering | delivered | cancelled
 *
 * Props:
 *   status  — string (one of the above)
 *   size    — "sm" | "md" (default "md")
 *
 * This is a Server Component — no "use client" needed.
 */

const STATUS_CONFIG = {
  pending: {
    label: "Pending",
    bg: "#fdebd0",
    color: "#a04000",
    icon: "📋",
  },
  preparing: {
    label: "Preparing",
    bg: "#d5f5e3",
    color: "#1e8449",
    icon: "👨‍🍳",
  },
  ready: {
    label: "Ready",
    bg: "#d6eaf8",
    color: "#1a5276",
    icon: "✅",
  },
  delivering: {
    label: "Delivering",
    bg: "#e8daef",
    color: "#6c3483",
    icon: "🛵",
  },
  delivered: {
    label: "Delivered",
    bg: "#eaecee",
    color: "#5d6d7e",
    icon: "🏠",
  },
  cancelled: {
    label: "Cancelled",
    bg: "#fde8e6",
    color: "#c0392b",
    icon: "❌",
  },
};

export default function StatusBadge({ status, size = "md" }) {
  const config = STATUS_CONFIG[status] ?? {
    label: status,
    bg: "#eaecee",
    color: "#5d6d7e",
    icon: "❓",
  };

  const paddingMap = { sm: "0.15rem 0.5rem", md: "0.25rem 0.75rem" };
  const fontSizeMap = { sm: "0.7rem", md: "0.8rem" };

  return (
    <span
      style={{
        display: "inline-flex",
        alignItems: "center",
        gap: "0.3rem",
        padding: paddingMap[size] ?? paddingMap.md,
        borderRadius: "9999px",
        background: config.bg,
        color: config.color,
        fontWeight: 600,
        fontSize: fontSizeMap[size] ?? fontSizeMap.md,
        letterSpacing: "0.02em",
        whiteSpace: "nowrap",
      }}
      aria-label={`Order status: ${config.label}`}
    >
      <span aria-hidden="true">{config.icon}</span>
      {config.label}
    </span>
  );
}
