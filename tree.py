import os

def print_directory_tree(startpath, depth=3):
    for root, dirs, files in os.walk(startpath):
        level = root.replace(startpath, '').count(os.sep)
        if level >= depth:
            continue
        indent = ' ' * 4 * (level)
        print(f"{indent}[{os.path.basename(root)}]")
        subindent = ' ' * 4 * (level + 1)
        for f in files:
            print(f"{subindent}{f}")

# Llama a la función en el directorio actual
print_directory_tree(os.getcwd())

