import { images } from '../data/images.js'

export default function Hero() {
  return (
    <section id="hero" className="hero">
      <div className="hero__media">
        <img src={images.heroRoad} alt="Aerial view of a road winding through a green forest" />
        <div className="hero__overlay" />
      </div>

      <div className="hero__content container">
        <p className="hero__eyebrow">For:Human™ — Template</p>
        <h1 className="hero__title">
          Elevate your brand<br />with a human touch
        </h1>
        <a href="#cta" className="btn btn--light hero__btn">Buy Template</a>
      </div>

      <div className="hero__scroll">
        <span>Scroll to explore</span>
        <span className="hero__scroll-line" />
      </div>
    </section>
  )
}
