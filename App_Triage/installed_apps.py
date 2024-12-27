def filter_lines(input_file, output_file):
    with open(input_file, 'r') as infile:
        lines = infile.readlines()

    # Filter out lines that start with the specified prefixes
    filtered_lines = [line for line in lines if not line.startswith((
        'com.apple', 'com.android', 'com.google', 'com.samsung',
        'com.mediatek', 'com.sec.', 'android.auto', 
        'com.tmobile', 'com.qualcom'
    ))]

    with open(output_file, 'w') as outfile:
        outfile.writelines(filtered_lines)

# Get input file path from user and strip surrounding quotes
input_file = input("Drag and Drop Installed Apps Text File: ").strip('"')
output_file = "./Possible_3rdParty_apps.txt"

# Call the function to filter lines
filter_lines(input_file, output_file)

print(f"Filtered lines written to {output_file}")
