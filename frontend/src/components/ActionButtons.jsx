/**
 * ActionButtons — CTA buttons shown after every AI diagnosis response.
 */
export default function ActionButtons({ onUpload, onAsk, onReset }) {
  return (
    <div className="action-buttons">
      <button
        className="action-btn action-btn--upload"
        onClick={onUpload}
        aria-label="Upload another plant image"
      >
        📸 Upload another image
      </button>
      <button
        className="action-btn action-btn--chat"
        onClick={onAsk}
        aria-label="Ask a follow-up question"
      >
        💬 Ask a question
      </button>
      <button
        className="action-btn action-btn--reset"
        onClick={onReset}
        aria-label="Start a new session"
      >
        🔄 Start over
      </button>
    </div>
  )
}
