# GENERATEXT - Text Generated

## Instructions

### Environment

````
git clone https://github.com/claverru/generatext.git
cd generatext
docker build -t generatext .
````

### Download Wikipedia data with WikiExtractor
````
# apt-get install git
git clone https://github.com/attardi/wikiextractor.git
cd wikiextractor
python setup.py install
cd .. 
# apt-get install wget
# eswiki, enwiki, itwiki, etc 
wget http://download.wikimedia.org/eswiki/latest/eswiki-latest-pages-articles.xml.bz2
WikiExtractor.py -cb 250K -o extracted itwiki-latest-pages-articles.xml.bz2
````

### Development

````
docker run -it -v "%CD%":/usr/src generatext bash
````
