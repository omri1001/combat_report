# hyperlink_utils.py

from docx.oxml import OxmlElement
from docx.oxml.ns import qn
import docx.opc.constants

def add_hyperlink(paragraph, url, text):
    """
    Adds a clickable hyperlink to a paragraph.
    """
    # Access the document relationships to create a new hyperlink id
    part = paragraph.part
    r_id = part.relate_to(
        url,
        docx.opc.constants.RELATIONSHIP_TYPE.HYPERLINK,
        is_external=True
    )

    # Create the w:hyperlink tag and set the relationship id
    hyperlink = OxmlElement('w:hyperlink')
    hyperlink.set(qn('r:id'), r_id)

    # Create a run to hold the hyperlink text
    new_run = OxmlElement('w:r')

    # Create the run properties and set formatting
    rPr = OxmlElement('w:rPr')

    # Set font
    rFonts = OxmlElement('w:rFonts')
    rFonts.set(qn('w:ascii'), 'Arial')
    rFonts.set(qn('w:hAnsi'), 'Arial')
    rFonts.set(qn('w:eastAsia'), 'Arial')
    rPr.append(rFonts)

    # Set font size
    sz = OxmlElement('w:sz')
    sz.set(qn('w:val'), '24')  # 12 pt font size
    rPr.append(sz)

    # Underline
    u = OxmlElement('w:u')
    u.set(qn('w:val'), 'single')
    rPr.append(u)

    # Font color
    color = OxmlElement('w:color')
    color.set(qn('w:val'), '0000FF')  # Blue color
    rPr.append(color)

    # Create the text element and set the text
    w_t = OxmlElement('w:t')
    w_t.text = text

    # Build the hyperlink run
    new_run.append(rPr)
    new_run.append(w_t)
    hyperlink.append(new_run)

    # Add the hyperlink to the paragraph
    paragraph._p.append(hyperlink)

    return hyperlink
