import json, re, subprocess
from pathlib import Path

# Pattern to identify Python import statements
IMPORT_PATTERN = re.compile(r"^\s*(import|from)\s+[\w\.]+(\s+import\s+[\w\.\*\,\s]+)?")

def remove_duplicate_imports(nb_path: Path, save_as: Path = None) -> Path:
    """
    Remove duplicate import statements in a Jupyter notebook, keeping only the first occurrence.
    Returns the path to the cleaned notebook.
    """
    print(f"Opening notebook for deduplication: {nb_path}")
    with open(nb_path, 'r', encoding='utf-8') as f:
        notebook = json.load(f)  # Load notebook content as JSON

    seen = set()  # Track already encountered import lines
    for i, cell in enumerate(notebook.get('cells', [])):
        if cell.get('cell_type') != 'code':
            continue  # Skip non-code cells
        print(f"Processing code cell {i}")
        new_lines = []
        for line in cell.get('source', []):
            if IMPORT_PATTERN.match(line.strip()):  # Check if line is an import statement
                if line.strip() in seen:
                    print(f"Duplicate import skipped: {line.strip()}")
                    continue  # Skip duplicate imports
                seen.add(line.strip())
                print(f"Import added: {line.strip()}")
            new_lines.append(line)  # Add non-duplicate lines
        cell['source'] = new_lines  # Replace cell source with filtered lines

    out_path = save_as or nb_path.with_name(nb_path.stem + '_dedup.ipynb')
    print(f"Saving deduplicated notebook to: {out_path}")
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(notebook, f, indent=1)  # Save updated notebook

    return out_path

def sort_imports(nb_path: Path) -> None:
    """
    Sort and deduplicate imports in a notebook using isort via nbqa.
    Requires: nbqa, isort
    """
    print(f"Sorting imports in notebook using isort: {nb_path}")
    subprocess.run([
        'nbqa', 'isort', str(nb_path), '--in-place'  # Execute isort with nbqa in-place
    ], check=True)
    print("Sorting complete.")

def remove_unused_imports(nb_path: Path) -> None:
    """
    Remove unused imports and variables using autoflake via nbqa.
    Requires: nbqa, autoflake
    """
    print(f"Removing unused imports from notebook using autoflake: {nb_path}")
    subprocess.run([
        'nbqa', 'autoflake', str(nb_path), '--in-place',
        '--remove-all-unused-imports', '--remove-unused-variables'  # Remove both unused imports and variables
    ], check=True)
    print("Unused import removal complete.")

def clean_notebook(nb_path: str, save_as: str = None) -> str:
    """
    Full pipeline: remove duplicates, sort imports, remove unused imports.
    Returns path to final cleaned notebook.
    """
    print(f"Starting cleaning pipeline for: {nb_path}")
    nb = Path(nb_path)  # Convert input path string to Path object
    
    # Step 1: Remove duplicate imports
    deduped = remove_duplicate_imports(nb, Path(save_as) if save_as else None)

    # Step 2: Sort imports
    sort_imports(deduped)

    # Step 3: Remove unused imports
    remove_unused_imports(deduped)

    print(f"Notebook cleaned and saved at: {deduped}")
    return str(deduped)
