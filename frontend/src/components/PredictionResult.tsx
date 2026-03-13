interface Props {
    prediction: number | null
    task: string | null
    target_desc: string | null
    target_map: { [key: number]: string }
}

export default function PredictionResult({ prediction, task, target_desc, target_map }: Props) {
    if (prediction === null) return null

    if (task?.toLowerCase() === 'classification') {
        const label = target_map[Math.round(prediction)]
        const isHealthy = label?.toLowerCase().includes('healthy') ||
            label?.toLowerCase().includes('negative') ||
            label?.toLowerCase().includes('no') ||
            label?.toLowerCase().includes('benign') ||
            prediction === 0

        return (
            <div className={`rounded-lg border p-5 flex items-start gap-4 animate-[fadeIn_0.3s_ease]
                ${isHealthy
                    ? 'bg-emerald-950/30 border-emerald-800/50'
                    : 'bg-red-950/30 border-red-800/50'}`}>

                {/* output results indicator */}
                <div className={`mt-0.5 w-3 h-3 rounded-full shrink-0 ${isHealthy
                    ? 'bg-emerald-400 shadow-[0_0_10px_#34d399]'
                    : 'bg-red-400 shadow-[0_0_10px_#f87171]'}`}
                />

                <div className="flex flex-col gap-1">
                    <p className="text-xs uppercase tracking-widest text-gray-500">Result</p>
                    <p className={`text-xl font-bold tracking-tight ${isHealthy ? 'text-emerald-400' : 'text-red-400'}`}>
                        {label ?? `Class ${Math.round(prediction)}`}
                    </p>
                    {target_desc && (
                        <p className="text-xs text-gray-500 mt-1">{target_desc}</p>
                    )}
                </div>
            </div>
        )

    } else if (task?.toLowerCase() === 'regression') {
        return (
            <div className="rounded-lg border border-gray-800 bg-gray-900 p-5 flex items-start gap-4 animate-[fadeIn_0.3s_ease]">
                <div className="mt-0.5 w-3 h-3 rounded-full shrink-0 bg-blue-400 shadow-[0_0_10px_#60a5fa]" />
                <div className="flex flex-col gap-1">
                    <p className="text-xs uppercase tracking-widest text-gray-500">Predicted Value</p>
                    <p className="text-xl font-bold tracking-tight text-blue-400">
                        {prediction.toFixed(3)}
                    </p>
                    {target_desc && (
                        <p className="text-xs text-gray-500 mt-1">{target_desc}</p>
                    )}
                </div>
            </div>
        )

    } else {
        return (
            <div className="rounded-lg border border-yellow-800/50 bg-yellow-950/20 p-4">
                <p className="text-xs text-yellow-500">Invalid task type — expected classification or regression.</p>
            </div>
        )
    }
}