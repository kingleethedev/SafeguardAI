# AI Model Configuration

YOLO_CONFIG = {
    'MODEL_PATH': 'yolov8n.pt',
    'CONFIDENCE_THRESHOLD': 0.25,
    'IOU_THRESHOLD': 0.45,
    'CLASS_NAMES': [
        'person', 'bicycle', 'car', 'motorcycle', 'airplane', 'bus', 'train', 'truck',
        'boat', 'traffic light', 'fire hydrant', 'stop sign', 'parking meter', 'bench',
        'bird', 'cat', 'dog', 'horse', 'sheep', 'cow', 'elephant', 'bear', 'zebra',
        'giraffe', 'backpack', 'umbrella', 'handbag', 'tie', 'suitcase', 'frisbee',
        'skis', 'snowboard', 'sports ball', 'kite', 'baseball bat', 'baseball glove',
        'skateboard', 'surfboard', 'tennis racket', 'bottle', 'wine glass', 'cup',
        'fork', 'knife', 'spoon', 'bowl', 'banana', 'apple', 'sandwich', 'orange',
        'broccoli', 'carrot', 'hot dog', 'pizza', 'donut', 'cake', 'chair', 'couch',
        'potted plant', 'bed', 'dining table', 'toilet', 'tv', 'laptop', 'mouse',
        'remote', 'keyboard', 'cell phone', 'microwave', 'oven', 'toaster', 'sink',
        'refrigerator', 'book', 'clock', 'vase', 'scissors', 'teddy bear', 'hair drier',
        'toothbrush'
    ]
}

NLP_MODELS = {
    'SENTIMENT': {
        'model_name': 'cardiffnlp/twitter-roberta-base-sentiment-latest',
        'labels': ['negative', 'neutral', 'positive'],
        'max_length': 512
    },
    'THREAT_CLASSIFICATION': {
        'model_name': 'cardiffnlp/twitter-roberta-base-offensive',
        'labels': ['not-offensive', 'offensive'],
        'max_length': 512
    }
}

# Feature Extraction Settings
FEATURE_EXTRACTION = {
    'TEXT_EMBEDDING_DIM': 768,
    'IMAGE_EMBEDDING_DIM': 512,
    'USE_PCA': True,
    'PCA_COMPONENTS': 50
}

# Training Configuration (if retraining models)
TRAINING_CONFIG = {
    'BATCH_SIZE': 32,
    'LEARNING_RATE': 1e-5,
    'EPOCHS': 10,
    'VALIDATION_SPLIT': 0.2,
    'EARLY_STOPPING_PATIENCE': 3
}