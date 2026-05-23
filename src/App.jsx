import Navbar from './components/Navbar.jsx'
import Hero from './components/Hero.jsx'
import Intro from './components/Intro.jsx'
import Features from './components/Features.jsx'
import WordStack from './components/WordStack.jsx'
import Sustainability from './components/Sustainability.jsx'
import FirstImpression from './components/FirstImpression.jsx'
import TemplateCombines from './components/TemplateCombines.jsx'
import Testimonials from './components/Testimonials.jsx'
import Faq from './components/Faq.jsx'
import Logos from './components/Logos.jsx'
import Cta from './components/Cta.jsx'
import Footer from './components/Footer.jsx'

export default function App() {
  return (
    <div className="site">
      <Navbar />
      <main>
        <Hero />
        <Intro />
        <Features />
        <WordStack />
        <Sustainability />
        <FirstImpression />
        <TemplateCombines />
        <Testimonials />
        <Faq />
        <Logos />
        <Cta />
      </main>
      <Footer />
    </div>
  )
}
