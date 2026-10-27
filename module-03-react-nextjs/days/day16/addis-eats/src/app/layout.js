import Link from "next/link";
import "./globals.css";
import Providers from "./providers";

export const metadata = { title: "Addis Eats", description: "Fresh Ethiopian favourites, delivered in Addis Ababa." };

export default function RootLayout({ children }) {
  return <html lang="en"><body><Providers><header className="site-header"><Link className="brand" href="/">Addis Eats</Link><nav aria-label="Main navigation"><Link href="/menu">Menu</Link><Link href="/checkout">Checkout</Link></nav></header>{children}<footer className="site-footer">© 2026 Addis Eats · Made with Ethiopian flavour</footer></Providers></body></html>;
}
