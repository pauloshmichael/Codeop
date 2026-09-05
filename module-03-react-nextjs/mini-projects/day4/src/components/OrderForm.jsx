import { useState } from 'react'

const AREAS = [
  'Bole', 'Yeka', 'Kirkos', 'Arada', 'Lideta',
  'Nifas Silk-Lafto', 'Kolfe Keranio', 'Gullele', 'Addis Ketema', 'Akaky Kaliti',
]

function OrderForm() {
  const [form, setForm] = useState({ name: '', phone: '', area: '' })

  const handleChange = (event) => {
    const { name, value } = event.target
    setForm((prev) => ({ ...prev, [name]: value }))
  }

  const handleSubmit = (event) => {
    event.preventDefault()
    console.log('Order details:', form)
  }

const PHONE_PATTERN = /^(?:\+251|0)9\d{8}$/   // put this above the component
const phoneValid = PHONE_PATTERN.test(form.phone)
const showPhoneError = form.phone !== '' && !phoneValid

  return (
    <form className="order-form" onSubmit={handleSubmit}>
      <h2>Delivery details</h2>

      <label>
        Name
        <input name="name" value={form.name} onChange={handleChange} />
      </label>

      <label>
        TeleBirr number
        <input
          name="phone"
          type="tel"
          value={form.phone}
          onChange={handleChange}
          placeholder="0912345678"
          aria-invalid={showPhoneError}
        />
          {showPhoneError && (
       <p className="error">Enter a valid number, e.g. 0912345678 or +251912345678.</p>
           )}
      </label>

      <label>
        Area
        <select name="area" value={form.area} onChange={handleChange}>
          <option value="">Choose an area</option>
          {AREAS.map((area) => (
            <option key={area} value={area}>{area}</option>
          ))}
        </select>
      </label>

      <button type="submit" disabled={!phoneValid}>Place order</button>
    </form>
  )
}

export default OrderForm