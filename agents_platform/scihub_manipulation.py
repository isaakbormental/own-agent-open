from scihub import SciHub

sh = SciHub()

# fetch specific article (don't download to disk)
# this will return a dictionary in the form
# {'pdf': PDF_DATA,
#  'url': SOURCE_URL,
#  'name': UNIQUE_GENERATED NAME
# }
#result = sh.fetch('http://ieeexplore.ieee.org/xpl/login.jsp?tp=&arnumber=1648853')

# result = sh.download('http://ieeexplore.ieee.org/xpl/login.jsp?tp=&arnumber=1648853', path='paper.pdf')
import urllib.request
HEADERS = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:27.0) Gecko/20100101 Firefox/27.0'}
query = "Fuzzy Logic Controller Mobile Robotics"

# req = urllib.request.Request('https://scholar.google.com/scholar', headers=HEADERS, data=query)
# response = urllib.request.urlopen(req)
# the_page = response.read()
# print(response)


papers = sh.search("Fuzzy Logic Controller Mobile Robotics")
print(papers)
# i = 0
# while(True):
#     try:
#         papers = sh.search("Fuzzy Logic Controller Mobile Robotics")
#         break
#     except Exception:
#         i += 1
#         print('Try {0}'.format(i))
#         continue
