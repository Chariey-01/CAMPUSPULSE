import { useState, createElement } from 'react'
import { getCategoryIcon, getCategoryStyle } from '../lib/categoryVisuals'

// Two-tier: the place's own photo (image_url - either admin/owner-entered
// today, or eventually an uploaded file's URL from Cloudinary/Supabase
// Storage) if it loads, otherwise a category-tinted icon tile. Deliberately
// does NOT fall back to a category stock photo - that's the whole point of
// splitting category identity (PageBackground/CategoryBanner) from place
// identity (this component): a card should never borrow its category's
// photo and pass it off as the place's own.
export default function PlaceImage({ place, className = '', iconSize = 28 }) {
  // No place in this app ever changes id without remounting (list items are
  // keyed by place.id, detail pages remount per route param), so the initial
  // stage never needs to re-sync via an effect.
  const [broken, setBroken] = useState(false)

  const style = getCategoryStyle(place?.category)
  const hasPhoto = Boolean(place?.image_url) && !broken

  if (!hasPhoto) {
    const Icon = getCategoryIcon(place?.category?.icon)
    return (
      <div className={`${className} placeholder`} style={style}>
        {createElement(Icon, { size: iconSize, strokeWidth: 1.5 })}
      </div>
    )
  }

  return (
    <div className={className} style={style}>
      <img src={place.image_url} alt={place?.name} loading="lazy" onError={() => setBroken(true)} />
    </div>
  )
}
