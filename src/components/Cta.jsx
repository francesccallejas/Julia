import { images } from '../data/images.js'

export default function Cta() {
  return (
    <section id="cta" className="cta">
      <div className="cta__media">
        <img src={images.lake} alt="Mountain lake surrounded by forest" />
        <div className="cta__overlay" />
      </div>
      <div className="cta__content container">
        <h2>Unlock your website's full potential</h2>
        <p>Launch a brand experience that feels premium, sustainable, and human.</p>
        <a href="#hero" className="btn btn--light">Buy Template</a>
      </div>
    </section>
  )
}
