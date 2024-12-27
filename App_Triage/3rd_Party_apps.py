def filter_lines_to_html(input_file, output_file, is_android):
    with open(input_file, 'r') as infile:
        lines = infile.readlines()

    if is_android:
        filtered_lines = [
            f"<a href='https://play.google.com/store/apps/details?id={line.strip()}'>{line.strip()}</a>"
            for line in lines 
            if not line.startswith((
                'com.apple', 'com.android', 'com.google', 'com.samsung',
                'com.mediatek', 'com.sec.', 'android.auto', 
                'com.tmobile', 'com.qualcom'
            ))
        ]
    else:
        filtered_lines = [
            line.strip() for line in lines 
            if not line.startswith((
                'com.apple', 'com.android', 'com.google', 'com.samsung',
                'com.mediatek', 'com.sec.', 'android.auto', 
                'com.tmobile', 'com.qualcom'
            ))
        ]

    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>3rd Party App Triage Report</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 20px; }
            h1 { color: #333; }
            ul { list-style-type: none; padding: 0; }
            li { margin: 10px 0; }
            a { text-decoration: none; color: #007BFF; }
            a:hover { text-decoration: underline; }
        </style>
    </head>
    <body>
        <h1>Filtered Applications Report</h1>
        <ul>
    """

    for line in filtered_lines:
        html_content += f"<li>{line}</li>\n"

    
    html_content += """
        </ul>
    </body>
    </html>
    """

    
    with open(output_file, 'w') as outfile:
        outfile.write(html_content)


input_file = input("Drag and Drop Installed Apps Text File: ").strip('"')
output_file = "./3rd_Party_AppsReport.html"


while True:
    device_type = input("Is this device an Android (enter 1) or iOS (enter 2)? ")
    if device_type in {'1', '2'}:
        is_android = device_type == '1'
        break
    else:
        print("Invalid input. Please enter 1 for Android or 2 for iOS.")

filter_lines_to_html(input_file, output_file, is_android)

print(f"Filtered lines written to {output_file}")
