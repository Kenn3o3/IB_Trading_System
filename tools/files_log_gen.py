import os
import argparse

def log_message(message, log_file):
    # Function to write a message to the log file
    with open(log_file, 'a', encoding='utf-8') as log:
        log.write(message + "\n")

def print_tree_structure(parent_dir, log_file):
    # Function to recursively print the file structure without printing the content
    for root, dirs, files in os.walk(parent_dir):
        # Remove __pycache__ directories from the list of directories to traverse
        dirs[:] = [d for d in dirs if d != '__pycache__']
        # Determine the level of the current directory in the tree
        level = root.replace(parent_dir, '').count(os.sep)
        indent = ' ' * 4 * level
        
        # Print the directory name and log it
        dir_message = f"{indent}└── {os.path.basename(root)}/"
        print(dir_message)
        log_message(dir_message, log_file)
        
        # Print the file names and log them
        for file in files:
            file_message = f"{indent}    ├── {file}"
            print(file_message)
            log_message(file_message, log_file)

def print_file_content(file_path, log_file):
    # Print the contents of the file and log it
    try:
        with open(file_path, 'r') as file:
            content = file.read()
            file_message = f"\n# {file_path} content:\n"
            print(file_message)
            log_message(file_message, log_file)
            print(f"    ```")
            log_message(f"    ```", log_file)
            print(content)
            log_message(content, log_file)
            print(f"    ```")
            log_message(f"    ```", log_file)
    except Exception as e:
        error_message = f"{' ' * 4}Error reading {file_path}: {str(e)}"
        print(error_message)
        log_message(error_message, log_file)

def print_full_tree_and_contents(parent_dir, log_file):
    # First, print the entire directory structure and log it
    print("Directory Structure:")
    log_message("Directory Structure:", log_file)
    print_tree_structure(parent_dir, log_file)

    # Then, print the content of each file and log it
    print("\nFile Contents:")
    log_message("\nFile Contents:", log_file)
    for root, dirs, files in os.walk(parent_dir):
        # Remove __pycache__ directories from the list of directories to traverse
        dirs[:] = [d for d in dirs if d != '__pycache__']
        for file in files:
            file_path = os.path.join(root, file)
            print_file_content(file_path, log_file)

def main():
    # Set up command-line argument parsing
    parser = argparse.ArgumentParser(description="Generate a file tree structure and log file contents.")
    parser.add_argument("parent_folder", help="Path to the parent folder to analyze")

    # Parse the arguments
    args = parser.parse_args()

    # Overwrite or create the log file
    with open("tools/prompt_templates/files_log.txt", 'w'): pass  # Creates or overwrites the log file

    # Run the function to print the tree structure and contents, while logging
    print_full_tree_and_contents(args.parent_folder, "tools/prompt_templates/files_log.txt")

if __name__ == "__main__":
    main()