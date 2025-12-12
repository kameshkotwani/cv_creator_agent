from langchain_core.prompts import ChatPromptTemplate
# testing template loader
def template_loader(name:str):
    """
    Loads the templates from prompts directory.
    
    :param name: Description
    :type name: str
    """
    import tomllib
    
    with open(f"src/agents/prompts/{name}.toml", 'rb') as f:
        prompt = tomllib.load(f)['prompt']['template']

    return ChatPromptTemplate.from_template(prompt)
    
print(template_loader("experience"))
