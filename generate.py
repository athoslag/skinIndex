import os

# Define the directories
image_dir = 'image'
skin_dir = 'skin'
pages_output_dir = 'pages' # Directory for paginated files index2.html, index3.html, etc.

# Util method
def remove_zeros(arg):
    filename = arg
    while filename and filename[0] == '0': # Added check for empty string
        filename = filename[1:]
    return filename if filename else "0" # Return "0" if all zeros were removed or input was "0"

# Get the list of image files
if not os.path.isdir(image_dir):
    print(f"Error: Image directory '{image_dir}' not found.")
    exit()

image_files = [f for f in os.listdir(image_dir) if f.lower().endswith('.jpg')] # Made extension check case-insensitive
image_files.sort() # Sort alphabetically

if not image_files:
    print(f"No .jpg files found in '{image_dir}'.")
    exit()

# Pagination settings
items_per_page = 100
total_pages_count = (len(image_files) + items_per_page - 1) // items_per_page

# Create pages directory if it doesn't exist and there's more than one page
if total_pages_count > 1 and not os.path.exists(pages_output_dir):
    os.makedirs(pages_output_dir)

# Function to generate HTML content for a page
def generate_html_page(current_page_num, all_image_files, total_pages, is_main_index_page):
    # --- Start: Generate Pagination HTML (common for top and bottom) ---
    pagination_html_content = '<div class="pagination">\n'
    
    # Previous link
    if current_page_num > 1:
        prev_target_page_num = current_page_num - 1
        prev_href = ""
        if prev_target_page_num == 1: # Target is the main index.html (logical page 1)
            # If current page is in pages_output_dir (e.g., pages/index2.html), link to ../index.html
            # If current page is the main index.html (this case shouldn't happen for "Previous" if total_pages > 1 and current_page_num > 1)
            # The logic below correctly assumes if current_page_num > 1, and prev_target is 1, we are on a sub-page.
            prev_href = "../index.html"
        else: # Target is pages/indexN.html (logical page > 1)
            # Current page is also in pages_output_dir (e.g. pages/index3.html linking to index2.html)
            prev_href = f"index{prev_target_page_num}.html"
        pagination_html_content += f'<a href="{prev_href}">Previous</a>\n'

    # Numbered links
    for i in range(1, total_pages + 1):
        link_class = 'current' if i == current_page_num else ''
        href = ""
        if i == 1: # Link to the main index.html (logical page 1)
            href = "../index.html" if not is_main_index_page else "index.html"
        else: # Link to pages/index<i>.html (logical page i > 1)
            href = f"index{i}.html" if not is_main_index_page else f"{pages_output_dir}/index{i}.html"
        
        pagination_html_content += f'<a class="{link_class}" href="{href}">{i}</a>\n'

    # Next link
    if current_page_num < total_pages:
        next_target_page_num = current_page_num + 1
        # If current page is main index.html, next is pages/index2.html
        # If current page is pages/indexN.html, next is pages/indexN+1.html
        href_next = f"{pages_output_dir}/index{next_target_page_num}.html" if is_main_index_page else f"index{next_target_page_num}.html"
        pagination_html_content += f'<a href="{href_next}">Next</a>\n'
    
    pagination_html_content += '</div>\n'
    # --- End: Generate Pagination HTML ---

    html_content = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Reborn Fighters Skins - Page {current_page_num}</title>
<style>
body {{
    background: #000;
    color: #eee; /* Added default text color for better readability */
    font-family: sans-serif; /* Added a default font */
}}
.grid {{
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
    gap: 20px;
    padding: 20px;
}}
.card {{
    border: 1px solid #808080;
    padding: 10px;
    text-align: center;
    border-radius: 8px;
    background: #0f0f0f;
}}
.card img {{
    max-width: 100%;
    height: auto;
    border-radius: 4px;
}}
.download-btn {{
    margin-top: 10px;
    display: inline-block;
    padding: 8px 12px;
    background-color: #0056b3;
    color: white;
    text-decoration: none;
    border-radius: 4px;
}}
.download-btn:hover {{
    background-color: #007bff;
}}
.pagination {{
    text-align: center;
    margin: 20px 0;
}}
.pagination a {{
    margin: 0 5px;
    padding: 8px 12px;
    background-color: #0056b3;
    color: white;
    text-decoration: none;
    border-radius: 4px;
}}
.pagination a:hover {{
    background-color: #007bff;
}}
.pagination .current {{
    background-color: #808080;
    pointer-events: none; /* Prevents clicking the current page link */
}}
</style>
</head>
<body>

<h1 style="text-align:center; color: #007bff;">Reborn Fighters / Getamped Skins</h1>
'''
    # Add pagination at the top if there's more than one page
    if total_pages > 1:
        html_content += pagination_html_content

    html_content += '\n<div class="grid">\n'

    # Determine asset path prefix (for images and skins)
    asset_path_prefix = "../" if not is_main_index_page else ""

    # Add image cards to the HTML content
    start_index = (current_page_num - 1) * items_per_page
    end_index = min(start_index + items_per_page, len(all_image_files))
    for image_file_name in all_image_files[start_index:end_index]:
        base_name = os.path.splitext(image_file_name)[0]
        display_name = remove_zeros(base_name)
        
        skin_file_skin_ext = f"{base_name}.skin"
        skin_file_hskin_ext = f"{base_name}.hskin"
        
        path_to_check_skin_ext = os.path.join(skin_dir, skin_file_skin_ext)
        path_to_check_hskin_ext = os.path.join(skin_dir, skin_file_hskin_ext)
        
        actual_skin_filename = None
        
        if os.path.exists(path_to_check_skin_ext):
            actual_skin_filename = skin_file_skin_ext
        elif os.path.exists(path_to_check_hskin_ext):
            actual_skin_filename = skin_file_hskin_ext
            
        download_link_html = ""
        if actual_skin_filename:
            download_link_html = f'<a class="download-btn" href="{asset_path_prefix}{skin_dir}/{actual_skin_filename}" download>Download #{display_name}</a>'
        else:
            download_link_html = f'<p style="color:red; margin-top:10px;">Skin #{display_name} not found</p>'

        html_content += f'''
<div class="card">
    <img src="{asset_path_prefix}{image_dir}/{image_file_name}" alt="Image {base_name}">
    {download_link_html}
</div>
'''

    html_content += '</div>\n' # Close grid

    # Add pagination at the bottom if there's more than one page
    if total_pages > 1:
        html_content += pagination_html_content
    
    html_content += '''
</body>
</html>
'''
    return html_content

# Generate HTML files for each page
for page_num_to_generate in range(1, total_pages_count + 1):
    is_this_the_main_index_file = (page_num_to_generate == 1)
    
    html_page_content = generate_html_page(page_num_to_generate, image_files, total_pages_count, is_this_the_main_index_file)
    
    output_file_path = ""
    if is_this_the_main_index_file:
        output_file_path = 'index.html' # Root directory
    else:
        output_file_path = os.path.join(pages_output_dir, f'index{page_num_to_generate}.html')
    
    with open(output_file_path, 'w', encoding='utf-8') as f:
        f.write(html_page_content)
    print(f"Generated: {output_file_path}")

print(f"\nHTML files have been generated successfully. Main file is index.html.")
if total_pages_count > 1:
    print(f"Other pages are in the '{pages_output_dir}/' directory (e.g., {pages_output_dir}/index2.html).")
