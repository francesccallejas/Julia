import { images } from '../data/images.js'

export default function Sustainability() {
  return (
    <section className="sustain container">
      <div className="sustain__text">
        <h2>The ultimate template for businesses driven by sustainability</h2>
        <p>
          Designed for brands that care about their impact, this template pairs
          a calm, natural aesthetic with the structure modern audiences expect.
          Tell your story, showcase your values, and invite people to be part
          of something meaningful.
        </p>
        <p>
          From hero to footer, every section is ready to adapt—so you can launch
          a site that feels considered, credible, and unmistakably human.
        </p>
      </div>
      <div className="sustain__media">
        <img src={images.forest} alt="Dense green forest seen from above" />
      </div>
    </section>
  )
}
