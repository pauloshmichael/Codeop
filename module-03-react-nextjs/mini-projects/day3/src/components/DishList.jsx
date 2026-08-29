import PropTypes from 'prop-types'
import Card from './Card'
import Dish from './Dish'
import { dishShape } from '../propTypes'

function DishList({ dishes, category, onAdd }) {
  if (dishes.length === 0) {
    return <p className="empty">No dishes in "{category}" right now.</p>
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
  category: PropTypes.string.isRequired,
  onAdd: PropTypes.func,
}

export default DishList