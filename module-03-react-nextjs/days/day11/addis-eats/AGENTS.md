# Addis Eats — Agent Notes (Day 36)

## Project Overview
A Next.js 15 App Router food delivery app for Ethiopian cuisine.
Built as a Day 36 capstone project for the IBT Full Stack Academy.

## Key Architecture Decisions

### Routing
- **App Router** with file-based routing (`src/app/`)
- Dynamic routes: `/menu/[id]` and `/orders/[id]`
- Route Handlers: `src/app/api/**`

### Data Strategy
- **Server Components** read data directly from `src/lib/` modules (no API round-trip)
- **Client Components** use `useSWR` with the shared `fetcher` utility for live data
- In-memory store (`src/lib/orders.js`) — data resets on server restart

### Authentication
- HTTP-only cookie `addis-eats-session` (JSON: `{ name, role }`)
- Two hard-coded accounts: `customer/customer123` and `staff/kitchen456`
- Session helpers in `src/lib/session.js`

### Styling
- Tailwind CSS v4 utility classes + custom CSS variables in `globals.css`
- Design tokens: `--color-primary`, `--color-surface`, etc.
- Utility classes: `.btn`, `.btn-primary`, `.btn-secondary`, `.card`, `.badge`

## File Map
```
src/
├── app/
│   ├── page.js              # Home (Server Component)
│   ├── layout.js            # Root layout with nav
│   ├── globals.css          # Design tokens & utilities
│   ├── error.js             # Global error boundary (Client)
│   ├── not-found.js         # 404 page (Server)
│   ├── menu/
│   │   ├── page.js          # Menu listing (Server — reads searchParams)
│   │   ├── loading.js       # Skeleton loading UI
│   │   └── [id]/page.js     # Dish detail (Server — dynamic)
│   ├── cart/page.js         # Cart (Client — useState)
│   ├── checkout/page.js     # Checkout (Client — form + fetch)
│   ├── orders/[id]/page.js  # Order tracking (Client — SWR)
│   ├── kitchen/page.js      # Kitchen dashboard (Client — SWR)
│   ├── auth/signin/page.js  # Sign-in form (Client)
│   └── api/
│       ├── dishes/route.js          # GET dishes
│       ├── orders/route.js          # GET + POST orders
│       ├── orders/[id]/route.js     # GET + PATCH order
│       ├── auth/signin/route.js     # POST sign-in
│       └── auth/signout/route.js    # POST sign-out
├── components/
│   └── SignOutButton.jsx     # Client sign-out button
└── lib/
    ├── menu.js      # Dish catalog + helpers
    ├── orders.js    # In-memory orders store
    ├── session.js   # Cookie session helpers
    ├── schema.js    # Request body validators
    └── fetcher.js   # SWR fetch wrapper
```

## Running Locally
```bash
cd days/Day_36/addis-eats
npm install
npm run dev
# Open http://localhost:3000
```

## Demo Credentials
| Role     | Username | Password    |
|----------|----------|-------------|
| Customer | customer | customer123 |
| Staff    | staff    | kitchen456  |
