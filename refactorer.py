import nbformat
from nbformat import write, read
import subprocess

# Path to the original and refactored notebook
orig_nb = 'credit-fraud-dealing-with-imbalanced-datasets.ipynb'
refactored_nb = 'updated_v2.ipynb'

# Read the original notebook
nb = read(orig_nb, as_version=4)

# Export to a Python script using nbformat
script_path = orig_nb.replace('.ipynb', '.py')
with open(script_path, 'w', encoding='utf-8') as f:
    for cell in nb.cells:
        if cell.cell_type == 'code':
            f.write(''.join(cell.source) + '\n\n')

# Use isort to sort and format imports
subprocess.run(['isort', script_path])

# Use Black for code formatting targeting Python 3.11
subprocess.run(['black', '--target-version', 'py311', script_path])

# Use Flynt to convert .format() to f-strings where possible
subprocess.run(['flynt', '-i', script_path])

# Read back the formatted script and convert to notebook cells
with open(script_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

new_nb = nbformat.v4.new_notebook()
new_cells = []
buffer = []
for line in lines:
    if line.strip() == '' and buffer:
        new_cells.append(nbformat.v4.new_code_cell(''.join(buffer)))
        buffer = []
    else:
        buffer.append(line)
# Append any remaining lines
if buffer:
    new_cells.append(nbformat.v4.new_code_cell(''.join(buffer)))

new_nb.cells = new_cells

# Write the refactored notebook
with open(refactored_nb, 'w', encoding='utf-8') as f:
    write(new_nb, f)

print(f"Refactored notebook saved to '{refactored_nb}'.")
