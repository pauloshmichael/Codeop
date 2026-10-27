import Link from "next/link";
import AddToCart from "./AddToCart";

// No "use client": this list stays on the server even when composed into the
// client filter shell below.
export default function DishList({ dishes }) {
  if (!dishes.length) return <p className="empty-state">No recipes match this category.</p>;

  return <div className="dish-grid">{dishes.map((dish) => <article className="dish-card" key={dish.id}><span className="tag">{dish.cuisine}</span><h2><Link href={`/menu/${dish.id}`}>{dish.name}</Link></h2><p>{dish.difficulty} · {dish.prepTimeMinutes + dish.cookTimeMinutes} min · {dish.caloriesPerServing} cal</p><p className="price">★ {dish.rating} ({dish.reviewCount} reviews)</p><AddToCart dish={dish} /></article>)}</div>;
}
