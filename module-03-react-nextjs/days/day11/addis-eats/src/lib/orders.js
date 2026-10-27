/**
 * @file orders.js
 * @description In-memory orders store for Addis Eats.
 *
 * In a real production app this would be replaced by a database (e.g.
 * PostgreSQL via Prisma, or Firebase Firestore), but for this Day 36
 * exercise we keep a simple module-level array so that data survives
 * across API requests within the same Next.js dev-server process.
 *
 * Exported helpers:
 *  - getAllOrders()          — return all orders (newest first)
 *  - getOrderById(id)       — find one order by id
 *  - createOrder(data)      — validate + insert a new order, return it
 *  - updateOrderStatus(id, status) — change the status of an order
 */

import { nanoid } from "nanoid";

/**
 * Valid order statuses and their display labels.
 */
export const ORDER_STATUSES = {
  pending:    "Pending",
  preparing:  "Preparing",
  ready:      "Ready for pickup",
  delivering: "Out for delivery",
  delivered:  "Delivered",
  cancelled:  "Cancelled",
};

/** Module-level in-memory store. */
const orders = [];

// ── Seed data so the kitchen dashboard is not empty on first load ──────────
function seedOrders() {
  orders.push({
    id: "ord-seed-1",
    customerName: "Hana Tesfaye",
    customerPhone: "0912345678",
    deliveryAddress: "Bole, Addis Ababa",
    items: [
      { dishId: "doro-wot", name: "Doro Wot", price: 280, quantity: 2 },
      { dishId: "injera",   name: "Injera",   price: 30,  quantity: 4 },
    ],
    total: 680,
    status: "preparing",
    createdAt: new Date(Date.now() - 12 * 60 * 1000).toISOString(), // 12 min ago
  });

  orders.push({
    id: "ord-seed-2",
    customerName: "Biruk Alemu",
    customerPhone: "0922334455",
    deliveryAddress: "Piassa, Addis Ababa",
    items: [
      { dishId: "beyaynetu", name: "Beyaynetu",  price: 220, quantity: 1 },
      { dishId: "buna",      name: "Ethiopian Buna", price: 50, quantity: 2 },
    ],
    total: 320,
    status: "pending",
    createdAt: new Date(Date.now() - 3 * 60 * 1000).toISOString(), // 3 min ago
  });
}

seedOrders();

// ── Public API ────────────────────────────────────────────────────────────

/**
 * Returns all orders sorted newest-first.
 * @returns {object[]}
 */
export function getAllOrders() {
  return [...orders].sort(
    (a, b) => new Date(b.createdAt) - new Date(a.createdAt)
  );
}

/**
 * Finds a single order by its id.
 * @param {string} id
 * @returns {object|undefined}
 */
export function getOrderById(id) {
  return orders.find((o) => o.id === id);
}

/**
 * Creates and stores a new order.
 * @param {{ customerName: string, customerPhone: string, deliveryAddress: string, items: object[] }} data
 * @returns {object} the newly created order
 * @throws {Error} if required fields are missing
 */
export function createOrder(data) {
  const { customerName, customerPhone, deliveryAddress, items } = data;

  if (!customerName || !deliveryAddress || !items?.length) {
    throw new Error("customerName, deliveryAddress, and at least one item are required.");
  }

  const total = items.reduce((sum, item) => sum + item.price * item.quantity, 0);

  const order = {
    id: `ord-${nanoid(8)}`,
    customerName: customerName.trim(),
    customerPhone: customerPhone?.trim() ?? "",
    deliveryAddress: deliveryAddress.trim(),
    items,
    total,
    status: "pending",
    createdAt: new Date().toISOString(),
  };

  orders.unshift(order); // add to front so newest is first
  return order;
}

/**
 * Updates the status of an existing order.
 * @param {string} id
 * @param {string} status — must be a key in ORDER_STATUSES
 * @returns {object} the updated order
 * @throws {Error} if order not found or status is invalid
 */
export function updateOrderStatus(id, status) {
  if (!Object.keys(ORDER_STATUSES).includes(status)) {
    throw new Error(`Invalid status: "${status}". Valid values: ${Object.keys(ORDER_STATUSES).join(", ")}`);
  }

  const order = orders.find((o) => o.id === id);
  if (!order) throw new Error(`Order "${id}" not found.`);

  order.status = status;
  return { ...order };
}
