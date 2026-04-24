import { useCallback, useState } from 'react'
import ChatWindow from './components/ChatWindow'
import InputBar from './components/InputBar'
import { useChat } from './hooks/useChat'

export default function App() {
  const {
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
  } = useChat()

  const [resetConfirm, setResetConfirm] = useState(false)

  const handleResetClick = useCallback(() => {
    if (messages.length === 0) return
    if (resetConfirm) {
      handleReset()
      setResetConfirm(false)
    } else {
      setResetConfirm(true)
      setTimeout(() => setResetConfirm(false), 3000)
    }
  }, [resetConfirm, handleReset, messages.length])

  const handleChipClick = useCallback(
    (chip) => {
      sendMessage(chip)
    },
    [sendMessage]
  )

  return (
    <div className="app-shell">
      {/* ── Header ─────────────────────────── */}
      <header className="header" role="banner">
        <div className="header-brand">
          <span className="header-logo">🌿</span>
          <div>
            <div className="header-title">PlantMD</div>
            <div className="header-tagline">AI Plant Disease Diagnostics</div>
          </div>
        </div>

        <button
          className="header-reset-btn"
          onClick={handleResetClick}
          aria-label="Start a new session"
          title={resetConfirm ? 'Click again to confirm' : 'Start over'}
          style={resetConfirm ? { borderColor: 'rgba(239,68,68,0.6)', color: '#f87171' } : {}}
        >
          🔄 {resetConfirm ? 'Confirm?' : 'Start Over'}
        </button>
      </header>

      {/* ── Chat area ──────────────────────── */}
      <ChatWindow
        messages={messages}
        isLoading={isLoading}
        chatEndRef={chatEndRef}
        onUpload={triggerFilePicker}
        onAsk={focusTextInput}
        onReset={handleResetClick}
        onChipClick={handleChipClick}
      />

      {/* ── Input bar ──────────────────────── */}
      <InputBar
        onSend={sendMessage}
        onFileChange={handleFileInputChange}
        pendingImage={pendingImage}
        onClearImage={clearPendingImage}
        fileInputRef={fileInputRef}
        textInputRef={textInputRef}
        isLoading={isLoading}
      />

      {/* ── Error toast ────────────────────── */}
      {error && (
        <div className="error-toast" role="alert" aria-live="assertive">
          ⚠️ {error}
        </div>
      )}
    </div>
  )
}
