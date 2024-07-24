# Component Counter - Python

This is a Python program for processing images in the `.pgm` format. It includes functions to load the image, label connected components, apply distance transform, thresholding, and normalization.

## Features

1. **Load Image (`.pgm`)**
2. **Connected Components Labeling**
3. **Distance Transform**
4. **Thresholding**
5. **Image Normalization**


## How to Run

-  Run the script by passing the path to the `.pgm` image as an argument:

```bash
python process_image.py path/to/image.pgm
```

The program will apply the transformations and display the number of components in the image.


## Notes

- The program assumes the input image is in `.pgm` (Portable GrayMap) format.
- The image must be specified in ASCII format (P2).
- The `threshold` function uses a limit for binarizing the image.
- The `distance` function applies the distance transform to calculate the distance of pixels to the background.
- The `normalize` function adjusts the gray levels after the distance transform.
- The `cc_label` function labels the connected components in the image.

## Requirements

- No external libraries, just bare Python 3.x