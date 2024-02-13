import xml.etree.ElementTree as ET

def parse_xml_element(element, parent_id, mermaid_markup, current_id=[0]):
    """
    Recursively parse XML elements to generate MermaidJS markup.
    
    :param element: The XML element to parse.
    :param parent_id: The ID of the parent element.
    :param mermaid_markup: The MermaidJS markup being generated.
    :param current_id: A mutable default parameter used to assign unique IDs to elements.
    """
    current_id[0] += 1
    my_id = current_id[0]
    
    # Add the current element to the markup
    mermaid_markup.append(f"{parent_id} -->|{element.tag}| {my_id}")

    # Recursively process child elements
    for child in element:
        parse_xml_element(child, my_id, mermaid_markup, current_id)

def xml_to_mermaid(xml_file):
    """
    Converts an XML structure to a MermaidJS graph structure.

    :param xml_file: Path to the XML file.
    :return: A string containing the MermaidJS markup.
    """
    # Parse the XML file
    tree = ET.parse(xml_file)
    root = tree.getroot()

    # Initialize MermaidJS markup
    mermaid_markup = ["graph TD"]

    # Start parsing from the root
    parse_xml_element(root, "root", mermaid_markup)

    return '\n'.join(mermaid_markup)

# Example Usage
xml_file = 'path_to_your_file.xml'  # Replace with your XML file path
mermaid_markup = xml_to_mermaid(xml_file)
print(mermaid_markup)
