interface Props {
    prediction: number | null
    task: string | null
    target_desc: string | null
}

export default function PredictionResult({ prediction, task, target_desc }: Props) {
    if (prediction === null) return null

    if (task?.toLowerCase() === "classification") {
        return (
            <div>
                {/* can be multiclass classification, create algo to take into account the entire string and extract correct terms depending on val */}
                <h2>Result: {prediction === 1 ? 'At Risk' : 'Healthy'}</h2>
            </div>
        )

    } else if (task?.toLowerCase() === 'regression') {
        return <div>
            {prediction}
        </div>

    } else {
        return <p>task not given. invalid input.</p>;
    }
}   