# UI Segmentation and Element Detection
## A sample segmentation output
```json
{
    "segments": [
        {
            "id": 0,
            "class": "Component",
            "subclass": null,
            "height": 29,
            "width": 51,
            "position": {
                "column_min": 88,
                "row_min": 86,
                "column_max": 139,
                "row_max": 115
            }
        },
        {
            "id": 1,
            "class": "Block",
            "subclass": null,
            "height": 189,
            "width": 300,
            "position": {
                "column_min": 116,
                "row_min": 206,
                "column_max": 416,
                "row_max": 395
            },
            "children": [
                2,
                4
            ]
        },
        {
            "id": 2,
            "class": "Component",
            "subclass": null,
            "height": 22,
            "width": 205,
            "position": {
                "column_min": 158,
                "row_min": 240,
                "column_max": 363,
                "row_max": 262
            },
            "parent": 1
        },
        {
            "id": 3,
            "class": "Text",
            "subclass": null,
            "height": 35,
            "width": 44,
            "position": {
                "column_min": 319,
                "row_min": 72,
                "column_max": 363,
                "row_max": 107
            },
            "text_content": "Ui"
        },
        {
            "id": 4,
            "class": "Text",
            "subclass": null,
            "height": 14,
            "width": 171,
            "position": {
                "column_min": 160,
                "row_min": 214,
                "column_max": 331,
                "row_max": 228
            },
            "text_content": "AIM - Aalto Interface Metrics service",
            "parent": 1
        }
    ],
    "img_shape": [
        800,
        1280,
        3
    ],
    "img_b64": "iV...I="
}
```