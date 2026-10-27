import { Geist, Geist_Mono } from "next/font/google";
import Link from "next/link";
import SWRProvider from "@/components/SWRProvider";
import "./globals.css";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const metadata = {
  title: {
    template: "%s | Addis Eats",
    default: "Addis Eats — Ethiopian Food Delivery",
  },
  description:
    "Order authentic Ethiopian dishes — injera, tibs, kitfo, and more — delivered fresh to your door in Addis Ababa.",
  keywords: ["Ethiopian food", "food delivery", "injera", "Addis Ababa", "restaurant"],
};

export default function RootLayout({ children }) {
  return (
    <html
      lang="en"
      className={`${geistSans.variable} ${geistMono.variable} h-full antialiased`}
    >
      <body className="min-h-full flex flex-col" style={{ background: "var(--color-bg)", color: "var(--color-text)" }}>
        {/* ===== Top Navigation ===== */}
        <header
          style={{
            background: "var(--color-surface)",
            borderBottom: "1px solid var(--color-border)",
            boxShadow: "var(--shadow-sm)",
            position: "sticky",
            top: 0,
            zIndex: 100,
          }}
        >
          <nav className="container" style={{ display: "flex", alignItems: "center", justifyContent: "space-between", paddingBlock: "1rem" }}>
            {/* Logo */}
            <Link href="/" style={{ display: "flex", alignItems: "center", gap: "0.5rem" }}>
              <span style={{ fontSize: "1.5rem" }}>🍛</span>
              <span style={{ fontSize: "1.25rem", fontWeight: 700, color: "var(--color-primary)" }}>
                Addis Eats
              </span>
            </Link>

            {/* Nav Links */}
            <div style={{ display: "flex", alignItems: "center", gap: "1.5rem" }}>
              <Link
                href="/menu"
                style={{ fontWeight: 500, color: "var(--color-text-muted)", transition: "color 0.2s" }}
              >
                Menu
              </Link>
              <Link
                href="/cart"
                style={{ fontWeight: 500, color: "var(--color-text-muted)", transition: "color 0.2s" }}
              >
                🛒 Cart
              </Link>
              <Link
                href="/kitchen"
                style={{ fontWeight: 500, color: "var(--color-text-muted)", transition: "color 0.2s" }}
              >
                Kitchen
              </Link>
              <Link
                href="/auth/signin"
                className="btn btn-primary"
                style={{ padding: "0.4rem 1rem", borderRadius: "var(--radius-md)" }}
              >
                Sign In
              </Link>
            </div>
          </nav>
        </header>

        {/* ===== Page Content ===== */}
        <main style={{ flex: 1 }}>
          <SWRProvider>
            {children}
          </SWRProvider>
        </main>

        {/* ===== Footer ===== */}
        <footer
          style={{
            background: "var(--color-surface)",
            borderTop: "1px solid var(--color-border)",
            padding: "2rem 0",
            marginTop: "auto",
          }}
        >
          <div className="container" style={{ display: "flex", alignItems: "center", justifyContent: "space-between", flexWrap: "wrap", gap: "1rem" }}>
            <div style={{ display: "flex", alignItems: "center", gap: "0.5rem" }}>
              <span>🍛</span>
              <span style={{ fontWeight: 600, color: "var(--color-primary)" }}>Addis Eats</span>
            </div>
            <p style={{ fontSize: "0.85rem", color: "var(--color-text-light)" }}>
              © 2025 Addis Eats · Authentic Ethiopian Cuisine · Built with Next.js
            </p>
          </div>
        </footer>
      </body>
    </html>
  );
}
