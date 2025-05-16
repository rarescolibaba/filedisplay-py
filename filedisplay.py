import os
import unicodedata

def remove_diacritics_and_sentence_case(text: str) -> str:
    nfkd_form = unicodedata.normalize('NFKD', text)
    ascii_text = "".join([c for c in nfkd_form if not unicodedata.combining(c)])
    return ascii_text

def list_directory_hierarchy(start_path: str, max_depth: int = -1):

    GLYPH_SPACE = "    "
    GLYPH_BRANCH = "├───" # U+251C BOX DRAWINGS LIGHT VERTICAL AND RIGHT, U+2500 LIGHT HORIZONTAL (x3)
    GLYPH_VERTICAL = "│   " # U+2502 BOX DRAWINGS LIGHT VERTICAL
    GLYPH_LAST_BRANCH = "└───" # U+2514 BOX DRAWINGS LIGHT UP AND RIGHT, U+2500 LIGHT HORIZONTAL (x3)

    def _recursive_list(current_path, prefix, current_depth):
        if max_depth != -1 and current_depth > max_depth:
            return

        try:
            entries = [e for e in os.listdir(current_path) if not e.startswith('.')]
            entries.sort()
        except PermissionError:
            print(f"{prefix}{GLYPH_LAST_BRANCH} [Permission denied]")
            return
        except FileNotFoundError:
            print(f"{prefix}{GLYPH_LAST_BRANCH} [Error: not found or is not a directory]")
            return


        num_entries = len(entries)
        for i, entry_name in enumerate(entries):
            is_last = (i == num_entries - 1)
            connector = GLYPH_LAST_BRANCH if is_last else GLYPH_BRANCH

            display_name = remove_diacritics_and_sentence_case(entry_name)
            
            full_path = os.path.join(current_path, entry_name)
            
            print(f"{prefix}{connector}{display_name}")
            
            if os.path.isdir(full_path):
                next_prefix = prefix + (GLYPH_SPACE if is_last else GLYPH_VERTICAL)
                _recursive_list(full_path, next_prefix, current_depth + 1)

    if not os.path.isdir(start_path):
        print(f"Error: Path '{start_path}' is not a directory or does not exist.")
        return

    root_display_name = remove_diacritics_and_sentence_case(os.path.basename(start_path))
    if not root_display_name :
        root_display_name = remove_diacritics_and_sentence_case(os.path.abspath(start_path))
        root_display_name = os.path.basename(root_display_name)


    print(f"{root_display_name}")
    _recursive_list(start_path, "", 0)


if __name__ == "__main__":
    current_folder = os.getcwd()
    
    print("Current folder hierarchy:")
    list_directory_hierarchy(current_folder)
