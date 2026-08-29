import Header from './components/Header'
import Dish from './components/Dish'
import { dishes } from './data/dishes'

function App() {
  return (
    <>
      <Header />
      <main>
        <h2>Today's Menu</h2>
        {dishes.map((dish) => (
          <Dish
            key={dish.id}
            name={dish.name}
            price={dish.price}
            description={dish.description}
          />
        ))}
      </main>
    </>
  )
}

export default App