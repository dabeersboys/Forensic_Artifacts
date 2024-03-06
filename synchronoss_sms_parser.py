import os

def create_html_table(directory):
    file_info = []
    
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".txt"):
                file_path = os.path.join(root, file)
                date_folder = os.path.basename(root)
                directory_name = os.path.basename(os.path.dirname(root))
                file_name = os.path.basename(file)
                
                with open(file_path, 'r') as f:
                    file_contents = f.read()
                
                file_info.append((date_folder, directory_name, file_name, file_contents))
    
    file_info.sort(key=lambda x: x[2])  # Sort by file name
    
    table_content = "<table border='1'><tr><th>Date</th><th>Direction</th><th>File Name</th><th>Contents</th></tr>"
    
    for info in file_info:
        table_content += f"<tr><td>{info[0]}</td><td>{info[1]}</td><td>{info[2]}</td><td>{info[3]}</td></tr>"
    
    table_content += "</table>"
    return table_content

def main():
    sms_directory = input("Drag and drop sms folder here. Remove any quotations in file path: ")
    html_table = create_html_table(sms_directory)
    
    with open("sms_report.html", 'w') as output_file:
        output_file.write(html_table)

if __name__ == "__main__":
    main()
