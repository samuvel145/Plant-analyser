import DiagnosisCard from './DiagnosisCard'

/**
 * Format plain AI text with basic markdown-like styling.
 */
function AiText({ text }) {
  // Convert **bold** and bullet lists to styled HTML
  const lines = text.split('\n')
  return (
    <div className="ai-prose">
      {lines.map((line, i) => {
        if (!line.trim()) return <br key={i} />

        // Bold: **text**
        const formatted = line.replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>')

        // Bullet points
        if (line.trim().startsWith('- ') || line.trim().startsWith('• ')) {
          return (
            <ul key={i} style={{ marginTop: 0 }}>
              <li dangerouslySetInnerHTML={{ __html: formatted.replace(/^[-•]\s/, '') }} />
            </ul>
          )
        }

        return <p key={i} dangerouslySetInnerHTML={{ __html: formatted }} />
      })}
    </div>
  )
}

/**
 * MessageBubble — renders a single chat message (user or AI).
 *
 * @param {Object}   msg       - message object from state
 * @param {Function} onUpload  - triggers file picker (for action buttons)
 * @param {Function} onAsk     - focuses text input
 * @param {Function} onReset   - resets session
 */
export default function MessageBubble({ msg, onUpload, onAsk, onReset }) {
  const isUser = msg.role === 'user'

  if (isUser) {
    return (
      <div className="msg-row msg-row--user" role="listitem">
        <div className="bubble bubble--user">
          {msg.type === 'image' && msg.imagePreviewUrl && (
            <img
              src={msg.imagePreviewUrl}
              alt="Uploaded plant"
              className="bubble-img"
            />
          )}
          {msg.text && <span>{msg.text}</span>}
          {msg.type === 'image' && !msg.text && (
            <span style={{ opacity: 0.75, fontSize: '0.82rem' }}>
              📸 Sent an image for analysis
            </span>
          )}
        </div>
      </div>
    )
  }

  // AI messages
  if (msg.type === 'diagnosis') {
    return (
      <div className="msg-row msg-row--ai" role="listitem">
        <div className="msg-avatar msg-avatar--ai">🌿</div>
        <DiagnosisCard
          data={msg.data}
          onUpload={onUpload}
          onAsk={onAsk}
          onReset={onReset}
        />
      </div>
    )
  }

  if (msg.type === 'guardrail') {
    return (
      <div className="msg-row msg-row--ai" role="listitem">
        <div className="msg-avatar msg-avatar--ai">🌿</div>
        <div className="bubble bubble--ai bubble--guardrail">
          {msg.text}
        </div>
      </div>
    )
  }

  // Default: plain text AI message
  return (
    <div className="msg-row msg-row--ai" role="listitem">
      <div className="msg-avatar msg-avatar--ai">🌿</div>
      <div className="bubble bubble--ai">
        <AiText text={msg.text || ''} />
      </div>
    </div>
  )
}
