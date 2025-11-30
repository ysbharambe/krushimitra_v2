# Dataset Structure

Place your training data in the following structure:

```
user_collected/
├── images/
│   ├── train/
│   │   ├── image1.jpg
│   │   ├── image2.jpg
│   │   └── ...
│   └── val/
│       ├── image1.jpg
│       └── ...
└── labels/
    ├── train/
    │   ├── image1.txt
    │   ├── image2.txt
    │   └── ...
    └── val/
        ├── image1.txt
        └── ...
```

## Label Format (YOLO)
Each `.txt` file should contain bounding box annotations:
```
<class_id> <x_center> <y_center> <width> <height>
```

All values are normalized (0-1).
