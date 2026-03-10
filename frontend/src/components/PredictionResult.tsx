interface Props {
    prediction: number | null
}

export default function PredictionResult({ prediction }: Props) {
    if (prediction === null) return null

    return (
        <div>
            <h2>Result: {prediction === 1 ? 'At Risk' : 'Healthy'}</h2>
        </div>
    )
}