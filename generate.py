import os

# Define the directories
image_dir = 'image'
skin_dir = 'skin'

# Get the list of image files
image_files = [f for f in os.listdir(image_dir) if f.endswith('.jpg')]

# Create the HTML content
html_content = '''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Image Grid with Skin Downloads</title>
  <style>
    .grid {
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
      gap: 20px;
      padding: 20px;
    }
    .card {
      border: 1px solid #ccc;
      padding: 10px;
      text-align: center;
      border-radius: 8px;
      background: #f9f9f9;
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
      background-color: #007bff;
      color: white;
      text-decoration: none;
      border-radius: 4px;
    }
    .download-btn:hover {
      background-color: #0056b3;
    }
  </style>
</head>
<body>

  <div class="grid">
'''

# Add image cards to the HTML content
for image_file in image_files:
    base_name = os.path.splitext(image_file)[0]
    skin_file = f"{base_name}.skin"
    html_content += f'''
    <div class="card">
      <img src="{image_dir}/{image_file}" alt="{base_name}">
      <a class="download-btn" href="{skin_dir}/{skin_file}" download>Download Skin</a>
    </div>
    '''

# Close the HTML tags
html_content += '''
  </div>

</body>
</html>
'''

# Write the HTML content to a file
with open('index.html', 'w') as f:
    f.write(html_content)

print("HTML file 'index.html' has been generated successfully.")

