/**
 * @file schema.js
 * @description Simple validation helpers for Addis Eats request bodies.
 *
 * We keep validation in a separate file so it can be shared between
 * API Route Handlers and Server Actions without duplication.
 *
 * In a larger project you might reach for Zod or Yup, but for Day 36
 * we write plain-JS validators to keep the dependency footprint small.
 */

/**
 * Validates an order creation payload.
 *
 * Required fields:
 *  - customerName    : non-empty string
 *  - deliveryAddress : non-empty string
 *  - items           : non-empty array where each item has
 *                        dishId (string), name (string),
 *                        price (positive number), quantity (positive integer)
 *
 * Optional fields:
 *  - customerPhone   : string
 *
 * @param {unknown} body — raw parsed JSON from the request
 * @returns {{ ok: true, data: object } | { ok: false, error: string }}
 */
export function validateOrder(body) {
  if (!body || typeof body !== "object") {
    return { ok: false, error: "Request body must be a JSON object." };
  }

  const { customerName, customerPhone, deliveryAddress, items } = body;

  if (!customerName || typeof customerName !== "string" || !customerName.trim()) {
    return { ok: false, error: "customerName is required and must be a non-empty string." };
  }

  if (!deliveryAddress || typeof deliveryAddress !== "string" || !deliveryAddress.trim()) {
    return { ok: false, error: "deliveryAddress is required and must be a non-empty string." };
  }

  if (!Array.isArray(items) || items.length === 0) {
    return { ok: false, error: "items must be a non-empty array." };
  }

  for (const [i, item] of items.entries()) {
    if (!item.dishId || typeof item.dishId !== "string") {
      return { ok: false, error: `items[${i}].dishId must be a non-empty string.` };
    }
    if (!item.name || typeof item.name !== "string") {
      return { ok: false, error: `items[${i}].name must be a non-empty string.` };
    }
    if (typeof item.price !== "number" || item.price <= 0) {
      return { ok: false, error: `items[${i}].price must be a positive number.` };
    }
    if (!Number.isInteger(item.quantity) || item.quantity <= 0) {
      return { ok: false, error: `items[${i}].quantity must be a positive integer.` };
    }
  }

  return {
    ok: true,
    data: {
      customerName: customerName.trim(),
      customerPhone: (customerPhone ?? "").trim(),
      deliveryAddress: deliveryAddress.trim(),
      items,
    },
  };
}

/**
 * Validates a sign-in request body.
 *
 * @param {unknown} body
 * @returns {{ ok: true, data: object } | { ok: false, error: string }}
 */
export function validateSignIn(body) {
  if (!body || typeof body !== "object") {
    return { ok: false, error: "Request body must be a JSON object." };
  }

  const { name, password } = body;

  if (!name || typeof name !== "string" || !name.trim()) {
    return { ok: false, error: "name is required." };
  }

  if (!password || typeof password !== "string") {
    return { ok: false, error: "password is required." };
  }

  return { ok: true, data: { name: name.trim(), password } };
}
