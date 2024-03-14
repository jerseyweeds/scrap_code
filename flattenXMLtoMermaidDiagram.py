import xml.etree.ElementTree as ET

def parse_xml_recursively(element, parent_id, mermaid_structure, id_counter):
    # Increment the counter for unique ID
    current_id = id_counter[0]
    id_counter[0] += 1

    # Get the current tag name
    current_tag = f"{element.tag}{current_id}"

    # Add to the mermaid structure
    if parent_id is not None:
        mermaid_structure.append(f"{parent_id} --> {current_tag}")

    # Process children
    for child in element:
        parse_xml_recursively(child, current_tag, mermaid_structure, id_counter)

def xml_to_mermaid(xml_path):
    # Parse the XML file
    tree = ET.parse(xml_path)
    root = tree.getroot()

    # Initialize mermaid structure and a counter for unique IDs
    mermaid_structure = ["graph TD"]
    id_counter = [0]

    # Parse recursively
    parse_xml_recursively(root, None, mermaid_structure, id_counter)

    return "\n".join(mermaid_structure)

# Replace 'your_file.xml' with your actual XML file path
xml_file_path = 'your_file.xml'
mermaid_diagram = xml_to_mermaid(xml_file_path)
print(mermaid_diagram)