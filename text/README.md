# TEXT

## Instructions

### Set Up environment

````
cd generatext/text
docker build -t generatext .
````

### Run for Development

````
docker run -it -v "%CD%":/usr/src generatext bash
````

### Steps

#### 1. Download Wikipedia data with WikiExtractor

````
git clone https://github.com/attardi/wikiextractor.git
cd wikiextractor
# python setup.py install
# eswiki, enwiki, itwiki, etc 
wget http://download.wikimedia.org/eswiki/latest/eswiki-latest-pages-articles.xml.bz2
python WikiExtractor.py -cb 250K -o extracted eswiki-latest-pages-articles.xml.bz2
````

#### 2. Mine sentences from extracted Data

````
python mine.py
````

#### 3. Clean sentences from mined Data

````
python clean.py
````