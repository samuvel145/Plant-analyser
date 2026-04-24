/**
 * TypingIndicator — animated three-dot loader shown while AI is thinking.
 */
export default function TypingIndicator() {
  return (
    <div className="msg-row msg-row--ai">
      <div className="msg-avatar msg-avatar--ai">🌿</div>
      <div className="bubble bubble--ai">
        <div className="typing-indicator">
          <span className="typing-dot" />
          <span className="typing-dot" />
          <span className="typing-dot" />
        </div>
      </div>
    </div>
  )
}
