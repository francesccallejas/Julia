const features = [
  {
    title: 'Transform your identity',
    text: 'Shape a distinctive brand presence that resonates with your audience and stands the test of time.',
    icon: 'spark',
  },
  {
    title: 'State-of-the-Art Platform',
    text: 'Built on modern, reliable technology so your website stays fast, secure, and future-proof.',
    icon: 'layers',
  },
  {
    title: 'Bestselling designer',
    text: 'Crafted by award-winning designers with an eye for detail and an obsession for clarity.',
    icon: 'pen',
  },
  {
    title: 'Human-centered approach',
    text: 'Every interaction is designed around real people, making your site intuitive and welcoming.',
    icon: 'heart',
  },
  {
    title: 'Optimized performance',
    text: 'Lightweight, accessible, and tuned for speed across every device and connection.',
    icon: 'gauge',
  },
  {
    title: 'Endlessly customizable',
    text: 'Adapt colors, type, and layout in minutes to make the template unmistakably yours.',
    icon: 'sliders',
  },
]

function Icon({ name }) {
  const common = {
    width: 28,
    height: 28,
    viewBox: '0 0 24 24',
    fill: 'none',
    stroke: 'currentColor',
    strokeWidth: 1.6,
    strokeLinecap: 'round',
    strokeLinejoin: 'round',
  }
  const paths = {
    spark: <path d="M12 3v4M12 17v4M3 12h4M17 12h4M6.3 6.3l2.8 2.8M14.9 14.9l2.8 2.8M17.7 6.3l-2.8 2.8M9.1 14.9l-2.8 2.8" />,
    layers: <><path d="M12 2 2 7l10 5 10-5-10-5Z" /><path d="m2 17 10 5 10-5M2 12l10 5 10-5" /></>,
    pen: <><path d="M12 19l7-7 3 3-7 7-3-3z" /><path d="M18 13l-1.5-7.5L2 2l3.5 14.5L13 18l5-5z" /><path d="M2 2l7.586 7.586" /></>,
    heart: <path d="M20.8 4.6a5.5 5.5 0 0 0-7.8 0L12 5.6l-1-1a5.5 5.5 0 0 0-7.8 7.8l1 1L12 21l7.8-7.6 1-1a5.5 5.5 0 0 0 0-7.8z" />,
    gauge: <><path d="M12 14a2 2 0 1 0 0-4 2 2 0 0 0 0 4z" /><path d="M12 14l4-4" /><path d="M3.4 18a9 9 0 1 1 17.2 0" /></>,
    sliders: <><path d="M4 21v-7M4 10V3M12 21v-9M12 8V3M20 21v-5M20 12V3M1 14h6M9 8h6M17 16h6" /></>,
  }
  return <svg {...common}>{paths[name]}</svg>
}

export default function Features() {
  return (
    <section id="features" className="features container">
      <div className="features__head">
        <h2 className="features__title">Make website great again</h2>
        <a href="#intro" className="btn btn--outline">Learn More</a>
      </div>

      <div className="features__grid">
        {features.map((f) => (
          <article key={f.title} className="feature-card">
            <span className="feature-card__icon"><Icon name={f.icon} /></span>
            <h3>{f.title}</h3>
            <p>{f.text}</p>
          </article>
        ))}
      </div>
    </section>
  )
}
