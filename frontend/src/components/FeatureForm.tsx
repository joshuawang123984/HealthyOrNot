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

    const handleChange = (feature: string, value: string) => {
        setValues(prev => ({ ...prev, [feature]: value }))
    }

    const handleSubmit = () => {
        const featureValues = features.map(f => parseFloat(values[f] || '0'))

        fetch('http://localhost:5001/predict', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ dataset, features: featureValues })
        })
            .then(res => res.json())
            .then(data => onSubmit(data.prediction))
    }

    return (
        <div>
            {features.map(feature => (
                <div key={feature}>
                    <label title={featuresDesc?.[feature]?.type ?? ''}>{feature} -- {featuresDesc?.[feature]?.description ?? feature}</label>
                    <input
                        type="number"
                        value={values[feature] || ''}
                        onChange={e => handleChange(feature, e.target.value)}
                    />
                </div>
            ))}
            <button onClick={handleSubmit}>Predict</button>
        </div>
    )
}