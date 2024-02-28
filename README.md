![Logo](./misc/logo.png)
# How to install?
Required version of Python: 3.10+ 

Installing this tool is pretty easy, beacause it depends only on two main packages: NumPy and OpenCV. So you can at first run:
```
python -m pip install -r requirements.txt
```

# Interface
## CLI
```
usage: main.py [-h] [--root ROOT] [--output OUTPUT] [--format FORMAT] [--ttsplit TTSPLIT] [-vw VIEWPORT_WIDTH] [-vh VIEWPORT_HEIGHT] [--image-width IMAGE_WIDTH] [--image-height IMAGE_HEIGHT]

options:
  -h, --help            show this help message and exit
  --root ROOT           Path to the folder with input images.
  --output OUTPUT       Path to the folder where dataset will be stored.
  --format FORMAT       Choose between 'standard' and 'tficon' format of COCO dataset.
  --ttsplit TTSPLIT     Value between 0.0 and 1.0 that sets the size of the train part.
  -vw VIEWPORT_WIDTH, --viewport-width VIEWPORT_WIDTH
                        Width of the viewport window.
  -vh VIEWPORT_HEIGHT, --viewport-height VIEWPORT_HEIGHT
                        Height of the viewport window.
  --image-width IMAGE_WIDTH
                        Width of the image to save. If None than the width will not change.
  --image-height IMAGE_HEIGHT
                        Height of the image to save. If None than the height will not change.
```

The example usage of the tool is:
```
python main.py --root example/inputs --output output
```

You should get the same output as in the example/output folder.

## Keyboard
- For saving current state of the labelling press 's'. 
- Moving to the next image 'n'.
- Back to the previous image 'p'.