from bs4 import BeautifulSoup

soup = BeautifulSoup(open('/Users/baileyspell/Downloads/images.html'), 'html.parser')

table_tags = soup.find_all('table')

img_srcs = []
for table in table_tags:
    img_tags = table.find_all('img')
    img_srcs.extend([img['src'] for img in img_tags if 'src' in img.attrs])

print(img_srcs)
print(len(img_srcs))