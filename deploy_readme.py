import os
import sys

class ReadmeDeployer:
    def __init__(self):
        self.readme_file = 'README_content.md'

    def read_readme_content(self):
        try:
            with open(self.readme_file, 'r') as f:
                content = f.read()
            
            # Process the content to properly format code blocks
            lines = content.split('\n')
            formatted_lines = []
            in_code_block = False
            
            for line in lines:
                if line.strip() == '```':
                    in_code_block = not in_code_block
                    formatted_lines.append(line)
                elif in_code_block:
                    # Indent code block contents
                    formatted_lines.append('    ' + line)
                else:
                    formatted_lines.append(line)
            
            return '\n'.join(formatted_lines)
        except FileNotFoundError:
            print(f"Error: {self.readme_file} not found.")
            sys.exit(1)
        except IOError as e:
            print(f"Error reading {self.readme_file}: {e}")
            sys.exit(1)

    def deploy_readme(self):
        try:
            if os.path.exists('README.md'):
                overwrite = input("README.md already exists. Do you want to overwrite it? (y/n): ").lower()
                if overwrite != 'y':
                    print("Operation cancelled.")
                    return

            readme_content = self.read_readme_content()
            with open('README.md', 'w') as f:
                f.write(readme_content)
            print("README.md has been successfully created in the current directory.")

        except IOError as e:
            print(f"An error occurred while writing the file: {e}")
            sys.exit(1)
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            sys.exit(1)

def main():
    deployer = ReadmeDeployer()
    deployer.deploy_readme()

if __name__ == "__main__":
    main()