import { images } from '../data/images.js'

export default function TemplateCombines() {
  return (
    <section className="combines">
      <div className="combines__media">
        <img src={images.roadAerial} alt="Winding road through green hills from above" />
        <div className="combines__overlay" />
      </div>
      <div className="combines__content container">
        <h2>
          A template that combines a sleek aesthetic with user-friendly features
          to elevate your brand
        </h2>
      </div>
    </section>
  )
}
