"use client";

/**
 * @file components/SignOutButton.jsx
 * @description Reusable "Sign Out" button component.
 *
 * Must be a Client Component ("use client") because it attaches an
 * onClick handler and uses useRouter for navigation after sign-out.
 *
 * Usage:
 *   import SignOutButton from "@/components/SignOutButton";
 *   <SignOutButton />
 */

import { useState } from "react";
import { useRouter } from "next/navigation";

export default function SignOutButton({ className, style }) {
  const router = useRouter();
  const [loading, setLoading] = useState(false);

  async function handleSignOut() {
    setLoading(true);
    try {
      await fetch("/api/auth/signout", { method: "POST" });
      router.push("/");
      router.refresh(); // re-render server components so nav updates
    } finally {
      setLoading(false);
    }
  }

  return (
    <button
      onClick={handleSignOut}
      disabled={loading}
      className={className ?? "btn btn-secondary"}
      style={style}
      aria-label="Sign out of Addis Eats"
    >
      {loading ? "Signing out…" : "Sign Out"}
    </button>
  );
}
