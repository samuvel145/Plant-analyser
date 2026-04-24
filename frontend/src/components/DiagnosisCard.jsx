import { useEffect, useRef } from 'react'
import ActionButtons from './ActionButtons'

/**
 * Maps confidence colour key → CSS class names for bar and badge.
 */
const COLOUR_MAP = {
  green:        { bar: 'conf-green',       badge: 'badge-green' },
  'light-green':{ bar: 'conf-light-green', badge: 'badge-light-green' },
  amber:        { bar: 'conf-amber',       badge: 'badge-amber' },
  orange:       { bar: 'conf-orange',      badge: 'badge-orange' },
  red:          { bar: 'conf-red',         badge: 'badge-red' },
}

/**
 * Parse a confidence string like "91%" → 91.
 */
function parseConfidenceInt(str) {
  const match = str?.match(/\d+/)
  return match ? Math.min(100, parseInt(match[0], 10)) : 0
}

/**
 * Determine confidence colour from percentage.
 */
function getColour(pct) {
  if (pct >= 90) return 'green'
  if (pct >= 75) return 'light-green'
  if (pct >= 55) return 'amber'
  if (pct >= 35) return 'orange'
  return 'red'
}

function getTierLabel(pct) {
  if (pct >= 90) return 'Very High'
  if (pct >= 75) return 'High'
  if (pct >= 55) return 'Moderate'
  if (pct >= 35) return 'Low'
  return 'Very Low'
}

/**
 * DiagnosisCard — renders structured plant disease diagnosis result.
 *
 * @param {Object} data - diagnosis data from API
 * @param {Function} onUpload - callback to trigger file picker
 * @param {Function} onAsk - callback to focus text input
 * @param {Function} onReset - callback to reset session
 */
export default function DiagnosisCard({ data, onUpload, onAsk, onReset }) {
  const confInt = parseConfidenceInt(data.confidence)
  const colour  = data.confidence_colour || getColour(confInt)
  const tier    = data.confidence_tier   || getTierLabel(confInt)
  const colours = COLOUR_MAP[colour] || COLOUR_MAP['green']

  const barRef = useRef(null)

  // Animate bar width after mount
  useEffect(() => {
    if (!barRef.current) return
    barRef.current.style.width = '0%'
    const t = setTimeout(() => {
      if (barRef.current) barRef.current.style.width = `${confInt}%`
    }, 80)
    return () => clearTimeout(t)
  }, [confInt])

  const isHealthy = data.disease?.toLowerCase().includes('none detected') ||
                    data.disease?.toLowerCase().includes('healthy')

  return (
    <div className="diagnosis-card" role="region" aria-label="Diagnosis result">
      {/* Header */}
      <div className="diagnosis-header">
        <span>{isHealthy ? '✅' : '🔬'}</span>
        <span className="diagnosis-badge">
          {isHealthy ? 'Healthy Plant' : 'Diagnosis Complete'}
        </span>
      </div>

      {/* Plant */}
      <div className="diagnosis-row">
        <span className="diagnosis-label">🌱 Plant</span>
        <span className="diagnosis-value">{data.plant}</span>
      </div>

      {/* Disease */}
      <div className="diagnosis-row">
        <span className="diagnosis-label">🦠 Disease</span>
        <span className="diagnosis-value" style={{ color: isHealthy ? '#5da85d' : '#dceddc' }}>
          {data.disease}
        </span>
      </div>

      {/* Confidence */}
      <div className="diagnosis-row" style={{ flexDirection: 'column', gap: '0.3rem' }}>
        <div style={{ display: 'flex', alignItems: 'center' }}>
          <span className="diagnosis-label">📊 Confidence</span>
          <span className="diagnosis-value">
            {data.confidence}
            <span className={`conf-tier-badge ${colours.badge}`}>{tier}</span>
          </span>
        </div>
        <div className="confidence-bar-wrap" style={{ marginLeft: '0' }}>
          <div
            ref={barRef}
            className={`confidence-bar-fill ${colours.bar}`}
            style={{ width: '0%', transition: 'width 0.8s cubic-bezier(0.4,0,0.2,1)' }}
            role="progressbar"
            aria-valuenow={confInt}
            aria-valuemin={0}
            aria-valuemax={100}
          />
        </div>
      </div>

      {/* Symptoms */}
      {data.symptoms?.length > 0 && (
        <>
          <p className="diagnosis-section-title">🔍 Symptoms</p>
          <ul className="diagnosis-list">
            {data.symptoms.map((s, i) => (
              <li key={i}>{s}</li>
            ))}
          </ul>
        </>
      )}

      {/* Treatment */}
      {data.treatment?.length > 0 && (
        <>
          <p className="diagnosis-section-title">💊 Treatment</p>
          <ol className="diagnosis-list">
            {data.treatment.map((t, i) => (
              <li key={i}>{t}</li>
            ))}
          </ol>
        </>
      )}

      {/* Low confidence disclaimer */}
      {confInt < 35 && (
        <div className="disclaimer-box" role="alert">
          ⚠️ This result has low confidence. Please consult a local agricultural
          extension officer for confirmation.
        </div>
      )}

      {/* Action Buttons */}
      <ActionButtons onUpload={onUpload} onAsk={onAsk} onReset={onReset} />
    </div>
  )
}
