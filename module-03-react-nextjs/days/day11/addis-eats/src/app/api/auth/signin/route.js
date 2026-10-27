/**
 * @file app/api/auth/signin/route.js
 * @description POST /api/auth/signin — authenticates a user and writes a session cookie.
 *
 * Accepts JSON body: { name: string, password: string }
 *
 * Hard-coded credentials (teaching example only):
 *   customer / customer123  → role: "customer"
 *   staff    / kitchen456   → role: "staff"
 *
 * On success, sets the "addis-eats-session" cookie and returns 200.
 * On failure, returns 401 with an error message.
 */

import { NextResponse } from "next/server";
import { setSession } from "@/lib/session";
import { validateSignIn } from "@/lib/schema";

/** Hard-coded user directory — replace with a real DB in production. */
const USERS = [
  { name: "customer", password: "customer123", role: "customer" },
  { name: "staff",    password: "kitchen456",  role: "staff"    },
];

export async function POST(request) {
  let body;
  try {
    body = await request.json();
  } catch {
    return NextResponse.json({ error: "Request body must be valid JSON." }, { status: 400 });
  }

  const validation = validateSignIn(body);
  if (!validation.ok) {
    return NextResponse.json({ error: validation.error }, { status: 400 });
  }

  const { name, password } = validation.data;
  const user = USERS.find((u) => u.name === name && u.password === password);

  if (!user) {
    return NextResponse.json(
      { error: "Invalid name or password." },
      { status: 401 }
    );
  }

  // Write session cookie
  await setSession({ name: user.name, role: user.role });

  return NextResponse.json({
    message: `Welcome, ${user.name}! Signed in as ${user.role}.`,
    name: user.name,
    role: user.role,
  });
}
