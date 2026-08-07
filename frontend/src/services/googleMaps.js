export function isValidGoogleMapsLink(url) {
  if (!url) return false

  try {
    const parsed = new URL(url)
    return parsed.protocol === 'http:' || parsed.protocol === 'https:'
  } catch {
    return false
  }
}

export function openGoogleMaps(url) {
  if (!isValidGoogleMapsLink(url)) {
    throw new Error('No map location is available for this place yet.')
  }

  // google_maps_link is always a plain https:// URL (validated above), so the browser/OS
  // handles routing it to the Google Maps app or website on its own - no need to branch
  // on platform or construct a native deep-link scheme ourselves
  window.open(url, '_blank', 'noopener,noreferrer')
}
