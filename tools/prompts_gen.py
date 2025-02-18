def read_or_create_file(filename):
    """Reads a file, creates an empty one if missing, and returns its content."""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        with open(filename, 'w', encoding='utf-8') as f:
            pass  # Create empty file
        return ''  # Return empty content for this run

def read_required_file(filename):
    """Reads a file and exits if it's missing (for templates)."""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        print(f"Error: Required file '{filename}' not found. Ensure you have generated the template files first.")
        exit(1)

# Read or create placeholder files (empty if missing)
bot_role = read_or_create_file('tools/prompt_templates/bot_role.txt')
files_log = read_or_create_file('tools/prompt_templates/files_log.txt')
desired_functions = read_or_create_file('tools/prompt_templates/desired_functions.txt')
errors = read_or_create_file('tools/prompt_templates/errors.txt')

# Read templates (required; exit if missing)
create_template = read_required_file('tools/prompt_templates/prompt_template_create.txt')
debug_template = read_required_file('tools/prompt_templates/prompt_template_debug.txt')

# Replace placeholders in templates
prompt_create = create_template.replace('<bot_role>', bot_role) \
                               .replace('<files_log>', files_log) \
                               .replace('<desired_functions>', desired_functions)

prompt_debug = debug_template.replace('<files_log>', files_log) \
                             .replace('<errors>', errors)

# Write final prompts to files
with open('tools/_prompt_create.txt', 'w', encoding='utf-8') as f:
    f.write(prompt_create)

with open('tools/_prompt_debug.txt', 'w', encoding='utf-8') as f:
    f.write(prompt_debug)

print("Successfully generated prompts. Empty files were created for missing placeholders.")