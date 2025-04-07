import sys
import re
import numpy as np

if len(sys.argv) != 3:
    print("Usage: python script.py <file_path> <amplitude_table_name>")
    sys.exit(1)

file_path = sys.argv[1]
table_name = sys.argv[2]

try:
    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        data = f.read()
except FileNotFoundError:
    print(f"File not found: {file_path}")
    sys.exit(1)

# Build dynamic regex using the table name
pattern = fr'{re.escape(table_name)}(.*?)\x02'

# multiple instances of the table name in the file
halfway = len(data) // 2
data = data[halfway:]

match = re.search(pattern, data, re.DOTALL)
if match:
    middle_section = match.group(1)

    # Match numbers with optional decimals
    number_matches = re.findall(r'\d+(?:\.\d+)?', middle_section)

    # Convert all to float
    all_numbers = [float(n) for n in number_matches]

    # Drop the first and last numbers if they're unwanted junk
    if len(all_numbers) > 2:
        cleaned_numbers = all_numbers[1:-1]
    else:
        cleaned_numbers = all_numbers

    # Convert to NumPy array
    numbers = np.array(cleaned_numbers)
    print("Extracted NumPy array:")
    print(numbers)
else:
    print(f"No section found for table: {table_name} in file: {file_path}. Check the table name and try again.")

