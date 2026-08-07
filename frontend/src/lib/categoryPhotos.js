// Category hero photos now live in the backend (Category.hero_image, set at
// seed/admin time) rather than being hardcoded here — this file only keeps
// the one photo that isn't tied to a specific category: the default/landing
// backdrop shown when no category is selected, and the fallback used if a
// category was created without a hero_image set.
const DEFAULT_PHOTO_ID = '1591123120675-6f7f1aae0e5b' // wide campus path, students walking

export function getHeroPhotoUrl({ width = 1600, quality = 65 } = {}) {
  return `https://images.unsplash.com/photo-${DEFAULT_PHOTO_ID}?w=${width}&q=${quality}&fit=crop&auto=format`
}

// Single source of truth for "which photo represents the current view" —
// the selected category's own hero_image (from the API), or the default
// campus shot when nothing is selected or the category has none set.
// Centralizing this here means any page that needs a background for the
// current category calls this one function instead of re-deriving it.
export function getBackgroundPhotoUrl(category, opts = {}) {
  return category?.hero_image || getHeroPhotoUrl(opts)
}
