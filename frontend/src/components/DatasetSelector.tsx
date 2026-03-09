import type { Datasets } from '../types.ts'

interface Props {
    datasets: Datasets
    selected: string
    onSelect: (name: string) => void
}

export default function DatasetSelector({ datasets, selected, onSelect }: Props) {
    return (
        <select value={selected} onChange={e => onSelect(e.target.value)}>
            <option value="">Select a dataset</option>
            {Object.keys(datasets).map(name => (
                <option key={name} value={name}>{name}</option>
            ))}
        </select>
    )
}