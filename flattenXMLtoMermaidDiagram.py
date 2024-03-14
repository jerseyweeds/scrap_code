import xml.etree.ElementTree as ET

def parse_xml_recursively(element, parent_name, mermaid_structure, level=0):
    # Get the current tag name
    current_tag = f"{element.tag}{level}"
    # Add to the mermaid structure
    if parent_name:
        mermaid_structure.append(f"{parent_name} --> {current_tag}")
    # Process children
    children = list(element)
    for i, child in enumerate(children):
        parse_xml_recursively(child, current_tag, mermaid_structure, level + 1 + i)

def xml_to_mermaid(xml_path):
    # Parse the XML file
    tree = ET.parse(xml_path)
    root = tree.getroot()

    # Initialize mermaid structure
    mermaid_structure = ["graph TD"]

    # Parse recursively
    parse_xml_recursively(root, "", mermaid_structure)

    return "\n".join(mermaid_structure)

# Replace 'your_file.xml' with your actual XML file path
xml_file_path = 'your_file.xml'
mermaid_diagram = xml_to_mermaid(xml_file_path)
print(mermaid_diagram)