from nbconvert import HTMLExporter
import nbformat

def convert_notebook_to_html(notebook_path):
    # Load the notebook
    with open(notebook_path) as f:
        notebook_content = nbformat.read(f, as_version=4)

    # Use the 'skeleton' template
    html_exporter = HTMLExporter(template_name='skeleton')
    
    # Convert the notebook to HTML
    (body, resources) = html_exporter.from_notebook_node(notebook_content)

    return body
