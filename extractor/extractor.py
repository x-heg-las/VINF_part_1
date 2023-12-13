## This program represents entity extractor from github repository HTML
## To run this script you need to provide data file with repository HTMLs.
## Sample file (raw-data.csv) is provided. Run with: python3 extractor.py.
##
## Author: Patrik Heglas

import argparse
import csv
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET
import re

def extract_entities(data):
    entities = []
    index = 0
    # Arrray of column titles used in csv
    
    for line in data:
        index += 1
        print(f'{index} of {len(data)}')

        # Parse entities from HTML
        soup = BeautifulSoup(line, 'html.parser')
        if soup.find(id='readme'): readme = soup.find(id='readme').get_text()
        if soup.select_one('#repository-container-header strong'): repo_name = soup.select_one('#repository-container-header strong').text.strip()
        if soup.select_one('#repository-container-header [rel="author"]'): username = soup.select_one('#repository-container-header [rel="author"]').text.strip()
        if soup.select_one('.Box-header .Details a[href*="commits"]:not(.commit-author) strong'): commit_count = soup.select_one('.Box-header .Details a[href*="commits"]:not(.commit-author) strong').text.strip()
        languages = []
        
        for l in soup.select('.Layout-sidebar .BorderGrid-cell a[href*="search?l="]'):
            languages.append(l.text.strip())

        if soup.select_one('.Layout-sidebar .BorderGrid:first-child .BorderGrid-row:first-child .BorderGrid-cell:first-child p.f4'): about = soup.select_one('.Layout-sidebar .BorderGrid:first-child .BorderGrid-row:first-child .BorderGrid-cell:first-child p.f4').text.strip()
        if soup.find(id='repo-stars-counter-star') :star_count = soup.find(id='repo-stars-counter-star').get_text()
        watch_count = None
        if soup.select_one('#repo-notifications-counter'): watch_count = soup.select_one('#repo-notifications-counter').text.strip()
        tags = []

        for t in soup.select('.Layout-sidebar .BorderGrid:first-child .BorderGrid-row:first-child .BorderGrid-cell:first-child [data-octo-click="topic_click"]'):
            tags.append(t.text.strip())

        record = [username or '', repo_name or '', readme or '', commit_count or '', '\t'.join(languages), '\t'.join(tags), about or '', star_count or '0', watch_count or '0' ]
        entities.append(record)

    return entities

def save_to_csv(entities):
    # Build csv - this was used prior xml and is not longer used
    entities.insert(0, ['Username', 'Repository name', 'Readme', 'Commit count', 'Languages', 'Tags', 'About', 'Star count', 'Watch count'])

    with open('./entities.csv', 'w') as of:
        writer = csv.writer(of)
        writer.writerows(entities)

def save_to_xml(entities):
    # Build XML
    root = ET.Element('root')

    languages_set = set()
    
    for item in entities:
        repository = ET.SubElement(root, 'repository')

        username = ET.SubElement(repository, 'username')
        username.text = item[0]

        repo_name = ET.SubElement(repository, 'reponame')
        repo_name.text = item[1]

        readme = ET.SubElement(repository, 'readme')
        readme.text = item[2]

        commit_count = ET.SubElement(repository, 'commitcount')
        commit_count.text = item[3]

        languages = ET.SubElement(repository, 'languages')
        languages.text = item[4]

        # process languages
        languages_split = item[4].split('\t')

        for language in languages_split:
            token = language.split(' ')[0]
            languages_set.add(token)
        
        # end languages processing

        tags = ET.SubElement(repository, 'tags')
        tags.text = item[5]

        about = ET.SubElement(repository, 'about')
        about.text = item[6]

        star_count = ET.SubElement(repository, 'starcount')
        star_count.text = item[7]

        watch_count = ET.SubElement(repository, 'watchcount')
        watch_count.text = item[8]


    # Create tokens key with languages as value. This is used to join wiki data with repository data based on used programming languages.   
    tokens = ET.SubElement(repository, 'tokens')
    tokens.text = ', '.join(map(str, languages_set))

    tree = ET.ElementTree(root)

    tree.write('entities.xml', encoding='utf-8', xml_declaration=True)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--data', help='Raw data file to extract entities from', default='raw-data.csv')
    
    args = parser.parse_args()
    data_file = args.data

    with open(data_file, 'r') as file:
        entities = extract_entities(file.readlines())

        save_to_xml(entities)

if __name__ == '__main__':
    main()