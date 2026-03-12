import { useState, useEffect } from 'react'
import type { Datasets } from './types'
import DatasetSelector from './components/DatasetSelector'
import FeatureForm from './components/FeatureForm'
import PredictionResult from './components/PredictionResult'

function App() {
  const [datasets, setDatasets] = useState<Datasets>({})
  const [selectedDataset, setSelectedDataset] = useState<string>('')
  const [prediction, setPrediction] = useState<number | null>(null)

  useEffect(() => {
    fetch('http://localhost:5001/datasets')
      .then(res => res.json())
      .then(data => setDatasets(data))

  }, [])

  return (
    <div>
      <h1>HealthyOrNot</h1>
      <DatasetSelector datasets={datasets} selected={selectedDataset} onSelect={setSelectedDataset} />
      <FeatureForm features={selectedDataset ? datasets[selectedDataset].features : []} featuresDesc={selectedDataset ? datasets[selectedDataset].features_desc : {}} onSubmit={setPrediction} dataset={selectedDataset} />
      <PredictionResult prediction={prediction} task={selectedDataset ? datasets[selectedDataset].task : null} target_desc={selectedDataset ? datasets[selectedDataset].target_desc : null} target_map={selectedDataset ? datasets[selectedDataset].target_map : {}} />
    </div>
  )
}

export default App