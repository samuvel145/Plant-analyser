import { useState, useRef, useCallback, useEffect } from 'react'
import { v4 as uuidv4 } from 'uuid'
import { analyseImage, sendChat, resetSession } from '../api/agentApi'
import { validateImageFile, createImagePreview, revokeImagePreview } from '../utils/imageUtils'

const SESSION_KEY = 'plantmd_session_id'

function getOrCreateSessionId() {
  let id = sessionStorage.getItem(SESSION_KEY)
  if (!id) {
    id = uuidv4()
    sessionStorage.setItem(SESSION_KEY, id)
  }
  return id
}

export function useChat() {
  const [messages, setMessages] = useState([])
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState(null)
  const [pendingImage, setPendingImage] = useState(null) // { file, previewUrl }
  const sessionId = useRef(getOrCreateSessionId())
  const fileInputRef = useRef(null)
  const textInputRef = useRef(null)
  const chatEndRef = useRef(null)

  // Auto-scroll to latest message
  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages, isLoading])

  // Clear error after 4s
  useEffect(() => {
    if (!error) return
    const t = setTimeout(() => setError(null), 4000)
    return () => clearTimeout(t)
  }, [error])

  const addMessage = useCallback((msg) => {
    setMessages((prev) => [...prev, { id: uuidv4(), ...msg }])
  }, [])

  const clearPendingImage = useCallback(() => {
    if (pendingImage?.previewUrl) revokeImagePreview(pendingImage.previewUrl)
    setPendingImage(null)
  }, [pendingImage])

  /** Handle image file selection */
  const handleImageSelect = useCallback((file) => {
    const { valid, error: err } = validateImageFile(file)
    if (!valid) {
      setError(err)
      return
    }
    clearPendingImage()
    setPendingImage({
      file,
      previewUrl: createImagePreview(file),
    })
  }, [clearPendingImage])

  /** Handle file input change */
  const handleFileInputChange = useCallback((e) => {
    const file = e.target.files?.[0]
    if (file) handleImageSelect(file)
    // Reset so same file can be re-selected
    if (fileInputRef.current) fileInputRef.current.value = ''
  }, [handleImageSelect])

  /** Send message (image or text) */
  const sendMessage = useCallback(async (text) => {
    if (!text?.trim() && !pendingImage) return
    if (isLoading) return

    setIsLoading(true)
    setError(null)

    try {
      if (pendingImage) {
        // Add user bubble with image + optional text
        addMessage({
          role: 'user',
          type: 'image',
          imagePreviewUrl: pendingImage.previewUrl,
          text: text?.trim() || null,
        })

        const data = await analyseImage(
          pendingImage.file,
          sessionId.current,
          text?.trim() || null
        )

        if (data.type === 'diagnosis') {
          addMessage({ role: 'ai', type: 'diagnosis', data: data.data })
        } else if (data.type === 'guardrail') {
          addMessage({ role: 'ai', type: 'guardrail', text: data.message })
        }

        // Keep preview URL alive (used in bubble) — don't revoke
        setPendingImage(null)
      } else {
        // Text-only chat
        addMessage({ role: 'user', type: 'text', text: text.trim() })

        const data = await sendChat(sessionId.current, text.trim())

        if (data.type === 'chat') {
          addMessage({ role: 'ai', type: 'text', text: data.message })
        } else if (data.type === 'guardrail') {
          addMessage({ role: 'ai', type: 'guardrail', text: data.message })
        }
      }
    } catch (err) {
      const detail =
        err?.response?.data?.detail ||
        err?.response?.data?.message ||
        'Something went wrong. Please try again.'
      setError(detail)
    } finally {
      setIsLoading(false)
    }
  }, [pendingImage, isLoading, addMessage])

  /** Reset session */
  const handleReset = useCallback(async () => {
    try {
      await resetSession(sessionId.current)
    } catch (_) { /* silent */ }

    // Generate new session ID
    const newId = uuidv4()
    sessionStorage.setItem(SESSION_KEY, newId)
    sessionId.current = newId

    setMessages([])
    clearPendingImage()
    setError(null)
    setIsLoading(false)
  }, [clearPendingImage])

  /** Trigger file picker */
  const triggerFilePicker = useCallback(() => {
    fileInputRef.current?.click()
  }, [])

  /** Focus text input */
  const focusTextInput = useCallback(() => {
    textInputRef.current?.focus()
  }, [])

  return {
    messages,
    isLoading,
    error,
    pendingImage,
    fileInputRef,
    textInputRef,
    chatEndRef,
    sendMessage,
    handleReset,
    handleFileInputChange,
    clearPendingImage,
    triggerFilePicker,
    focusTextInput,
  }
}
