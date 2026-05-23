import { images } from '../data/images.js'

const tags = ['Storytelling Expertise', 'Foundation', 'Human-Centered Vision']

export default function Intro() {
  return (
    <section id="intro" className="intro container">
      <div className="intro__top">
        <h2 className="intro__text">
          Everything you see—from images to headlines—is just an example of
          what's possible. Adapt every element to fit your industry, values,
          and creative vision, whether you're an agency, consultant, or
          innovative startup.
        </h2>
      </div>

      <div className="intro__tags">
        {tags.map((t) => (
          <span key={t} className="tag">{t}</span>
        ))}
      </div>

      <div className="intro__images">
        <img src={images.grass} alt="Close up of green grass" />
        <img src={images.mountain} alt="Mountain range under soft light" />
      </div>
    </section>
  )
}
