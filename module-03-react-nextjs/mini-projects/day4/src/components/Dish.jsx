import { useState } from 'react'
import PropTypes from 'prop-types'

function Dish({ name, price, spicy = false, currency = 'ETB', description }) {
  const [count, setCount] = useState(0)

    const handleAdd = () => {
    setCount((c) => c + 1)
    onAdd?.(price)
  }

  return (
    <div className="dish">
      <div>
        <h3>
          {name} {spicy === true && <span className="badge">Spicy</span>}
          {count > 0 && <span className="count">× {count}</span>}
        </h3>
        {description && <p className="description">{description}</p>}
      </div>
      <div className="dish-side">
        <span className="price">{price} {currency}</span>
        <button onClick={() => setCount((c) => c + 1)}>Add</button>
      </div>
    </div>
  )
}

Dish.propTypes = {
  name: PropTypes.string.isRequired,
  price: PropTypes.number.isRequired,
  spicy: PropTypes.bool,
  currency: PropTypes.string,
  description: PropTypes.string,
}

export default Dish