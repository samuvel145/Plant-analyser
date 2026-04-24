import { useState, useRef, useCallback } from 'react'

/**
 * InputBar — fixed-bottom text input + image upload button.
 *
 * @param {Function} onSend          - called with (text) when user submits
 * @param {Function} onFileChange    - called with file input change event
 * @param {Object}   pendingImage    - { file, previewUrl } or null
 * @param {Function} onClearImage    - clears pending image
 * @param {Object}   fileInputRef    - ref for the hidden file input
 * @param {Object}   textInputRef    - ref for the textarea
 * @param {boolean}  isLoading       - disables input while AI is responding
 */
export default function InputBar({
  onSend,
  onFileChange,
  pendingImage,
  onClearImage,
  fileInputRef,
  textInputRef,
  isLoading,
}) {
  const [text, setText] = useState('')

  const canSend = (text.trim().length > 0 || !!pendingImage) && !isLoading

  const handleSubmit = useCallback(() => {
    if (!canSend) return
    onSend(text.trim())
    setText('')
  }, [canSend, onSend, text])

  const handleKeyDown = useCallback(
    (e) => {
      if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault()
        handleSubmit()
      }
    },
    [handleSubmit]
  )

  const handleTextChange = (e) => {
    setText(e.target.value)
    // Auto-resize textarea
    e.target.style.height = 'auto'
    e.target.style.height = Math.min(e.target.scrollHeight, 80) + 'px'
  }

  return (
    <div className="input-bar-wrap">
      {/* Image preview strip */}
      {pendingImage && (
        <div className="img-preview-strip" role="status" aria-label="Image queued for upload">
          <img
            src={pendingImage.previewUrl}
            alt="Preview"
            className="img-preview-thumb"
          />
          <span className="img-preview-name">{pendingImage.file.name}</span>
          <button
            className="img-preview-remove"
            onClick={onClearImage}
            aria-label="Remove selected image"
            title="Remove image"
          >
            ✕
          </button>
        </div>
      )}

      {/* Main input row */}
      <div className="input-bar">
        {/* Hidden file input */}
        <input
          ref={fileInputRef}
          type="file"
          accept="image/jpeg,image/png,image/webp"
          style={{ display: 'none' }}
          onChange={onFileChange}
          aria-label="Upload plant image"
          id="plant-image-upload"
        />

        {/* Clip / upload button */}
        <button
          type="button"
          className="input-icon-btn input-icon-btn--clip"
          onClick={() => fileInputRef.current?.click()}
          aria-label="Attach plant image"
          title="Upload plant image"
          disabled={isLoading}
        >
          📎
        </button>

        {/* Text area */}
        <textarea
          ref={textInputRef}
          className="input-textarea"
          placeholder={
            pendingImage
              ? 'Add a note (optional)…'
              : 'Ask about plant diseases, or upload a photo…'
          }
          value={text}
          onChange={handleTextChange}
          onKeyDown={handleKeyDown}
          disabled={isLoading}
          rows={1}
          aria-label="Message input"
          id="chat-message-input"
        />

        {/* Send button */}
        <button
          type="button"
          className="input-icon-btn input-icon-btn--send"
          onClick={handleSubmit}
          disabled={!canSend}
          aria-label="Send message"
          title="Send"
        >
          ➤
        </button>
      </div>
    </div>
  )
}
