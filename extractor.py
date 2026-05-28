import re


def extract_invoice_number(text):

    patterns = [
        r'Invoice\\s*No[:\\s]*([A-Za-z0-9\\-/]+)',
        r'Invoice\\s*Number[:\\s]*([A-Za-z0-9\\-/]+)',
        r'Bill\\s*No[:\\s]*([A-Za-z0-9\\-/]+)',
        r'Tax\\s*Invoice[:\\s#]*([A-Za-z0-9\\-/]+)',
    ]

    for pattern in patterns:
        match = re.search(pattern, text, re.I)

        if match:
            return match.group(1)

    return "Not Found"


def extract_total_amount(text):

    patterns = [
        r'Grand\\s*Total[:\\s₹]*([\\d,]+\\.?\\d*)',
        r'Total\\s*Amount[:\\s₹]*([\\d,]+\\.?\\d*)',
        r'Total[:\\s₹]*([\\d,]+\\.?\\d*)',
    ]

    for pattern in patterns:
        match = re.search(pattern, text, re.I)

        if match:
            return match.group(1)

    return "Not Found"


def extract_gst_amount(text):

    cgst_match = re.search(
        r'CGST[:\\s₹]*([\\d,]+\\.?\\d*)',
        text,
        re.I
    )

    sgst_match = re.search(
        r'SGST[:\\s₹]*([\\d,]+\\.?\\d*)',
        text,
        re.I
    )

    if cgst_match and sgst_match:

        try:

            total_gst = (
                float(cgst_match.group(1).replace(',', '')) +
                float(sgst_match.group(1).replace(',', ''))
            )

            return str(total_gst)

        except:
            pass

    gst_match = re.search(
        r'GST[:\\s₹]*([\\d,]+\\.?\\d*)',
        text,
        re.I
    )

    if gst_match:
        return gst_match.group(1)

    return "Not Found"


def extract_vendor_name(text):

    lines = text.split('\\n')

    if len(lines) > 0:
        return lines[0]

    return "Not Found"
