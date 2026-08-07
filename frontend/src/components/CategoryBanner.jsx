import { createElement } from 'react'
import { getCategoryIcon, getCategoryStyle } from '../lib/categoryVisuals'

// Gives the currently-selected category a named identity (icon, name,
// description) inside the content panel. It used to fetch its own copy of
// the category photo for a boxed banner — now redundant, since PageBackground
// already puts that same photo behind the whole page — so this stays a
// lightweight text/icon strip instead of duplicating the image fetch.
export default function CategoryBanner({ category }) {
  if (!category) return null

  const Icon = getCategoryIcon(category.icon)
  const style = getCategoryStyle(category)

  return (
    <div className="category-banner" style={style}>
      <span className="cat-icon">
        {createElement(Icon, { size: 22, strokeWidth: 1.6 })}
      </span>
      <div>
        <h2>{category.name}</h2>
        {category.description && <p>{category.description}</p>}
      </div>
    </div>
  )
}
