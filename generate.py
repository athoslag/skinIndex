import os

# Define the directories
image_dir = 'image'
skin_dir = 'skin'

# Util method
def remove_zeros(arg):
    filename = arg
    while filename[0] == '0':
        filename = filename[1:]
    return filename

# Get the list of image files
image_files = [f for f in os.listdir(image_dir) if f.endswith('.jpg')]
image_files.sort()

# Pagination settings
items_per_page = 100
total_pages = (len(image_files) + items_per_page - 1) // items_per_page

# Function to generate HTML content for a page
def generate_html_page(page_num, image_files):
    html_content = '''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Reborn Fighters Skins</title>
<style>
body {
    background: #000;
}
.grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
    gap: 20px;
    padding: 20px;
}
.card {
    border: 1px solid #808080;
    padding: 10px;
    text-align: center;
    border-radius: 8px;
    background: #0f0f0f;
}
.card img {
    max-width: 100%;
    height: auto;
    border-radius: 4px;
}
.download-btn {
    margin-top: 10px;
    display: inline-block;
    padding: 8px 12px;
    background-color: #0056b3;
    color: white;
    text-decoration: none;
    border-radius: 4px;
}
.download-btn:hover {
    background-color: #007bff;
}
.pagination {
    text-align: center;
    margin: 20px 0;
}
.pagination a {
    margin: 0 5px;
    padding: 8px 12px;
    background-color: #0056b3;
    color: white;
    text-decoration: none;
    border-radius: 4px;
}
.pagination a:hover {
    background-color: #007bff;
}
.pagination .current {
    background-color: #808080;
    pointer-events: none;
}
</style>
</head>
<body>

<div class="grid">
'''

    # Add image cards to the HTML content
    start_index = (page_num - 1) * items_per_page
    end_index = min(start_index + items_per_page, len(image_files))
    for image_file in image_files[start_index:end_index]:
        base_name = os.path.splitext(image_file)[0]
        skin_file = f"{base_name}.skin"
        display_name = remove_zeros(base_name)
        html_content += f'''
<div class="card">
    <img src="{image_dir}/{image_file}" alt="{base_name}">
    <a class="download-btn" href="{skin_dir}/{skin_file}" download>Download #{display_name}</a>
</div>
'''

    # Add pagination links
    html_content += '''
</div>
<div class="pagination">
'''
    if page_num > 1:
        html_content += f'<a href="index{page_num - 1}.html">Previous</a>'
    for i in range(1, total_pages + 1):
        if i == page_num:
            html_content += f'<a class="current" href="index{i}.html">{i}</a>'
        else:
            html_content += f'<a href="index{i}.html">{i}</a>'
    if page_num < total_pages:
        html_content += f'<a href="index{page_num + 1}.html">Next</a>'
    html_content += '''
</div>

</body>
</html>
'''
    return html_content

# Generate HTML files for each page
for page_num in range(1, total_pages + 1):
    html_content = generate_html_page(page_num, image_files)
    file_name = f'index{page_num}.html'
    with open(file_name, 'w') as f:
        f.write(html_content)

print("HTML files have been generated successfully.")

