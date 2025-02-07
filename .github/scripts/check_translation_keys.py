import json
import os

"""
This script checks that all translation.json files in the 'locales' directory
(en, fi, sv) have the same set of keys to ensure consistency across languages.
"""

def get_keys_from_file(filename):
    """Load JSON file and return a set of its keys."""
    with open(filename, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return set(data.keys())

def main():
    path = 'client/public/locales'  # Base directory containing language folders
    languages = ['en', 'fi', 'sv']
    files = [os.path.join(path, lang, 'translation.json') for lang in languages]

    # Check if all expected files exist
    missing_files = [file for file in files if not os.path.exists(file)]
    if missing_files:
        print(f"Error: Missing translation files: {missing_files}")
        exit(1)

    all_keys = []

    # Get keys from each file
    for file in files:
        all_keys.append((file, get_keys_from_file(file)))

    # Explicitly set English as the reference
    base_file, base_keys = next((file, keys) for file, keys in all_keys if 'en/translation.json' in file)

    for file, keys in all_keys:
        if file == base_file:
            continue
        if keys != base_keys:
            diff = keys.symmetric_difference(base_keys)
            print(f"Keys mismatch between {base_file} and {file}. Difference: {diff}")
            exit(1)

    print("All translation files have consistent keys!")

if __name__ == "__main__":
    main()
