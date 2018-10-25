# GENERATEXT - Text Generated

## Instructions

git clone https://github.com/claverru/generatext.git

cd generatext

docker build -t generatext .

### For development

docker run -it -v "%CD%":/usr/src generatext bash
