import re

# Raw Strings (support)
ROMAN = r'(M{1,4}(CM|CD|D?C{0,3})(XC|XL|L?X{0,3})(IX|IV|V?I{0,3})'\
		+ r'|M{0,4}(CM|C?D|D?C{1,3})(XC|XL|L?X{0,3})(IX|IV|V?I{0,3})'\
		+ r'|M{0,4}(CM|CD|D?C{0,3})(XC|X?L|L?X{1,3})(IX|IV|V?I{0,3})'\
		+ r'|M{0,4}(CM|CD|D?C{0,3})(XC|XL|L?X{0,3})(IX|I?V|V?I{1,3}))'

CENT_ROMAN = r'(((s|S)iglo(s)?)|(s.))\s(({0}\,\s)*{0}\sy\s)?{0}'.format(ROMAN)

# Regex
R_ROMAN = re.compile(ROMAN)
R_CENT_ROMAN = re.compile(CENT_ROMAN)
NUM_REG = re.compile(r'\#?([0-9]+(\,|\.|\s|\:))*[0-9]+')
TAG_REG = re.compile(r'\<.*?\>')
PARENTHESIS_REG = re.compile(r'\(.*?\)')

# Spacy Model
ES_MODEL = 'es_core_news_md'
ENTS = ('PER', 'LOC', 'ORG', 'MISC')
# PER
# Named person or family.
# LOC
# Name of politically or geographically defined location 
# ORG
# Named corporate, governmental, or other organizational entity.
# MISC
# Miscellaneous entities, e.g. events, nationalities, products or works of art.
# Tokens


NUM_TOKEN = 'NUM'
TOKENS = ENTS + (NUM_TOKEN, )
TOKEN_THROW_RATIO = 0.5

# Debug
LOG_FORMAT = '%(levelname)s (%(asctime)-15s) for %(funcName)s: %(message)s'

# Folders
MINED_FOLDER = 'mined/'
CLEANED_FOLDER = 'cleaned/'