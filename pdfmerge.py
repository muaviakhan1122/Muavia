#python pdfmerge.py
import PyPDF2

pdffiles = ["1.pdf", "2.pdf"]  # Ensure you're using the correct file extensions
merger = PyPDF2.PdfMerger()

for filename in pdffiles:
    with open(filename, 'rb') as pdffile:  # Use context manager for file opening
        pdfReader = PyPDF2.PdfReader(pdffile)  # Correct method name 'PdfReader'
        merger.append(pdfReader)  # Merge the PDF content

merger.write('merged.pdf')  # Output the merged file
merger.close()
