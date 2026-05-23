import { images } from '../data/images.js'

const reviews = [
  {
    quote:
      'Switching to this template transformed how customers perceive us. It feels premium, warm, and completely on-brand.',
    name: 'Amelia Hart',
    role: 'Founder, Verdant Studio',
    avatar: images.avatar3,
  },
  {
    quote:
      'Setup was effortless and the design did the heavy lifting. Our conversion rate climbed within the first month.',
    name: 'Marcus Lee',
    role: 'CEO, Northshore Co.',
    avatar: images.avatar2,
  },
  {
    quote:
      'Beautiful, fast, and genuinely human. Exactly the impression we wanted to give a sustainability-minded audience.',
    name: 'Sofia Romano',
    role: 'Brand Lead, Atlas',
    avatar: images.avatar1,
  },
]

function Stars() {
  return (
    <div className="review__stars" aria-label="5 out of 5 stars">
      {Array.from({ length: 5 }).map((_, i) => (
        <svg key={i} width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
          <path d="M12 2l2.9 6.3 6.9.7-5.1 4.6 1.4 6.8L12 17.8 5.9 20.4l1.4-6.8L2.2 9l6.9-.7z" />
        </svg>
      ))}
    </div>
  )
}

export default function Testimonials() {
  return (
    <section id="testimonials" className="testimonials container">
      <h2 className="testimonials__title">Happy businesses</h2>
      <div className="testimonials__grid">
        {reviews.map((r) => (
          <article key={r.name} className="review">
            <Stars />
            <p className="review__quote">"{r.quote}"</p>
            <div className="review__person">
              <img src={r.avatar} alt={r.name} />
              <div>
                <strong>{r.name}</strong>
                <span>{r.role}</span>
              </div>
            </div>
          </article>
        ))}
      </div>
    </section>
  )
}
