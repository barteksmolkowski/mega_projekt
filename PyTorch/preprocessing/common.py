# popatrzec na decorators.py i utils.py i przeniesc dekoratory w odpowiednie miejsca
# tu zrobic import potrzebnych decoratorow z decorators.py i utils.py
# dokonczyc augmentation.py
# podsumowac w __init__.py
# zrobic na github
from typing import List, Tuple

TypeColor = Tuple[int, int, int]
TypeShadeGrayColor = int
TypeMatrix = List[List[int]]
TypeRandom = int
TypeIMG = List[List[Tuple[int, int, int]]]
MatrixChannels = Tuple[List[List[int]]]

import pyperclip

__all__ = [
    "TypeColor",
    "TypeShadeGrayColor",
    "TypeMatrix",
    "TypeRandom",
    "TypeIMG",
    "MatrixChannels"
]

def generate_import_statement(clipboard: bool):
    header = "from common import ("
    footer = ")"
    body_elements = []

    for name in __all__:
        body_elements.append(f"    {name}")
                   
    body = ",\n".join(body_elements).lstrip(",")

    content = f"{header}\n{body}\n{footer}"

    if clipboard:
        pyperclip.copy(content)
        return "Content pasted to the clipboard."
    return f"{content}"

def main():
    result = generate_import_statement(clipboard=True)
    print(result)  


if __name__ == "__main__":
    main()