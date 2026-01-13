"""
sprawdzić jakie jeszcze metody są potrzebne do pełnego image_data_preprocessing
na sam koniec zrobić klasę która wszystko połączy(class image_data_preprocessing)

project/
│
├── preprocessing/          ← WARSTWA DANYCH
│   ├── __init__.py
│   ├── io.py                ← ImageLoader, DataExporter
│   ├── conversion.py        ← ImageToMatrixConverter
│   ├── geometry.py          ← Resize, Padding, MatrixCreator
│   ├── normalization.py     ← Normalization
│   ├── grayscale.py         ← GrayScaleProcessing
│   ├── thresholding.py      ← Thresholding
│   ├── augmentation.py      ← DataAugmentation
│   ├── convolution.py       ← ConvolutionActions
│   ├── pooling.py           ← Pooling
│   ├── pipeline.py          ← ImageDataPreprocessing, TransformPipeline
│
├── features/                ← FEATURE ENGINEERING
│   ├── __init__.py
│   ├── edges.py             ← Sobel, Prewitt
│   ├── hog.py               ← HOG
│   └── extractor.py         ← FeatureExtraction
│
├── data/                    ← DATA MANAGEMENT
│   ├── __init__.py
│   ├── dataset.py           ← Dataset
│   ├── batch.py             ← BatchProcessing
│   ├── cache.py             ← CacheManager
│   ├── downloader.py        ← DataDownloader
│   ├── metadata.json        ← Data
│
├── nn/                      ← MODELE (PÓŹNIEJ)
│   ├── __init__.py
│   ├── tensor.py
│   ├── layers/
│   ├── model.py
│
├── training/                ← TRENING (PÓŹNIEJ)
│   ├── loss.py
│   ├── optimizer.py
│   └── trainer.py
│
└── main.py

features/                ← FEATURE ENGINEERING
├── __init__.py
├── edges.py             ← Sobel, Prewitt
├── hog.py               ← HOG
└── extractor.py         ← extract_edges i extract_features

__ImageLoader__
    open_image
__ImageToMatrixConverter__
    convert_image_to_matrix
    separate_channels
__MatrixProcessor__
    normalization
    resize
__GrayScaleProcessing__
    rgb_to_grayscale
    grayscale_to_rgb
__ConvolutionActions__
    convolution_2d
    apply_filter_to_channels_or_path
__MatrixCreator__
    create 
    pad
__DataAugmentation__
    augment
    horizontal_flip
    vertical_flip
    random_rotation
__Thresholding__
    apply_threshold
    adaptive_threshold
__Normalization__
    min_max_normalization
    z_score_normalization
__FeatureExtraction__
    extract_edges
    sobel
    prewitt
    hog
    extract_features
__DataExporter__
    save_as_image
    save_as_matrix
__ImageDataPreprocessing__
    preprocess
__BatchProcessing__
    create_batches
    process_batch
__Dataset__
    __len__
    __getitem__
__CacheManager__
    cache
    load
__TransformPipeline__
    apply


__FeatureExtraction__

"""