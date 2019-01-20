# ML

## Instructions

### Set Up environment

This can change if GPU needed.

````
docker pull tensorflow/tensorflow:latest-py3
````

### Run for Development

````
docker run -it -v .../generatext:/usr/src tensorflow/tensorflow:latest-py3 bash
````

### Steps

Inside ml folder

````
cd usr/src/text
````

#### 1. Train model

````
python train.py
````

## TODO:

- Refactor train, folder organization
- Reduce algorithm complexity (utils.py, TextSequence in magic.py)