import { useState } from 'react'

const faqs = [
  {
    q: 'Can I customize the template to match my brand?',
    a: 'Absolutely. Every color, font, image, and section is fully editable, so you can shape the template around your identity in minutes.',
  },
  {
    q: 'Does the template support e-commerce?',
    a: 'Yes. The layout is ready to integrate with popular commerce solutions, letting you sell products or services without rebuilding from scratch.',
  },
  {
    q: 'Can I change the fonts and branding?',
    a: 'Of course. Swap the typefaces, update the logo, and apply your palette—the design system adapts cleanly to your choices.',
  },
  {
    q: 'What kind of support is included?',
    a: 'You get detailed documentation and responsive support to help you launch smoothly and resolve any questions along the way.',
  },
  {
    q: 'Is the template fully responsive?',
    a: 'It is. The layout is crafted to look and perform beautifully on phones, tablets, and large desktop screens alike.',
  },
  {
    q: 'Is it optimized for SEO?',
    a: 'Yes. Semantic markup, fast load times, and clean structure give your site a strong foundation for search visibility.',
  },
]

export default function Faq() {
  const [open, setOpen] = useState(0)

  return (
    <section id="faq" className="faq container">
      <div className="faq__head">
        <h2>You ask, we answer</h2>
        <p>Everything you need to know before making the template your own.</p>
      </div>

      <div className="faq__list">
        {faqs.map((item, i) => {
          const isOpen = open === i
          return (
            <div key={item.q} className={`faq__item ${isOpen ? 'faq__item--open' : ''}`}>
              <button
                className="faq__q"
                aria-expanded={isOpen}
                onClick={() => setOpen(isOpen ? -1 : i)}
              >
                <span>{item.q}</span>
                <span className="faq__icon" aria-hidden="true" />
              </button>
              <div className="faq__a" role="region">
                <p>{item.a}</p>
              </div>
            </div>
          )
        })}
      </div>
    </section>
  )
}
