const words = ['Responsive', 'Modern', 'Engaging', 'Minimalistic', 'Versatile', 'Intuitive']

export default function WordStack() {
  return (
    <section className="wordstack">
      <div className="wordstack__overlay" />
      <div className="wordstack__inner container">
        {words.map((w) => (
          <h2 key={w} className="wordstack__word">{w}</h2>
        ))}
      </div>
    </section>
  )
}
