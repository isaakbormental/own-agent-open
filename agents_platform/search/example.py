from client import ElsevierClient
import json

client = ElsevierClient('edaaeecff0179818ef310aa99081ed65')
results = client.search_science_direct("Fuzzy Logic control")
print(results)
print(type(results))

print(results['search-results'].keys())

print(results['search-results']['entry'])

print(type(results['search-results']['entry']))
print(results['search-results']['entry'][0])
print(results['search-results']['entry'][0].keys())


# print('-----------------')
# for key in results['search-results']['entry'][0].keys():
#     print(results['search-results']['entry'][0][key])

for entry in results['search-results']['entry']:
    print(entry['dc:title'] + " " + entry['dc:identifier'])