import PropTypes from 'prop-types'
import Card from './Card'
import Dish from './Dish'
import { dishShape } from '../propTypes'

function DishList({ dishes, loading, error, onAdd }) {
  if (loading) {
    return (
      <div className="status" role="status">
        <div className="spinner" />
        Loading the menu…
      </div>
    )
  }

  if (error) {
    return <p className="status failed" role="alert">{error}</p>
  }

  if (dishes.length === 0) {
    return <p className="empty">No dishes found. Try another category or search.</p>
  }

  return (
    <div>
      {dishes.map((dish) => (
        <Card key={dish.id}>
          <Dish
            name={dish.name}
            price={dish.price}
            spicy={dish.spicy}
            description={dish.description}
            onAdd={onAdd}
          />
        </Card>
      ))}
    </div>
  )
}

DishList.propTypes = {
  dishes: PropTypes.arrayOf(dishShape).isRequired,
  loading: PropTypes.bool,
  error: PropTypes.string,
  onAdd: PropTypes.func,
}

export default DishList