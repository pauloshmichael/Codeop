import Header from './components/Header'
import Menu from './components/Menu'
import OrderForm from './components/OrderForm'
import { dishes } from './data/dishes'

function App() {
  return (
    <>
      <Header />
      <main>
        <h2>Today's Menu</h2>
        <Menu dishes={dishes} />
        <OrderForm />
      </main>
    </>
  )
}

export default App