# TEXT

## Instructions

### Set Up environment

````
cd generatext/text
docker build -t generatext .
````

### Run for Development

````
docker run -it -v .../generatext:/usr/src generatext bash
````

### Steps

Inside text folder

````
cd usr/src/text
````

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

#### 4. Generate Counter object for words (collections)

````
python counter.py
````

## TODO:

- Refactor mine.py
- Add restarted to clean.py (check if cleaned files already exist)
- Reduce algorithm complexity (counter.py)