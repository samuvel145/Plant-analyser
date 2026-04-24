/**
 * Client-side image validation utilities.
 */

const ALLOWED_TYPES = ['image/jpeg', 'image/png', 'image/webp']
const MAX_SIZE_MB = 10
const MAX_SIZE_BYTES = MAX_SIZE_MB * 1024 * 1024

/**
 * Validate an image file before upload.
 * @param {File} file
 * @returns {{ valid: boolean, error: string|null }}
 */
export function validateImageFile(file) {
  if (!file) return { valid: false, error: 'No file selected.' }

  if (!ALLOWED_TYPES.includes(file.type)) {
    return {
      valid: false,
      error: 'Only JPEG, PNG, and WEBP images are supported.',
    }
  }

  if (file.size > MAX_SIZE_BYTES) {
    return {
      valid: false,
      error: `Image too large. Maximum size is ${MAX_SIZE_MB} MB.`,
    }
  }

  if (file.size === 0) {
    return { valid: false, error: 'The selected file is empty.' }
  }

  return { valid: true, error: null }
}

/**
 * Create an object URL preview for a file.
 * @param {File} file
 * @returns {string} Object URL
 */
export function createImagePreview(file) {
  return URL.createObjectURL(file)
}

/**
 * Revoke an object URL to free memory.
 * @param {string} url
 */
export function revokeImagePreview(url) {
  URL.revokeObjectURL(url)
}
