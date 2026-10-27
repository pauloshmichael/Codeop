/**
 * @file app/api/orders/route.js
 * @description REST API endpoint for creating and listing orders.
 *
 * GET  /api/orders          — returns all orders (staff only in a real app)
 * POST /api/orders          — creates a new order
 *
 * POST body (JSON):
 *   {
 *     customerName:    "Hana Tesfaye",
 *     customerPhone:   "0912345678",
 *     deliveryAddress: "Bole, Addis Ababa",
 *     items: [
 *       { dishId: "doro-wot", name: "Doro Wot", price: 280, quantity: 2 }
 *     ]
 *   }
 *
 * POST response 201:
 *   { order: { id, customerName, items, total, status, createdAt, ... } }
 *
 * Error response:
 *   { error: "descriptive message" }
 */

import { NextResponse } from "next/server";
import { getAllOrders, createOrder } from "@/lib/orders";
import { validateOrder } from "@/lib/schema";

// ── GET /api/orders ────────────────────────────────────────────────────────
export async function GET() {
  const orders = getAllOrders();
  return NextResponse.json({ orders });
}

// ── POST /api/orders ───────────────────────────────────────────────────────
export async function POST(request) {
  let body;
  try {
    body = await request.json();
  } catch {
    return NextResponse.json(
      { error: "Request body must be valid JSON." },
      { status: 400 }
    );
  }

  // Validate using shared schema helper
  const validation = validateOrder(body);
  if (!validation.ok) {
    return NextResponse.json({ error: validation.error }, { status: 400 });
  }

  try {
    const order = createOrder(validation.data);
    return NextResponse.json({ order }, { status: 201 });
  } catch (err) {
    return NextResponse.json({ error: err.message }, { status: 500 });
  }
}
