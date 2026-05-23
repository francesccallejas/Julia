import { images } from '../data/images.js'

const tags = [
  'Top-Selling Knowledge',
  'Market-Leading Skills',
  'Best-Selling Insights',
  'High-Demand Expertise',
]

export default function FirstImpression() {
  return (
    <section className="impression container">
      <div className="impression__media">
        <img src={images.plant1} alt="Sunlit green leaves" />
        <img src={images.plant2} alt="Fresh green plant" />
      </div>
      <div className="impression__text">
        <h2>A lasting first impression</h2>
        <p>
          The moment someone lands on your site sets the tone for everything
          that follows. Thoughtful typography, generous spacing, and immersive
          imagery work together to make that first impression count.
        </p>
        <div className="impression__tags">
          {tags.map((t) => (
            <span key={t} className="tag tag--dark">{t}</span>
          ))}
        </div>
      </div>
    </section>
  )
}
