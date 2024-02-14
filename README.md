# How to install?
Required version of Python: 3.10+ 

Installing this tool is pretty easy, beacause it depends only on two main packages: NumPy and OpenCV. So you can at first run:
```
python -m pip install -r requirements.txt
```

# Interface
```
usage: main.py [-h] [--root ROOT] [--output OUTPUT] [--format FORMAT]

optional arguments:
  -h, --help       show this help message and exit
  --root ROOT      Path to the folder with input images.
  --output OUTPUT  Path to the folder where dataset will be stored.
  --format FORMAT  Choose between 'standard' and 'tficon' format of COCO dataset.
```

The example usage of the tool is:
```
python main.py --root example/inputs --output output
```

You should get the same output as in the example/output folder.