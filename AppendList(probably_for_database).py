from pathlib import Path
import re

def get_sorted_content(filename):
    filepath = Path(filename)

    # Check if the file exists
    if not filepath.exists():
        return []

    with open(filepath, 'r') as file:
        lines = file.readlines()

        # Strip out existing numbers and sort the lines alphabetically
        return sorted(re.sub(r"^\d+\.\s+", "", line).strip() for line in lines)

def append_to_file(filename, content):
    filepath = Path(filename)

    # Get the existing content of the file without numbers
    existing_content = get_sorted_content(filename)

    # Append the new content to the existing content
    existing_content.append(content)

    # Sort the combined content
    sorted_content = sorted(existing_content)

    # Write back to the file with numbers before each input
    with open(filepath, 'w') as file:
        for index, line in enumerate(sorted_content, 1):
            file.write(f"{index}. {line}\n")

def main():
    filename = "/Users/sunluyi/Desktop/Journal List.txt"
    
    while True:
        # Take input from the user
        content = input("Enter a word or sentence (or 'exit' to quit): ")
        
        # Exit loop if user types 'exit'
        if content.lower() == 'exit':
            break
        
        # Append content to the file
        append_to_file(filename, content)
        print(f"'{content}' has been added to {filename}.")

if __name__ == "__main__":
    main()
