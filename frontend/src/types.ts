export interface DatasetInfo {
    features: string[]
    task: string
    target_desc: string
    features_desc: {
        [key: string]: string
    }
}

export interface Datasets {
    [key: string]: DatasetInfo
}