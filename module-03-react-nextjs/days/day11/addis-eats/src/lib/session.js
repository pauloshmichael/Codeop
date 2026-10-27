/**
 * @file session.js
 * @description Lightweight session helpers for Addis Eats.
 *
 * We use a plain HTTP-only cookie called "addis-eats-session" to track
 * whether a user is "signed in". The value is a JSON string containing
 * the user's name and role.
 *
 * This is NOT production-grade authentication — it's a simple teaching
 * example to demonstrate how Next.js Route Handlers can read and write
 * cookies using the `next/headers` package.
 *
 * For a real app, use NextAuth.js, Clerk, or a proper JWT library.
 */

import { cookies } from "next/headers";

/** Name of the session cookie. */
const COOKIE_NAME = "addis-eats-session";

/** Cookie options */
const COOKIE_OPTIONS = {
  httpOnly: true,
  secure: process.env.NODE_ENV === "production",
  sameSite: "lax",
  path: "/",
  maxAge: 60 * 60 * 8, // 8 hours
};

/**
 * Reads and parses the current session from the cookie store.
 * @returns {{ name: string, role: "customer" | "staff" } | null}
 */
export async function getSession() {
  const cookieStore = await cookies();
  const raw = cookieStore.get(COOKIE_NAME);
  if (!raw?.value) return null;
  try {
    return JSON.parse(raw.value);
  } catch {
    return null;
  }
}

/**
 * Writes a new session cookie.
 * @param {{ name: string, role: "customer" | "staff" }} session
 */
export async function setSession(session) {
  const cookieStore = await cookies();
  cookieStore.set(COOKIE_NAME, JSON.stringify(session), COOKIE_OPTIONS);
}

/**
 * Clears the session cookie (signs the user out).
 */
export async function clearSession() {
  const cookieStore = await cookies();
  cookieStore.delete(COOKIE_NAME);
}

/**
 * Returns true if there is an active session.
 * @returns {boolean}
 */
export async function isAuthenticated() {
  const session = await getSession();
  return session !== null;
}

/**
 * Returns true if the current user has the "staff" role.
 * @returns {boolean}
 */
export async function isStaff() {
  const session = await getSession();
  return session?.role === "staff";
}
