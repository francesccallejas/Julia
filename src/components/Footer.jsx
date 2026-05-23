import { useState } from 'react'

const columns = [
  { title: 'Pages', links: ['Homepage 1', 'Homepage 2', 'Homepage 3', 'About 1', 'About 2', 'About 3'] },
  { title: 'Content', links: ['Pricing', 'Product', 'Blog', 'Stories', 'FAQ', '404'] },
  { title: 'Utility', links: ['Privacy Policy', 'Contact 1', 'Contact 2', 'Contact 3', 'Password'] },
]

function Social() {
  const icons = ['M22 12a10 10 0 1 0-11.6 9.9v-7H7.9V12h2.5V9.8c0-2.5 1.5-3.9 3.8-3.9 1.1 0 2.2.2 2.2.2v2.5h-1.2c-1.2 0-1.6.8-1.6 1.6V12h2.7l-.4 2.9h-2.3v7A10 10 0 0 0 22 12z']
  return (
    <div className="footer__social">
      {['in', 'X', 'IG', 'be'].map((s) => (
        <a key={s} href="#hero" aria-label={s}>{s}</a>
      ))}
    </div>
  )
}

export default function Footer() {
  const [email, setEmail] = useState('')
  const [sent, setSent] = useState(false)

  const submit = (e) => {
    e.preventDefault()
    if (!email) return
    setSent(true)
    setEmail('')
    setTimeout(() => setSent(false), 3500)
  }

  return (
    <footer className="footer">
      <div className="footer__top container">
        <div className="footer__news">
          <h3>Stay in the loop</h3>
          <p>Get template updates and design tips—no spam, ever.</p>
          <form className="footer__form" onSubmit={submit}>
            <input
              type="email"
              required
              placeholder="Enter your email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
            />
            <button type="submit" className="btn btn--light">Subscribe</button>
          </form>
          {sent && <p className="footer__sent">Thanks! You're on the list. ✓</p>}
        </div>

        <div className="footer__cols">
          {columns.map((c) => (
            <div key={c.title} className="footer__col">
              <h4>{c.title}</h4>
              <ul>
                {c.links.map((l) => (
                  <li key={l}><a href="#hero">{l}</a></li>
                ))}
              </ul>
            </div>
          ))}
        </div>
      </div>

      <div className="footer__wordmark container">
        <span>For:Human<sup>™</sup></span>
      </div>

      <div className="footer__bottom container">
        <p>© {new Date().getFullYear()} For:Human™. All rights reserved.</p>
        <Social />
      </div>
    </footer>
  )
}
