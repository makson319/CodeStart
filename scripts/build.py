"""Publish only site files, excluding development tools and reports."""
from pathlib import Path
import shutil

root = Path(__file__).resolve().parent.parent
output = root / '_site'
if output.exists():
    shutil.rmtree(output)
output.mkdir()
for filename in ('index.html', 'style.css'):
    shutil.copy2(root / filename, output / filename)
shutil.copytree(root / 'assets', output / 'assets')
(output / '.nojekyll').touch()
print('Built _site: HTML, CSS and assets')
