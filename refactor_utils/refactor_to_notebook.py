import nbformat
import subprocess
from nbformat import read, write


def extract_code_cells_to_script(nb_path: str, script_path: str) -> None:
    """
    Extracts code cells from a Jupyter notebook and writes them into a Python script.

    Args:
        nb_path: Path to the source notebook (.ipynb).
        script_path: Path where the intermediate .py script will be saved.
    """
    # Read the notebook
    notebook = read(nb_path, as_version=4)
    with open(script_path, 'w', encoding='utf-8') as script_file:
        for cell in notebook.cells:
            if cell.cell_type == 'code':
                # Write each code cell, preserving original spacing
                script_file.write(cell.source.rstrip() + '\n\n')


def apply_code_formatters(script_path: str) -> None:
    """
    Runs isort, Black, and Flynt on a Python script to normalize imports,
    enforce PEP 8 formatting for Python 3.11, and convert .format() to f-strings.

    Args:
        script_path: Path to the Python script to format.
    """
    # Organize imports alphabetically
    subprocess.run(['isort', script_path], check=True)
    # Apply code formatting for Python 3.11 compatibility
    subprocess.run(['black', '--target-version', 'py311', script_path], check=True)
    # Convert .format() usages into f-strings for readability
    subprocess.run(['flynt', '-i', script_path], check=True)


def script_to_notebook(script_path: str) -> nbformat.NotebookNode:
    """
    Splits a formatted Python script into discrete Jupyter code cells.

    Args:
        script_path: Path to the formatted .py script.

    Returns:
        A new NotebookNode containing code cells.
    """
    with open(script_path, 'r', encoding='utf-8') as script_file:
        lines = script_file.readlines()

    new_nb = nbformat.v4.new_notebook()
    cells = []
    buffer = []

    for line in lines:
        # Separate cells on blank lines
        if line.strip() == '' and buffer:
            cells.append(nbformat.v4.new_code_cell(''.join(buffer)))
            buffer = []
        else:
            buffer.append(line)
    # Include any trailing code as the last cell
    if buffer:
        cells.append(nbformat.v4.new_code_cell(''.join(buffer)))

    new_nb.cells = cells
    return new_nb


def refactor_notebook(orig_nb: str, refactored_nb: str) -> None:
    """
    Orchestrates the full refactoring pipeline:
    1. Extract code cells to a script
    2. Apply formatting and improvements
    3. Convert back to a notebook

    Args:
        orig_nb: Path to the original .ipynb file.
        refactored_nb: Destination path for the refactored .ipynb file.
    """
    script_path = orig_nb.replace('.ipynb', '.py')

    extract_code_cells_to_script(orig_nb, script_path)
    apply_code_formatters(script_path)
    new_nb = script_to_notebook(script_path)

    # Save the refactored notebook
    with open(refactored_nb, 'w', encoding='utf-8') as out_file:
        write(new_nb, out_file)
    print(f"Refactored notebook saved to '{refactored_nb}'.")


if __name__ == '__main__':
    # Define file paths
    source_notebook = 'credit-fraud-dealing-with-imbalanced-datasets.ipynb'
    output_notebook = 'credit-fraud-dealing-with-imbalanced-datasets-refactored.ipynb'

    # Run the refactoring process
    refactor_notebook(source_notebook, output_notebook)
