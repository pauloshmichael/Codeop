import Header from './components/Header'
import Menu from './components/Menu'
import OrderForm from './components/OrderForm'

const CATEGORY = 'Meat' // try 'Fasting', 'All', and 'Dessert' (no matches)

function App() {
  return (
    <>
      <Header />
      <main>
        <h2>Today's Menu</h2>
        <Menu />
        <OrderForm/>
      </main>
    </>
  )
}

export default App