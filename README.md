# image-resize
A small python script to batch-resize a directory of input images

# Usage
image-resize will batch-resize images in a directory. To run all that is needed is to specify a directory. Currently the code will create a directory automatically to save the completed images in.

Run
```
image-resize path-to-folder
```

# Options
Here are the various options

`-f comma-separated list of output formats [-f=jpeg,png,webp]`

# Installation
To install run the commands

```
sudo wget https://raw.githubusercontent.com/natecraddock/image-resize/master/image-resize.py -O /usr/local/bin/image-resize
sudo chmod a+rx /usr/local/bin/image-resize
```
