from bs4 import BeautifulSoup as BS
from subprocess import call
import sqlite3

call(['bash', 'helper.sh'])
with open('Seaborn.docset/Contents/Resources/Documents/examples/index.html', 'r') as infile:
    examples = BS(infile, 'lxml').find('div', {'id': 'example-gallery'}).find_all('a')[1:]
    gallaries = [] #list of examples, in the format of (name, link)
    dash_str_format= 'examples/{0}'
    for example in examples:
        name = example.span.p.text
        link = dash_str_format.format(example['href'][2:])
        gallaries.append((name, link))

conn = sqlite3.connect('Seaborn.docset/Contentes/Resources/docSet.dsidx')
c = conn.cursor()

for item in gallaries:
    c.execute('INSERT OR IGNORE INTO searchIndex(name, type, path) VALUES (?, ?, ?)', (item[0], 'Sample', item[1]))

conn.commit()
conn.close()
