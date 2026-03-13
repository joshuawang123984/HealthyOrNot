import { useState, useEffect } from 'react'
import type { Datasets } from './types'
import DatasetSelector from './components/DatasetSelector'
import FeatureForm from './components/FeatureForm'
import PredictionResult from './components/PredictionResult'

function App() {
  const [datasets, setDatasets] = useState<Datasets>({})
  const [selectedDataset, setSelectedDataset] = useState<string>('')
  const [prediction, setPrediction] = useState<number | null>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetch('http://localhost:5001/datasets')
      .then(res => res.json())
      .then(data => { setDatasets(data); setLoading(false) })
      .catch(() => setLoading(false))
  }, [])

  const dataset = selectedDataset ? datasets[selectedDataset] : null

  return (
    <div className="min-h-screen bg-gray-950 text-gray-100 flex flex-col">

      {/* head */}
      <header className="sticky top-0 z-50 border-b border-gray-800 bg-gray-950/90 backdrop-blur px-6 h-14 flex items-center justify-between">
        <div className="flex items-center gap-2 font-bold text-lg tracking-tight">
          <span className="w-2 h-2 rounded-full bg-emerald-400 shadow-[0_0_8px_#34d399] animate-pulse" />
          HealthyOrNot
        </div>
        <span className="text-xs text-gray-500 border border-gray-800 rounded px-2 py-1 tracking-widest uppercase">
          ML Diagnostic v1.0
        </span>
      </header>

      {/* body */}
      <div className="flex flex-1 overflow-hidden">

        {/* side */}
        <aside className="w-72 border-r border-gray-800 p-5 flex flex-col gap-6 overflow-y-auto">
          <div>
            <p className="text-xs uppercase tracking-widest text-gray-500 mb-3">Select Dataset</p>
            {loading ? (
              <div>
                <p className="text-xs text-gray-500 mb-2">Loading models…</p>
                <div className="h-0.5 bg-gray-800 rounded overflow-hidden">
                  <div className="h-full w-2/5 bg-emerald-400 rounded animate-pulse" />
                </div>
              </div>
            ) : (
              <DatasetSelector
                datasets={datasets}
                selected={selectedDataset}
                onSelect={(ds) => { setSelectedDataset(ds); setPrediction(null) }}
              />
            )}
          </div>

          {dataset && (
            <div className="border-t border-gray-800 pt-5">
              <p className="text-xs uppercase tracking-widest text-gray-500 mb-2">About</p>
              <p className="text-xs text-gray-500 leading-relaxed">
                {dataset.task === 'classification' ? 'Classification' : 'Regression'} model
                · {dataset.features?.length ?? 0} features
              </p>
            </div>
          )}
        </aside>

        {/* main content */}
        <main className="flex-1 overflow-y-auto p-6 flex flex-col gap-4">
          {!selectedDataset ? (
            <div className="flex-1 flex flex-col items-center justify-center text-gray-600 gap-3 text-center h-full">
              <span className="text-5xl opacity-30">⬡</span>
              <p className="text-sm max-w-xs leading-relaxed">
                Select a dataset from the sidebar to begin your diagnostic analysis.
              </p>
            </div>
          ) : (
            <>
              {prediction !== null && (
                <PredictionResult
                  prediction={prediction}
                  task={dataset?.task ?? null}
                  target_desc={dataset?.target_desc ?? null}
                  target_map={dataset?.target_map ?? {}}
                />
              )}

              <div className="bg-gray-900 border border-gray-800 rounded-lg p-5">
                <p className="text-xs uppercase tracking-widest text-gray-500 mb-4 flex items-center gap-2">
                  <span className="inline-block w-0.5 h-3 bg-emerald-400 rounded" />
                  Input Biomarkers
                </p>
                <FeatureForm
                  features={dataset?.features ?? []}
                  featuresDesc={dataset?.features_desc ?? {}}
                  onSubmit={setPrediction}
                  dataset={selectedDataset}
                />
              </div>
            </>
          )}
        </main>
      </div>
    </div>
  )
}

export default App