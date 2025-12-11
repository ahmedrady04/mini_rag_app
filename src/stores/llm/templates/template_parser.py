import os

class TemplateParser:

    def __init__(self,language:str, default_language:str='en'):
        self.current_path= os.path.dirname(os.path.abspath(__file__))
        self.language=None
        self.default_language=default_language
        self.set_language(language=language)


    def set_language(self,language:str):
            if not language:
                self.language=self.default_language
            
            language_path=os.path.join(
                self.current_path, "locales", language
            )
            
            if os.path.exists(language_path):
                self.language=language

            else:
                self.language=self.default_language

    def get_template(self,group:str, key:str, vars:dict={}):
            if not group or not key:
                return None
            
            group_path=os.path.join(self.current_path,"locales",self.language,f"{group}.py")
            target_language=self.language
            if not os.path.exists(group_path):
                target_language=self.default_language
                group_path=os.path.join(self.current_path,"locales",target_language,f"{group}.py")

            if not os.path.exists(group_path):
                return None
            
            # import group module
            try:
                    module = __import__(f"stores.llm.templates.locales.{target_language}.{group}", fromlist=[group])
            except ImportError:
                    return None
            
            key_attribute = getattr(module, key)
            return key_attribute.substitute(vars)


