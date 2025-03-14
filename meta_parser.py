from bs4 import BeautifulSoup
import os

def split_html_report_with_index(input_file, output_dir):
    # Create the output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # HTML header and style
    html_template = """
    <html>
    <head>
        <meta charset="UTF-8"/>
        <title>Meta Platforms Business Record</title>
        <style type="text/css">
            body {
                font-family: "DejaVu Sans Condensed", sans-serif;
                margin: 0;
            }
            table {
                table-layout: fixed;
                max-width: 209mm;
                word-break: break-word;
            }
            li label {
                max-width: 80%;
                vertical-align: top;
            }
            .sticky_side_bar {
                width: 10%;
                overflow: hidden;
                position: absolute;
                display: block;
                padding: 20px;
            }
            .records_output {
                height: 100vh;
                overflow: auto;
                width: 210mm;
                min-height: 297mm;
                padding: 20mm;
                margin: 10mm auto;
                border: 1px #D3D3D3 solid;
                border-radius: 5px;
                background: white;
                box-shadow: 0 0 5px rgba(0, 0, 0, 0.1);
            }
            img, video, audio {
                max-width: 100%;
                max-height: 200mm;
            }
            .t .t {
                margin-left: 10px;
                max-width: 209mm;
                word-break: keep-all;
            }
            .o {
                font-weight: bold;
            }
            .i {
                font-weight: bold;
                display: table;
            }
            .m {
                font-weight: normal;
                display: table-cell;
                padding: 2px;
                word-break: break-word;
                word-wrap: break-word !important;
            }
            .p {
                padding: 5px;
            }
            .pageBreak {
                background-color: rgb(66, 103, 178);
                color: white;
                padding: 20px;
                text-align: center;
                left: 0px;
                position: relative;
            }
            @media print {
                .pageBreak {
                    display: block;
                    page-break-before: always;
                    page-break-inside: avoid;
                }
                .pageBreak:not(.pageBreak ~ .pageBreak) {
                    page-break-before: avoid;
                }
                @page {
                    size: auto;
                    margin: 1;
                }
            }
        </style>
    </head>
    <body>
    """

    # Closing tags for the HTML
    html_closing = "</body></html>"

    # Read the input HTML file
    with open(input_file, 'r', encoding='utf-8') as file:
        soup = BeautifulSoup(file, 'html.parser')

    # Find all links with hrefs pointing to IDs
    links = soup.find_all('a', href=True)
    ids_to_extract = {link['href'][1:] for link in links if link['href'].startswith('#')}

    # Create a list to store index links
    index_links = []

    # Extract sections by ID
    for section_id in ids_to_extract:
        section = soup.find(id=section_id)
        if section:
            # Create the individual section's HTML
            section_html = f"{html_template}{section.prettify()}{html_closing}"

            # Save the section to a new HTML file
            output_file = os.path.join(output_dir, f"{section_id}.html")
            with open(output_file, 'w', encoding='utf-8') as file:
                file.write(section_html)

            # Add a link to the index
            index_links.append(f'<li><a href="{section_id}.html">{section_id}</a></li>')

            print(f"Created: {output_file}")

    # Generate the index page
    index_html = f"""
    {html_template}
    <h1>Index of Sections</h1>
    <ul>
        {''.join(index_links)}
    </ul>
    {html_closing}
    """
    index_file = os.path.join(output_dir, "index.html")
    with open(index_file, 'w', encoding='utf-8') as file:
        file.write(index_html)

    print(f"Created index page: {index_file}")

# Example usage
input_html = input("Drag and Drop tha motha fucka: ")  # Replace with your HTML file
output_directory = 'output_sections'  # Replace with your desired output directory
split_html_report_with_index(input_html, output_directory)
