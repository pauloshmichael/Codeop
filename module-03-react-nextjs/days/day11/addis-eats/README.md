# 🍛 Addis Eats — Ethiopian Food Delivery App

A full-featured food delivery web application built with **Next.js 15 App Router**, showcasing real-world patterns including data fetching, routing, authentication, and order management.

## 🚀 Features

- **Home Page** — Hero section with featured dishes and restaurant story
- **Menu Page** — Full dish catalog with category filtering and search
- **Dish Detail Page** — Individual dish info with add-to-cart action
- **Cart & Checkout** — Order summary, delivery details form, and confirmation
- **Order Tracking** — Live order status polling with SWR
- **Sign In / Sign Out** — Session-based authentication flow
- **Kitchen Dashboard** — Staff view to manage and update order statuses
- **API Routes** — RESTful endpoints for dishes and orders

## 🛠 Tech Stack

| Layer | Technology |
|-------|------------|
| Framework | Next.js 15 (App Router) |
| Language | JavaScript (JSX) |
| Styling | Tailwind CSS v4 |
| Data Fetching | SWR + Native fetch |
| Font | Geist Sans / Geist Mono |
| Deployment | Vercel |

## 📁 Project Structure

```
src/
├── app/
│   ├── layout.js           # Root layout with nav and providers
│   ├── page.js             # Home page
│   ├── globals.css         # Global styles and CSS variables
│   ├── menu/
│   │   ├── page.js         # Menu listing with filter
│   │   └── [id]/
│   │       └── page.js     # Individual dish detail
│   ├── cart/
│   │   └── page.js         # Cart review and checkout
│   ├── checkout/
│   │   └── page.js         # Order form and confirmation
│   ├── orders/
│   │   └── [id]/
│   │       └── page.js     # Live order tracking
│   ├── kitchen/
│   │   └── page.js         # Staff kitchen dashboard
│   ├── auth/
│   │   ├── signin/
│   │   │   └── page.js     # Sign-in form
│   │   └── signout/
│   │       └── route.js    # Sign-out handler
│   └── api/
│       ├── dishes/
│       │   └── route.js    # GET dishes with search + pagination
│       └── orders/
│           └── route.js    # GET + POST orders
├── components/
│   └── SignOutButton.jsx    # Client sign-out button
└── lib/
    ├── fetcher.js          # SWR fetcher utility
    ├── orders.js           # In-memory orders store
    ├── session.js          # Session helpers
    └── schema.js           # Order validation schema
```

## ⚡ Getting Started

```bash
npm install
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) to see the app.

## 📚 Learning Objectives (Day 36)

- Next.js App Router file-based routing conventions
- Server Components vs Client Components (`"use client"`)
- Route Handlers (`route.js`) for building API endpoints
- Dynamic routes (`[id]`) for dish detail and order tracking
- SWR for client-side data fetching and polling
- Session cookies for lightweight authentication
- In-memory data stores for rapid prototyping
