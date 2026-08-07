import {
  Utensils,
  BookOpen,
  Dumbbell,
  Home,
  HeartPulse,
  Pencil,
  Bus,
  Music2,
  MapPin,
} from 'lucide-react'

// Maps the `icon` string stored on each category (set at seed/admin time) to a
// Lucide icon component. Unrecognized keys fall back to a generic pin below.
const ICON_MAP = {
  utensils: Utensils,
  book: BookOpen,
  dumbbell: Dumbbell,
  home: Home,
  'heart-pulse': HeartPulse,
  pencil: Pencil,
  bus: Bus,
  music: Music2,
}

export function getCategoryIcon(iconKey) {
  return ICON_MAP[iconKey?.toLowerCase()] || MapPin
}

// Categories are admin-created and open-ended, so identity color is derived
// from the id (stable, deterministic) rather than a fixed name lookup —
// every category gets one of 8 curated hues without needing a mapping table.
export function getCategoryColor(categoryId) {
  const n = Number.isFinite(categoryId) ? categoryId : 0
  const index = ((n - 1) % 8 + 8) % 8
  return `var(--cat-${index + 1})`
}

export function getCategoryTint(categoryId) {
  return `color-mix(in srgb, ${getCategoryColor(categoryId)} 14%, transparent)`
}

// Spreadable inline style that scopes --cat-color/--cat-tint to a subtree,
// so shared CSS (place cards, banners, pills) can pick up each category's
// identity color via var(--cat-color, var(--accent)).
export function getCategoryStyle(category) {
  return {
    '--cat-color': getCategoryColor(category?.id),
    '--cat-tint': getCategoryTint(category?.id),
  }
}
