# Main focus is on REGEXES.exceptions by which we are filtering URLs to avoid during crawl.
# URLs not matching this regex are further processed by crawler and recorded if it contains public repository.

REGEXES = {
    'topics': r'<a\s+[^>]*href="/topics/[^"]*"',
    'collections': r'<a\s+[^>]*href="/collections/[^"]*"',
    'anchors': r'<a\s+[^>]*href="/[^"]*"',
    'exceptions': r'<a\s+[^>]*href="(/|https://www\.github\.com/|https://github\.com/)(login|signup|pricing|marketplace|features|.*/commits/*?author|.*commits?author=*|.*/pull/*|.*\.zip|.*/commit/*|.*/tree/*?|.*/branches|.*/refs/*?|.*/issues/*?|.*/blob/*?|join*?|.*search\?*?|.*/actions/*?|trending*|.*/compare/*?|customer-stories/*?|.*/releases/*?)[^"]*"',
    'href': r'<a[^>]*href=["\'](.*?)["\']',
    'github': r'https?://(?:www\.)?github\.com/.*'
}

DOMAIN = 'https://www.github.com'
REPOSITORY_IDENTIFIER=r'<a[^>]*?id="code-tab"[^>]*?class="[^"]*selected"[^>]*?>'
REPOSITORY_IDENTIFIER_2=r'<div+[^>]*?\s+id="readme"\s*'
MAX_REPOS = 1000000
