"""Check local links, images and fragment targets without network requests."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit
import sys

root = Path(__file__).resolve().parent.parent

class SiteParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids = set()
        self.links = []
        self.errors = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if 'id' in attrs:
            self.ids.add(attrs['id'])
        for name in ('src', 'href'):
            if attrs.get(name):
                self.links.append(attrs[name])
        if tag == 'img' and not attrs.get('alt', '').strip():
            self.errors.append('Image is missing descriptive alt text')

parser = SiteParser()
parser.feed((root / 'index.html').read_text(encoding='utf-8'))
for link in parser.links:
    url = urlsplit(link)
    if url.scheme or url.netloc:
        continue
    path = unquote(url.path)
    if path and not (root / path).is_file():
        parser.errors.append(f'Missing local file: {path}')
    if (not path or path == 'index.html') and url.fragment and unquote(url.fragment) not in parser.ids:
        parser.errors.append(f'Missing anchor: {url.fragment}')
if parser.errors:
    print('\n'.join(parser.errors), file=sys.stderr)
    sys.exit(1)
print(f'Checked {len(parser.links)} links and {len(parser.ids)} anchors; images have alt text')
