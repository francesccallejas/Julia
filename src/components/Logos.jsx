const brands = ['Evergreen', 'Northwind', 'Lumen', 'Terra', 'Solace', 'Apex']

export default function Logos() {
  return (
    <section className="logos container">
      <p className="logos__label">Trusted by forward-thinking teams</p>
      <div className="logos__row">
        {brands.map((b) => (
          <span key={b} className="logos__brand">{b}</span>
        ))}
      </div>
    </section>
  )
}
