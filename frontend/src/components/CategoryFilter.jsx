import { createElement } from 'react'
import { LayoutGrid } from 'lucide-react'
import { getCategoryIcon, getCategoryStyle } from '../lib/categoryVisuals'

export default function CategoryFilter({ categories, selected, onChange }) {
  return (
    <div className="category-filter">
      <button
        type="button"
        className={`category-chip ${selected === '' ? 'active' : ''}`}
        onClick={() => onChange('')}
      >
        <LayoutGrid size={14} strokeWidth={2} />
        All
      </button>
      {categories.map((category) => {
        const Icon = getCategoryIcon(category.icon)
        const isActive = selected === String(category.id)
        return (
          <button
            type="button"
            key={category.id}
            // `selected` comes from a URL query param (always a string), while
            // category.id is numeric - String() keeps the comparison type-safe
            className={`category-chip ${isActive ? 'active' : ''}`}
            style={isActive ? undefined : getCategoryStyle(category)}
            onClick={() => onChange(String(category.id))}
          >
            {createElement(Icon, { size: 14, strokeWidth: 2, color: isActive ? undefined : 'var(--cat-color)' })}
            {category.name}
          </button>
        )
      })}
    </div>
  )
}
