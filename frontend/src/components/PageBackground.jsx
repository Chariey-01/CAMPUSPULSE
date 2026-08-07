// Fixed, full-viewport photo layer with a dark readability scrim. Knows
// nothing about categories — it just paints whatever photoUrl it's given —
// so any page that wants a photographic backdrop reuses this one component
// instead of re-implementing the fixed/cover/overlay CSS itself.
export default function PageBackground({ photoUrl }) {
  return (
    <div
      className="page-background"
      style={{ backgroundImage: `url(${photoUrl})` }}
      aria-hidden="true"
    />
  )
}
