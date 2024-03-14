
import xml.etree.ElementTree as ET

def parse_xml_recursively(element, parent_tag, mermaid_structure):
    # Get the current tag name
    current_tag = element.tag

    # Add to the mermaid structure
    if parent_tag:
        connection = f"{parent_tag} --> {current_tag}"
        if connection not in mermaid_structure:
            mermaid_structure.append(connection)

    # Process children
    for child in element:
        parse_xml_recursively(child, current_tag, mermaid_structure)

def xml_to_mermaid(xml_path):
    # Parse the XML file
    tree = ET.parse(xml_path)
    root = tree.getroot()

    # Initialize mermaid structure
    mermaid_structure = ["graph TD"]

    # Parse recursively
    parse_xml_recursively(root, "", mermaid_structure)

    # Ensure distinct connections
    distinct_structure = list(set(mermaid_structure))

    return "\n".join(distinct_structure)

# Replace 'your_file.xml' with your actual XML file path
xml_file_path = 'your_file.xml'
mermaid_diagram = xml_to_mermaid(xml_file_path)
print(mermaid_diagram)