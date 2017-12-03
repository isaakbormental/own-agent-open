# -*- coding: utf-8 -*-
import requests
import os
from search.client import ElsevierClient
import time
from scihub import SciHub

url = "http://bme2.aut.ac.ir/mhmoradi/FUZZY%20COURSE/Reference%20Articles%20for%20Fuzzy%20Lecture/Fuzzy%20Logic%20in%20Control%20Systems%20Fuzzy-Part2.pdf"

def download_by_query(query, howmany):
    client = ElsevierClient('edaaeecff0179818ef310aa99081ed65')
    results = client.search_science_direct(query=query)
    for i in range(howmany):
        entry = results['search-results']['entry'][i]
        print(entry['dc:title'] + " " + entry['dc:identifier'])
        download_by_doi(entry['dc:identifier'].replace('DOI:', ''), os.path.join(os.path.dirname(os.path.abspath(__file__)), 'metadata'), '{0}.pdf'.format(entry['dc:title']))
        time.sleep(10)
    # for entry in results['search-results']['entry']:
    #     print(entry['dc:title'] + " " + entry['dc:identifier'])
    #     download_by_doi(entry['dc:identifier'].replace('DOI:',''), os.path.join(os.path.dirname(os.path.abspath(__file__)), 'metadata'), '{0}.pdf'.format(entry['dc:title']))


def download_by_doi(doi, destination, path):
    sh = SciHub()
    sh.download(identifier=doi, destination=destination, path=path)

def download_file(download_url, filename):
    response = requests.get(download_url)
    with open('metadata/{0}.pdf'.format(filename), 'wb') as f:
        f.write(response.content)


def load_pdfs():
    loaded_pdf_names = []
    loaded_pdfs = dict()
    pdfs_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'metadata')
    # print(goal_dir)
    # print(os.listdir(goal_dir))
    for filename in os.listdir(pdfs_dir):
        loaded_pdf_names.append(filename.replace('.pdf', ''))
        with open(os.path.join(pdfs_dir, filename), 'r') as file:
            loaded_pdfs[filename.replace('.pdf', '')] = file
    return loaded_pdf_names, loaded_pdfs

def delete_pdf(pdf, pdf_names, pdfs):
    pdf_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'metadata', pdf+'.pdf')
    new_pdf_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..\..\pdfs', pdf+'.pdf')
    print(pdf_path)
    print(new_pdf_path)
    os.rename(pdf_path, new_pdf_path)
    pdf_names.remove(pdf)
    del pdfs[pdf]
    return pdf_names, pdfs

def main():
    # download_file(url, 1)
    pdf_names, pdfs = load_pdfs()
    print(pdfs)
    print(pdf_names)

    # pdf_names, pdfs = delete_pdf('1', pdf_names, pdfs)

    print(pdfs)
    print(pdf_names)


    download_by_query("convolutional neural networks lung cancer", 11)



if __name__ == "__main__":
    main()