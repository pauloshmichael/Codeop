/**
 * @file menu.js
 * @description Static Ethiopian dish catalog for Addis Eats.
 *
 * Each dish has:
 *  - id         : unique slug used in URL params
 *  - name       : display name
 *  - category   : one of "Mains" | "Vegetarian" | "Sides" | "Drinks" | "Desserts"
 *  - price      : price in ETB (Ethiopian Birr)
 *  - description: short description shown on card / detail page
 *  - emoji      : representative emoji used in place of a photo
 *  - spice      : 0-3 heat level (0 = none, 3 = very spicy)
 *  - time       : estimated prep time in minutes
 *  - popular    : boolean — show "Popular" badge on card
 */

export const dishes = [
  {
    id: "doro-wot",
    name: "Doro Wot",
    category: "Mains",
    price: 280,
    description:
      "Ethiopia's most iconic dish — slow-simmered chicken drumsticks and whole boiled eggs in a rich, deeply spiced berbere sauce. Served with injera.",
    emoji: "🍗",
    spice: 3,
    time: 45,
    popular: true,
  },
  {
    id: "tibs",
    name: "Tibs",
    category: "Mains",
    price: 320,
    description:
      "Sautéed strips of tender lamb or beef cooked in butter with onions, garlic, jalapeños, and rosemary. A festive favourite.",
    emoji: "🥩",
    spice: 2,
    time: 25,
    popular: true,
  },
  {
    id: "kitfo",
    name: "Kitfo",
    category: "Mains",
    price: 350,
    description:
      "Lean minced beef seasoned with mitmita spice blend and niter kibbeh (spiced clarified butter). Served leb-leb (slightly cooked) or raw.",
    emoji: "🥓",
    spice: 2,
    time: 15,
    popular: false,
  },
  {
    id: "shiro-wot",
    name: "Shiro Wot",
    category: "Vegetarian",
    price: 180,
    description:
      "A hearty, creamy stew made from ground roasted chickpea flour simmered with onions, garlic, and berbere spice. Vegan-friendly.",
    emoji: "🫘",
    spice: 2,
    time: 20,
    popular: true,
  },
  {
    id: "gomen",
    name: "Gomen",
    category: "Vegetarian",
    price: 150,
    description:
      "Tender collard greens sautéed with onion, garlic, ginger, and a hint of turmeric. Light, nutritious, and traditionally served during fasting days.",
    emoji: "🥬",
    spice: 0,
    time: 20,
    popular: false,
  },
  {
    id: "fossolia",
    name: "Fossolia",
    category: "Vegetarian",
    price: 140,
    description:
      "Green beans and carrots stir-fried with onions, tomatoes, and a touch of Ethiopian spices. A colourful, mildly spiced vegan side.",
    emoji: "🫑",
    spice: 0,
    time: 20,
    popular: false,
  },
  {
    id: "beyaynetu",
    name: "Beyaynetu",
    category: "Vegetarian",
    price: 220,
    description:
      "The grand Ethiopian fasting platter — a selection of seven different vegan dishes including shiro, gomen, fossolia, misir, and more, arranged on a large injera.",
    emoji: "🌈",
    spice: 1,
    time: 35,
    popular: true,
  },
  {
    id: "misir-wot",
    name: "Misir Wot",
    category: "Vegetarian",
    price: 160,
    description:
      "Red lentils cooked low and slow in a vibrant berbere sauce with onion and garlic. Protein-rich and deeply satisfying.",
    emoji: "🫘",
    spice: 2,
    time: 30,
    popular: false,
  },
  {
    id: "injera",
    name: "Injera",
    category: "Sides",
    price: 30,
    description:
      "Traditional Ethiopian sourdough flatbread made from 100% teff flour. Slightly spongy and tangy — the foundation of every Ethiopian meal.",
    emoji: "🫓",
    spice: 0,
    time: 5,
    popular: false,
  },
  {
    id: "ayib",
    name: "Ayib",
    category: "Sides",
    price: 60,
    description:
      "Fresh Ethiopian cottage cheese, mild and crumbly, served as a cooling accompaniment to spicy wots.",
    emoji: "🧀",
    spice: 0,
    time: 5,
    popular: false,
  },
  {
    id: "tej",
    name: "Tej",
    category: "Drinks",
    price: 80,
    description:
      "Traditional Ethiopian honey wine, lightly fermented and subtly sweet. Served chilled in a berele (flask-shaped vessel).",
    emoji: "🍯",
    spice: 0,
    time: 3,
    popular: false,
  },
  {
    id: "buna",
    name: "Ethiopian Buna",
    category: "Drinks",
    price: 50,
    description:
      "Freshly roasted and brewed Ethiopian coffee, served in the traditional three-round coffee ceremony. Rich, aromatic, and full-bodied.",
    emoji: "☕",
    spice: 0,
    time: 15,
    popular: true,
  },
  {
    id: "chechebsa",
    name: "Chechebsa",
    category: "Desserts",
    price: 120,
    description:
      "Torn flatbread pieces tossed in niter kibbeh and berbere, often eaten as a hearty breakfast or dessert. Crispy, buttery, and warming.",
    emoji: "🫔",
    spice: 1,
    time: 15,
    popular: false,
  },
  {
    id: "firfir",
    name: "Firfir",
    category: "Mains",
    price: 200,
    description:
      "Leftover injera torn into pieces and stewed in berbere sauce with clarified butter. A rustic, comforting dish beloved for breakfast or brunch.",
    emoji: "🫕",
    spice: 2,
    time: 15,
    popular: false,
  },
];

/**
 * Returns all unique categories from the dish list.
 * @returns {string[]}
 */
export function getCategories() {
  return ["All", ...new Set(dishes.map((d) => d.category))];
}

/**
 * Finds a single dish by its id slug.
 * @param {string} id
 * @returns {object|undefined}
 */
export function getDishById(id) {
  return dishes.find((d) => d.id === id);
}

/**
 * Searches and filters dishes.
 * @param {{ query?: string, category?: string }} options
 * @returns {object[]}
 */
export function searchDishes({ query = "", category = "All" } = {}) {
  const q = query.toLowerCase();
  return dishes.filter((d) => {
    const matchesCategory = category === "All" || d.category === category;
    const matchesQuery =
      !q ||
      d.name.toLowerCase().includes(q) ||
      d.description.toLowerCase().includes(q);
    return matchesCategory && matchesQuery;
  });
}
