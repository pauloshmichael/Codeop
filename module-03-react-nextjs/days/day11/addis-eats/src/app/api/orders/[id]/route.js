/**
 * @file app/api/orders/[id]/route.js
 * @description REST API endpoints for a single order.
 *
 * GET   /api/orders/:id            — fetch one order by id
 * PATCH /api/orders/:id            — update order status (kitchen staff action)
 *
 * PATCH body (JSON):
 *   { "status": "preparing" }
 *
 * Valid statuses: pending | preparing | ready | delivering | delivered | cancelled
 */

import { NextResponse } from "next/server";
import { getOrderById, updateOrderStatus, ORDER_STATUSES } from "@/lib/orders";

// ── GET /api/orders/:id ────────────────────────────────────────────────────
export async function GET(request, { params }) {
  const { id } = await params;
  const order = getOrderById(id);

  if (!order) {
    return NextResponse.json({ error: `Order "${id}" not found.` }, { status: 404 });
  }

  return NextResponse.json({ order });
}

// ── PATCH /api/orders/:id ──────────────────────────────────────────────────
export async function PATCH(request, { params }) {
  const { id } = await params;

  let body;
  try {
    body = await request.json();
  } catch {
    return NextResponse.json({ error: "Request body must be valid JSON." }, { status: 400 });
  }

  const { status } = body ?? {};

  if (!status) {
    return NextResponse.json({ error: "status field is required." }, { status: 400 });
  }

  const validStatuses = Object.keys(ORDER_STATUSES);
  if (!validStatuses.includes(status)) {
    return NextResponse.json(
      { error: `Invalid status "${status}". Valid values: ${validStatuses.join(", ")}` },
      { status: 400 }
    );
  }

  try {
    const order = updateOrderStatus(id, status);
    return NextResponse.json({ order });
  } catch (err) {
    const is404 = err.message.includes("not found");
    return NextResponse.json({ error: err.message }, { status: is404 ? 404 : 500 });
  }
}
