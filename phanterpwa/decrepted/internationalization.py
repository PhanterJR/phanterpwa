import os
from phanterpwa.i18n import Translator
from .config import CONFIG

debug = CONFIG['PROJECT']['debug']
print(os.path.join(os.path.dirname(__file__), "..", "app", "languages"))
Translator_app = Translator(os.path.join(os.path.dirname(__file__), "..", "app", "languages"), debug=debug)
Translator_app.add_language("pt-BR")
Translator_api = Translator(os.path.join(os.path.dirname(__file__), "..", "api", "languages"), debug=debug)
Translator_api.add_language("pt-BR")
