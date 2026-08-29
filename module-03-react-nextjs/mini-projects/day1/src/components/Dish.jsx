function Dish({ name, price, description }) {
  return (
    <article className="dish">
      <div>
        <h3>{name}</h3>
        <p className="description">{description}</p>
      </div>
      <span className="price">{price} ETB</span>
    </article>
  )
}

export default Dish