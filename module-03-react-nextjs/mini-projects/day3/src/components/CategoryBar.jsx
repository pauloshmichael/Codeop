import PropTypes from 'prop-types'

function CategoryBar({ categories, selected, onSelect }) {
  return (
    <div className="chips">
      {categories.map((c) => (
        <button
          key={c}
          type="button"
          className={c === selected ? 'chip active' : 'chip'}
          aria-pressed={c === selected}
          onClick={() => onSelect(c)}
        >
          {c}
        </button>
      ))}
    </div>
  )
}

CategoryBar.propTypes = {
  categories: PropTypes.arrayOf(PropTypes.string).isRequired,
  selected: PropTypes.string.isRequired,
  onSelect: PropTypes.func.isRequired,
}

export default CategoryBar