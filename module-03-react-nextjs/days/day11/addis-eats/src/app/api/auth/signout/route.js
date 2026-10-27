/**
 * @file app/api/auth/signout/route.js
 * @description POST /api/auth/signout — clears the session cookie and signs the user out.
 */

import { NextResponse } from "next/server";
import { clearSession } from "@/lib/session";

export async function POST() {
  await clearSession();
  return NextResponse.json({ message: "Signed out successfully." });
}
