/**
 * @file app/api/dishes/route.js
 * @description REST API endpoint for the Addis Eats dish catalog.
 *
 * GET /api/dishes
 *   Returns filtered, paginated list of dishes.
 *
 *   Query params:
 *     q        — search term (matches name and description, case-insensitive)
 *     category — filter by category ("All" returns everything)
 *     page     — 1-based page number (default: 1)
 *     limit    — page size (default: 12, max: 50)
 *
 *   Response 200:
 *     {
 *       dishes: [...],
 *       total:  14,
 *       page:   1,
 *       limit:  12,
 *       pages:  2
 *     }
 */

import { NextResponse } from "next/server";
import { searchDishes } from "@/lib/menu";

export async function GET(request) {
  const { searchParams } = new URL(request.url);

  const query    = searchParams.get("q")        ?? "";
  const category = searchParams.get("category") ?? "All";
  const page     = Math.max(1, parseInt(searchParams.get("page")  ?? "1",  10));
  const limit    = Math.min(50, Math.max(1, parseInt(searchParams.get("limit") ?? "12", 10)));

  // Filter using our shared lib helper
  const filtered = searchDishes({ query, category });

  // Manual pagination
  const total  = filtered.length;
  const pages  = Math.ceil(total / limit);
  const start  = (page - 1) * limit;
  const dishes = filtered.slice(start, start + limit);

  return NextResponse.json({ dishes, total, page, limit, pages });
}
