export interface FeatureDesc {
    description: string
    type: string
}

export interface DatasetInfo {
    features: string[]
    task: string
    target_desc: string
    target_map: { [key: number]: string }
    features_desc: {
        [key: string]: FeatureDesc
    }
}

export interface Datasets {
    [key: string]: DatasetInfo
}