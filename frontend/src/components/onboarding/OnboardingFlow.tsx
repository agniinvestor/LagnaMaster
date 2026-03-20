// frontend/src/components/onboarding/OnboardingFlow.tsx — Session 83
// 4-screen onboarding with consent capture
'use client'
import { useState } from 'react'

const SCREENS = [
  {
    title: 'What LagnaMaster is',
    body: 'LagnaMaster is a personal timing and guidance companion inspired by Vedic Jyotish. It helps you reflect on your circumstances, understand timing patterns, and make decisions with more clarity.',
    cta: 'Continue',
  },
  {
    title: 'What LagnaMaster is not',
    body: 'LagnaMaster is not a predictor, oracle, or authority. It does not make financial, medical, legal, or relationship decisions for you. All guidance is reflective and supportive — not prescriptive.',
    cta: 'I understand',
  },
  {
    title: 'How to use it wisely',
    body: 'Use guidance as one input among many. Combine it with your own judgment, trusted advisors, and professional expertise. It works best when you approach it with curiosity, not dependency.',
    cta: 'Got it',
  },
  {
    title: 'Your consent',
    body: 'By continuing, you consent to LagnaMaster storing your birth data and computed chart for guidance purposes. You can withdraw consent and delete all your data at any time from Settings.',
    cta: 'I consent and continue',
    isConsent: true,
  },
]

interface Props { onComplete: (consented: boolean) => void }

export function OnboardingFlow({ onComplete }: Props) {
  const [screen, setScreen] = useState(0)
  const current = SCREENS[screen]

  return (
    <div className="min-h-screen bg-slate-950 flex items-center justify-center p-6">
      <div className="max-w-lg w-full space-y-8">
        {/* Progress */}
        <div className="flex gap-2">
          {SCREENS.map((_, i) => (
            <div key={i} className={`h-0.5 flex-1 rounded-full transition-colors
              ${i <= screen ? 'bg-blue-500' : 'bg-slate-800'}`} />
          ))}
        </div>

        {/* Content */}
        <div className="space-y-4">
          <h1 className="text-white text-xl font-medium">{current.title}</h1>
          <p className="text-slate-400 text-base leading-relaxed">{current.body}</p>
        </div>

        {/* Legal note for consent screen */}
        {current.isConsent && (
          <p className="text-slate-600 text-xs">
            Your data is encrypted and never sold. GDPR Article 17 right to erasure applies.
            See our Privacy Policy for details.
          </p>
        )}

        {/* Actions */}
        <div className="flex gap-3">
          {screen > 0 && (
            <button onClick={() => setScreen(s => s - 1)}
              className="px-4 py-2 text-slate-400 text-sm hover:text-slate-300 transition-colors">
              Back
            </button>
          )}
          <button
            onClick={() => {
              if (screen < SCREENS.length - 1) setScreen(s => s + 1)
              else onComplete(true)
            }}
            className="flex-1 px-6 py-3 bg-blue-600 hover:bg-blue-500 text-white
                       text-sm font-medium rounded-lg transition-colors">
            {current.cta}
          </button>
          {current.isConsent && (
            <button onClick={() => onComplete(false)}
              className="px-4 py-2 text-slate-600 text-sm hover:text-slate-500 transition-colors">
              Decline
            </button>
          )}
        </div>
      </div>
    </div>
  )
}
