#For use with a list of installed apps on a mobile device to aid in filtering not native apps for further research and analysis.
#Files need to be like a word list with one package name perline

def filter_lines(input_file, output_file):
    with open(input_file, 'r') as infile:
        lines = infile.readlines()

    filtered_lines = [line for line in lines if not line.startswith(('com.apple', 'com.android', 'com.google', 'com.samsung', 'com.mediatek', 'com.sec.android', 'android.auto'))]

    with open(output_file, 'w') as outfile:
        outfile.writelines(filtered_lines)

input_file = input("Drag and Drop Installed Apps Text File: ").strip('"')  # Removing surrounding quotes from the file path
output_file = "./Possible_3rdParty_apps.txt"
filter_lines(input_file, output_file)
