import { useState } from 'react'
import PropTypes from 'prop-types'
import CategoryBar from './CategoryBar'
import DishList from './DishList'
import { dishShape } from '../propTypes'

function Menu({ dishes }) {
  const [category, setCategory] = useState('All')
  const [total, setTotal] = useState(0)

  const categories = ['All', ...new Set(dishes.map((dish) => dish.category))]
  const visible =
    category === 'All' ? dishes : dishes.filter((dish) => dish.category === category)

  const handleAdd = (price) => setTotal((prev) => prev + price)

  return (
    <section>
      <CategoryBar categories={categories} selected={category} onSelect={setCategory} />
      <DishList dishes={visible} category={category} onAdd={handleAdd} />
      <p className="total">Order total: <strong>{total} ETB</strong></p>
    </section>
  )
}

Menu.propTypes = {
  dishes: PropTypes.arrayOf(dishShape).isRequired,
}

export default Menu