interface Props {
    prediction: number | null
    task: string | null
    target_desc: string | null
    target_map: { [key: number]: string }
}

export default function PredictionResult({ prediction, task, target_desc, target_map }: Props) {
    if (prediction === null) return null

    if (task?.toLowerCase() === "classification") {
        return (
            <div>
                <h2>{target_desc}</h2>
                <h2>{target_map[Math.round(prediction)]}</h2>

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