import axios from 'axios'

const api = axios.create({
  baseURL: '/api',
  timeout: 35000,
})

/**
 * Upload a plant image for disease analysis.
 * @param {File} imageFile - The image file to upload
 * @param {string} sessionId - UUID session identifier
 * @param {string|null} message - Optional accompanying note
 */
export async function analyseImage(imageFile, sessionId, message = null) {
  const formData = new FormData()
  formData.append('image', imageFile)
  formData.append('session_id', sessionId)
  if (message) formData.append('message', message)

  const response = await api.post('/analyse', formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
  })
  return response.data
}

/**
 * Send a conversational follow-up message.
 * @param {string} sessionId - UUID session identifier
 * @param {string} message - User's text message
 */
export async function sendChat(sessionId, message) {
  const response = await api.post('/chat', { session_id: sessionId, message })
  return response.data
}

/**
 * Reset/clear the current session.
 * @param {string} sessionId - UUID session identifier
 */
export async function resetSession(sessionId) {
  const response = await api.delete(`/session/${sessionId}`)
  return response.data
}

/**
 * Health check.
 */
export async function healthCheck() {
  const response = await api.get('/health')
  return response.data
}
