import re

# Read dependencies from requirements.txt
with open('app/requirements.txt', 'r') as req_file:
    dependencies = [line.strip() for line in req_file if line.strip() and not line.startswith("#")]

# Convert dependencies to TOML format
dependencies_toml = ',\n    '.join(f'"{dep}"' for dep in dependencies)

# Read the config.toml file
with open('config.toml', 'r') as file:
    config_content = file.readlines()

# Define regex to find the dependencies line in config.toml
dependencies_regex = re.compile(r'^\s*dependencies\s*=\s*\[')

# Find the line to replace
updated_content = []
inside_dependencies = False
for line in config_content:
    if dependencies_regex.match(line):
        # Replace dependencies with formatted content
        updated_content.append(f'dependencies = [\n    {dependencies_toml}\n]\n')
        inside_dependencies = True
    elif inside_dependencies and line.strip() == "]":
        inside_dependencies = False
    elif not inside_dependencies:
        updated_content.append(line)

# Write back the updated content to config.toml
with open('config.toml', 'w') as file:
    file.writelines(updated_content)

print("config.toml has been updated with the latest dependencies.")

