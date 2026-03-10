interface Props {
    prediction: number | null
    task: string | null
    target_desc: string | null
}

export default function PredictionResult({ prediction, task, target_desc }: Props) {
    if (prediction === null) return null

    return (
        <div>
            <h2>Result: {prediction === 1 ? 'At Risk' : 'Healthy'}</h2>
        </div>
    )
}   