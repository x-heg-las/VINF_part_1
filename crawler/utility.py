import constants as c
import re

def parse_links(content):
    # find all links inside content
    accepted_anchors = []

    anchors = re.findall(c.REGEXES['anchors'], str(content))

    for anchor in anchors:
        if re.search(c.REGEXES['exceptions'], anchor):
            # ignore exceptions
            continue
        else:
            # repo link
            if build_url(anchor) is not None:
                accepted_anchors.append(build_url(anchor))
    
    return accepted_anchors

# Checks if the document is public repository, according to specified identifiers.
def is_public_repo(content):
    return re.search(c.REPOSITORY_IDENTIFIER, str(content)) and re.search(c.REPOSITORY_IDENTIFIER_2, str(content)) 


def build_url(anchor):
    url = re.search(c.REGEXES['href'], anchor)
    git_url =  re.search(c.REGEXES['github'], anchor)
    if url or git_url:
        url = url.group(1)
    else:
        return None

    return f'{c.DOMAIN}{url}'