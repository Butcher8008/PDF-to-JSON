import json
import pdfplumber

def extract_pdf_info(pdf_file_path):
    pdf_data = {
        "MetaData": {},
        "Total_Pages": 0,
        "Words": [],
        "Text": "",
    }
    
    with pdfplumber.open(pdf_file_path) as pdf:
        # Extract metadata
        pdf_data["MetaData"] = {
            "Title": pdf.metadata.get("title", ""),
            "Author": pdf.metadata.get("author", ""),
            "Creator": pdf.metadata.get("creator", ""),
            "Creation_Date": pdf.metadata.get("creationDate", ""),
            "Modification_Date": pdf.metadata.get("modDate", ""),
            "PDF_Version": pdf.metadata.get("pdfVersion", ""),
        }
        
        # Extract text and word coordinates
        text = ""
        for page_number, page in enumerate(pdf.pages):
            text += page.extract_text()
            for word in page.extract_words():
                pdf_data["Words"].append({
                    "text": word["text"],
                    "xmin": word["x0"],
                    "ymin": page.height - word["top"],
                    "xmax": word["x1"],
                    "ymax": page.height - word["bottom"]
                })
        pdf_data["Text"] = text
        pdf_data["Total_Pages"] = len(pdf.pages)
        
    return pdf_data

def convert_pdf_to_json(pdf_file_path):
    pdf_info = extract_pdf_info(pdf_file_path)
    
    class pdf_to_json_converter:
        def __init__(self):
            self.mImageHashOnly = False
            self.mDocument = None
            pass

        def convert(self, info):
            lDict = info
            return lDict

    converter = pdf_to_json_converter()
    pdf_json_data = converter.convert(pdf_info)
    output_json_file = pdf_file_path.split('.')[0] + '.json'
    with open(output_json_file, 'w') as f:
        json.dump(pdf_json_data, f, indent=4)

    return output_json_file

# Example usage:
pdf_file_path = "sample-pdf-file.pdf"  # Replace "sample-pdf-file.pdf" with the path to your PDF file
json_output_file = convert_pdf_to_json(pdf_file_path)
print("PDF converted to JSON. Output file:", json_output_file)
