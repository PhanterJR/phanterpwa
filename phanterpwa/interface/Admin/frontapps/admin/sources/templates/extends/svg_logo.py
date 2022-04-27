from phanterpwa.helpers import (
    XML
)
import os
with open(os.path.join(os.path.dirname(__file__), "logo.svg"), 'r') as f:
    html = XML(f.read())
