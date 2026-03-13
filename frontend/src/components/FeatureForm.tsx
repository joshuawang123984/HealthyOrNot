import { useState } from 'react'
import type { FeatureDesc } from '../types'

interface Props {
    features: string[]
    featuresDesc: { [key: string]: FeatureDesc }
    dataset: string
    onSubmit: (prediction: number) => void
}

export default function FeatureForm({ features, featuresDesc, dataset, onSubmit }: Props) {
    const [values, setValues] = useState<{ [key: string]: string }>({})
    const [loading, setLoading] = useState(false)

    const handleChange = (feature: string, value: string) => {
        setValues(prev => ({ ...prev, [feature]: value }))
    }

    const handleSubmit = () => {
        setLoading(true)
        const featureValues = features.map(f => parseFloat(values[f] || '0'))

        fetch('http://localhost:5001/predict', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ dataset, features: featureValues })
        })
            .then(res => res.json())
            .then(data => { onSubmit(data.prediction); setLoading(false) })
            .catch(() => setLoading(false))
    }

    const filled = features.filter(f => values[f] !== undefined && values[f] !== '').length
    const progress = features.length > 0 ? (filled / features.length) * 100 : 0

    return (
        <div className="flex flex-col gap-5">

            {/* progress bar */}
            <div className="flex items-center gap-3">
                <div className="flex-1 h-0.5 bg-gray-800 rounded overflow-hidden">
                    <div
                        className="h-full bg-emerald-400 rounded transition-all duration-300"
                        style={{ width: `${progress}%` }}
                    />
                </div>
                <span className="text-xs text-gray-500 tabular-nums">{filled}/{features.length}</span>
            </div>

            {/* features table */}
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3">
                {features.map(feature => {
                    const desc = featuresDesc?.[feature]
                    return (
                        <div key={feature} className="group flex flex-col gap-1.5">
                            <label className="flex items-center justify-between gap-2">
                                <span className="text-xs text-gray-300 font-medium truncate" title={feature}>
                                    {feature}
                                </span>
                                {desc?.type && (
                                    <span className="text-[10px] text-gray-600 border border-gray-800 rounded px-1.5 py-0.5 shrink-0">
                                        {desc.type}
                                    </span>
                                )}
                            </label>
                            {desc?.description && (
                                <p className="text-[10px] text-gray-600 leading-relaxed">
                                    {desc.description}
                                </p>
                            )}
                            <input
                                type="number"
                                value={values[feature] || ''}
                                onChange={e => handleChange(feature, e.target.value)}
                                placeholder="0"
                                className="w-full bg-gray-950 border border-gray-800 rounded px-3 py-2 text-sm text-gray-100 placeholder-gray-700
                                           focus:outline-none focus:border-emerald-500 focus:ring-1 focus:ring-emerald-500/30
                                           transition-colors [appearance:textfield] [&::-webkit-outer-spin-button]:appearance-none [&::-webkit-inner-spin-button]:appearance-none"
                            />
                        </div>
                    )
                })}
            </div>

            {/* submit section */}
            <div className="flex justify-end pt-1">
                <button
                    onClick={handleSubmit}
                    disabled={loading}
                    className="flex items-center gap-2 bg-emerald-500 hover:bg-emerald-400 disabled:bg-gray-800 disabled:text-gray-600
                               text-gray-950 text-sm font-semibold px-5 py-2 rounded transition-colors cursor-pointer disabled:cursor-not-allowed"
                >
                    {loading ? (
                        <>
                            <span className="w-3.5 h-3.5 rounded-full border-2 border-gray-600 border-t-emerald-400 animate-spin" />
                            Analyzing…
                        </>
                    ) : 'Run Prediction'}
                </button>
            </div>
        </div>
    )
}