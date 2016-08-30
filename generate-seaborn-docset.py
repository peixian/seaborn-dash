from bs4 import BeautifulSoup as BS
from subprocess import call
import sqlite3

#call(['bash', 'helper.sh'])


with open('Seaborn.docset/Contents/Resources/Documents/examples/index.html', 'r') as infile:
    examples = BS(infile, 'lxml').find('div', {'id': 'example-gallery'}).find_all('a')[1:]
    gallaries = [] #list of examples, in the format of (name, link)
    dash_str_format = 'examples/{0}'
    for example in examples:
        link = dash_str_format.format(example['href'][2:])
        title = ''
        with open('Seaborn.docset/Contents/Resources/Documents/{}'.format(link), 'r') as gallary_file:
            title = BS(gallary_file, 'lxml').find('h1').text.replace(u'\u2019', '\'').replace(u'\xb6', '') #dirty hack to get around unicode errors
        name = '{} - {}'.format(example.span.p.text, title)
        gallaries.append((name, link))

with open('Seaborn.docset/Contents/Resources/Documents/tutorial.html', 'r') as infile:
    tutorials = BS(infile, 'lxml').find('div', {'class': 'row'}).find_all('a', {'class': 'reference internal'})
    guides = [] #list of guides
    for tutorial in tutorials:
        link = tutorial['href']
        name = tutorial.text
        guides.append((name, link))

conn = sqlite3.connect('./Seaborn.docset/Contents/Resources/docSet.dsidx')
c = conn.cursor()

for item in gallaries:
    c.execute('INSERT OR IGNORE INTO searchIndex(name, type, path) VALUES (?, ?, ?)', (item[0], 'Sample', item[1]))

for item in guides:
    c.execute('INSERT OR IGNORE INTO searchIndex(name, type, path) VALUES (?, ?, ?)', (item[0], 'Guide', item[1]))

conn.commit()
conn.close()
