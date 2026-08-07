import { api } from '../api/client'

// Uploads a single image file: gets a short-lived signed credential from our
// own backend (proves the upload comes from a logged-in user), then sends
// the file straight to Cloudinary - our server never sees the image bytes,
// it only ever stores the secure_url this resolves to.
export async function uploadImage(file) {
  const { signature, timestamp, api_key: apiKey, cloud_name: cloudName, folder } =
    await api.post('/api/uploads/signature')

  const formData = new FormData()
  formData.append('file', file)
  formData.append('api_key', apiKey)
  formData.append('timestamp', timestamp)
  formData.append('signature', signature)
  formData.append('folder', folder)

  const response = await fetch(`https://api.cloudinary.com/v1_1/${cloudName}/image/upload`, {
    method: 'POST',
    body: formData,
  })

  const data = await response.json()

  if (!response.ok) {
    throw new Error(data?.error?.message || 'Image upload failed')
  }

  return data.secure_url
}
