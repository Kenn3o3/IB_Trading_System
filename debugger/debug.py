import os

def print_tree_structure_and_content(parent_dir):
    # Function to recursively print the file structure and content
    for root, dirs, files in os.walk(parent_dir):
        # Determine the level of the current directory in the tree
        level = root.replace(parent_dir, '').count(os.sep)
        indent = ' ' * 4 * level
        
        # Print the directory name
        print(f"{indent}└── {os.path.basename(root)}/")
        
        # Print the file names and their contents
        for file in files:
            file_path = os.path.join(root, file)
            print(f"{indent}    ├── {file}")
            print_file_content(file_path)

def print_file_content(file_path):
    # Print the contents of the file
    try:
        with open(file_path, 'r') as file:
            print(f"{' ' * 8}{{")
            print(file.read())
            print(f"{' ' * 8}}}")
    except Exception as e:
        print(f"{' ' * 8}Error reading {file_path}: {str(e)}")

# Example usage
parent_folder = 'code'  # Replace with your parent folder path
print_tree_structure_and_content(parent_folder)
