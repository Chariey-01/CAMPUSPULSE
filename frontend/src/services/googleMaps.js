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

  // no OS/device detection needed - see explanation below
  window.open(url, '_blank', 'noopener,noreferrer')
}
