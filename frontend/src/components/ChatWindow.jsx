import MessageBubble from './MessageBubble'
import TypingIndicator from './TypingIndicator'

/**
 * Starter prompts shown when there are no messages yet.
 */
const WELCOME_CHIPS = [
  'What causes powdery mildew?',
  'How do I treat early blight?',
  'Is neem oil safe for vegetables?',
  'How often should I water tomatoes?',
]

/**
 * ChatWindow — the main scrollable message history area.
 */
export default function ChatWindow({
  messages,
  isLoading,
  chatEndRef,
  onUpload,
  onAsk,
  onReset,
  onChipClick,
}) {
  const isEmpty = messages.length === 0

  return (
    <main className="chat-window" role="log" aria-live="polite" aria-label="Chat history">
      {/* Welcome / empty state */}
      {isEmpty && (
        <div className="welcome-card">
          <span className="welcome-icon">🌿</span>
          <h1 className="welcome-title">PlantMD</h1>
          <p className="welcome-subtitle">
            Upload a photo of your plant or leaf and I'll give you an instant
            AI-powered disease diagnosis with treatment recommendations.
          </p>
          <div className="welcome-chips" role="list" aria-label="Suggested questions">
            {WELCOME_CHIPS.map((chip) => (
              <button
                key={chip}
                className="welcome-chip"
                role="listitem"
                onClick={() => onChipClick(chip)}
                aria-label={`Ask: ${chip}`}
              >
                {chip}
              </button>
            ))}
          </div>
        </div>
      )}

      {/* Message list */}
      {messages.map((msg) => (
        <MessageBubble
          key={msg.id}
          msg={msg}
          onUpload={onUpload}
          onAsk={onAsk}
          onReset={onReset}
        />
      ))}

      {/* Typing indicator */}
      {isLoading && <TypingIndicator />}

      {/* Scroll anchor */}
      <div ref={chatEndRef} />
    </main>
  )
}
