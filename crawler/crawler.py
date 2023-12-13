## This program represent crawler for public github repositories
## To run this script you need to install requirements and file with starting urls to crawl (--link-file attribute)
## Sample file is provided (links.txt). Run this with: python3 crawler.py
##
## Author: Patrik Heglas


import argparse
import re
import time
import requests
import constants as c
import utility as u
import os

paths = []
public_repos = 0
to_crawl = []
visited_links = []
oputput_file = ''

def crawl(url, crawl_file_name):

    print(f'Processing path: {url}')

    response = requests.get(url)
    print(f'response code: {response.status_code}')

    content_type = response.headers.get('content-type')

    if response.status_code == 200:
        # Skip binary files      
        if not content_type.lower().startswith('text/html'):
            return True # -> we still want to run crawler
    
        response_body = response.text
         
        # Check if the URL contains public repository
        if u.is_public_repo(response_body):
            print(f'*********************** found repo {url} *****************************')
            ++public_repos
            
            # Write public repository URL to the file
            with open("./assets/public_repos.txt", "a") as file:
                file.write(f"{url}\n")

            # Save HTML content of a repository to the file
            with open('./assets/output.csv', 'a') as file:
                response_body  = re.sub(r'\s', ' ', response_body)
                file.write(f"{response_body};\n")

            if public_repos >= c.MAX_REPOS:
                return False # -> stop crawler if we heave MAX_REPOS of repositories found

        with open(crawl_file_name, 'a') as f:
            # Do not add more links if we have over 30000 to crawl
            if len(to_crawl) - len(visited_links) < 30000:
                # Use regexes to find anchors (possibly new pages)
                for item in u.parse_links(response_body):
                    if item not in to_crawl and item not in visited_links:
                        to_crawl.append(item)
                        f.write(f'{item}\n')

        return True # -> continue crawl
    else:
        return True # -> placeholder for now, but continues run even if we receive url for invalid location (HTTP-404)


def load_links(file_path):
    url_list = []

    try:
        with open(file_path, 'r') as file:
            for line in file:
                url = line.strip()
                
                url_list.append(url)
        
        print(url_list)
    except FileNotFoundError:
        print(f"File not found: {file_path}")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

    return url_list


def main():
    parser = argparse.ArgumentParser(description='Crawler for public github repositories')

    # Path to file wiht links to crawl, separated with new line
    parser.add_argument('--link_file', help='File with links to crawl', default='./links.txt')

    parser.add_argument('--output', help='Output file path', default='./assets/output.csv')
    parser.add_argument('--wait', help='Time to wait between requests', default=1.2)
    parser.add_argument('--crawl', help='File with links to crawl', default='./assets/tocrawl.txt')
    parser.add_argument('--visited', help='File with visited links', default='./assets/visited.txt')

    args = parser.parse_args()
    
    link_file = args.link_file
    output_file = args.output
    wait_time = args.wait
    crawl_file_path = args.crawl
    visited_file_path = args.visited


    # Load links to crawl from file, if exists
    if crawl_file_path and os.path.exists(crawl_file_path):
        # load urls to crawl from file created if a crawl was interuppted by user
        with open(crawl_file_path, "r") as file:
            for line in file:
                to_crawl.append(line.strip())
    else:
        # basic root urls to start crawl from
        to_crawl.extend(load_links(link_file))

    # Load links to avoid from file, if exists
    if visited_file_path and os.path.exists(visited_file_path):
        with open(visited_file_path, "r") as file:
            for line in file:
                to_crawl.append(line.strip())

    while public_repos < c.MAX_REPOS and to_crawl:
        path = to_crawl.pop(0)

        if path in visited_links:
            continue

        with open(visited_file_path, 'a') as f:
            f.write(f'{path}\n')

        visited_links.append(path)
        status = crawl(path, crawl_file_path)

        if not status:
            break

        time.sleep(wait_time)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        # Save visited and enqueued URLs if the run in interupted.
        if to_crawl:
            with open('./assets/.to_crawl_bkp', 'w') as f:
                for line in to_crawl:
                    f.write(f'{line}\n')

        if visited_links:
            with open('./assets/.visited_links_bkp', 'w') as f:
                for line in to_crawl:
                    f.write(f'{line}\n')
    