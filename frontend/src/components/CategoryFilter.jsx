export default function CategoryFilter({ categories, selected, onChange }) {
  return (
    <div className="category-filter">
      <button className={selected === '' ? 'active' : ''} onClick={() => onChange('')}>
        All
      </button>
      {categories.map((category) => (
        <button
          key={category.id}
          className={selected === String(category.id) ? 'active' : ''}
          onClick={() => onChange(String(category.id))}
        >
          {category.name}
        </button>
      ))}
    </div>
  )
}
