import PropTypes from 'prop-types'

export const dishShape = PropTypes.shape({
  id: PropTypes.number.isRequired,
  name: PropTypes.string.isRequired,
  price: PropTypes.number.isRequired,
  category: PropTypes.string,
  spicy: PropTypes.bool,
  description: PropTypes.string,
})