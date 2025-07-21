from .tableau import Tableau
from .dax import Dax
from .language import Language
from ..convert_registry import registry

def get_from_to_languages(fromLanguage, toLanguage) -> tuple[Language, Language]:
    """
    Method to return an appropriate language
    """
    language = LanguageFactory()
    return language._get_langugage(fromLanguage), language._get_langugage(toLanguage)

def get_translator(custom:bool, fromLanguage:str, toLanguage:str) -> dict:
    """
    Method to return an appropriate translator
    """
    translator = TranslateFactory()

    if not custom:
        return translator._get_standard(fromLanguage,toLanguage)
    else:
        customized = translator._get_custom(fromLanguage, toLanguage)
        standard = translator._get_standard(fromLanguage,toLanguage)
        standard.update(customized)
        return standard, *translator._get_expressions(fromLanguage, toLanguage)
    
class LanguageFactory:
    """
    Class LanguageFactory produces the correct class object of a language
    """
    _languages = {
        'tableau': Tableau,
        'dax': Dax
    }
    
    def _get_langugage(self, format) -> Language:
        """
        Return class object of Language
        """
        if format in self._languages.keys():
            return self._languages[format]()
        else:
            raise ValueError(format)

class TranslateFactory:
    """
    Class TranslateFactory produces the correct translation for a language
    """
    def _get_standard(self, fromLanguage, toLanguage):
        """
        Return standard translation of one language to another 
        """
        key = f'{fromLanguage}_{toLanguage}'
        return registry[key][0] if key in registry.keys() else {}     
    
    def _get_custom(self, fromLanguage, toLanguage):
        """
        Return customized translation of one language to another 
        """
        key = f'{fromLanguage}_{toLanguage}'
        return registry[key][1] if key in registry.keys() else {}     

    def _get_expressions(self, fromLanguage, toLanguage):
        """
        Return customized expressions of one language to another 
        """
        key = f'{fromLanguage}_{toLanguage}'
        return registry[key][2] if key in registry.keys() else {}, registry[key][3] if key in registry.keys() else {} 
