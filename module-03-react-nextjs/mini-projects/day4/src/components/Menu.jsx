import { useEffect, useRef, useState } from 'react'
import CategoryBar from './CategoryBar'
import DishList from './DishList'

const CATEGORIES = ['All', 'Meat', 'Fasting', 'Breakfast']

function Menu() {
  const [category, setCategory] = useState('All')
  const [dishes, setDishes] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [query, setQuery] = useState('')
  const [total, setTotal] = useState(0)
  const searchRef = useRef(null)

  // derived, not stored
  const visible = dishes.filter((dish) =>
    dish.name.toLowerCase().includes(query.trim().toLowerCase())
  )

  // focus the search box once, after the DOM exists
  useEffect(() => {
    searchRef.current?.focus()
  }, [])

  // keep the tab title in sync with the list
  useEffect(() => {
    document.title = `Addis Eats · ${visible.length} dishes`
  }, [visible.length])

  // fetch whenever the category changes, cancelling the previous request
  useEffect(() => {
    const controller = new AbortController()

    async function loadDishes() {
      setLoading(true)
      setError(null)
      try {
        const res = await fetch(`/dishes.json?category=${encodeURIComponent(category)}`, {
          signal: controller.signal,
        })
        if (!res.ok) {
          throw new Error(`Couldn't load the menu (server replied ${res.status}). Please try again.`)
        }
        const data = await res.json()
        setDishes(category === 'All' ? data : data.filter((d) => d.category === category))
      } catch (err) {
        if (err.name === 'AbortError') return
        setError(
          err.name === 'TypeError' || err.name === 'SyntaxError'
            ? "We couldn't reach the menu. Check your connection and try again."
            : err.message
        )
      } finally {
        if (!controller.signal.aborted) setLoading(false)
      }
    }

    loadDishes()
    return () => controller.abort()
  }, [category])

  const handleAdd = (price) => setTotal((prev) => prev + price)

  return (
    <section>
      <input
        ref={searchRef}
        className="search"
        type="search"
        placeholder="Search dishes…"
        value={query}
        onChange={(e) => setQuery(e.target.value)}
      />
      <CategoryBar categories={CATEGORIES} selected={category} onSelect={setCategory} />
      <DishList dishes={visible} loading={loading} error={error} onAdd={handleAdd} />
      <p className="total">Order total: <strong>{total} ETB</strong></p>
    </section>
  )
}

export default Menu