

def markdown_to_blocks(md:str)->list[str]:
    if md is None: return []
    if len(md) < 1: return []
    sections = md.strip("\n").split("\n\n")
    sections = list(
        filter(lambda x: len(x) > 0, sections)
    )
    return sections
