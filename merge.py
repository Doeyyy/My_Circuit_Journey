import os

# Configuration: Files to include and directories to skip
EXTENSIONS = ('.py', '.html', '.css', '.js')
EXCLUDE_DIRS = {'venv', '.git', '__pycache__', 'media', 'staticfiles', 'node_modules'}
OUTPUT_FILE = 'full_codebase.txt'

def merge_codebase():
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as outfile:
        for root, dirs, files in os.walk('.'):
            # Filter out excluded directories
            dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
            
            for file in files:
                if file.endswith(EXTENSIONS):
                    file_path = os.path.join(root, file)
                    outfile.write(f"\n{'='*50}\n")
                    outfile.write(f"FILE: {file_path}\n")
                    outfile.write(f"{'='*50}\n\n")
                    
                    try:
                        with open(file_path, 'r', encoding='utf-8') as infile:
                            outfile.write(infile.read())
                    except Exception as e:
                        outfile.write(f"Error reading file: {e}")
                    outfile.write("\n")

    print(f"Success! Codebase merged into {OUTPUT_FILE}")

if __name__ == "__main__":
    merge_codebase()