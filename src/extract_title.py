import re

def extract_title(markdown):   
    lines = markdown.split("\n")
    
    for line in lines:
        if line.startswith("# "):
            return line[2:].strip()
    
        if line == "#":
            return ""
    
    raise Exception("The markdown file has no title.")