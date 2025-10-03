from PyPDF2 import PdfFileWriter, PdfFileReader


merger = PdfWriter()

d = {}

for i in range(len(nums)):
    d[f'input{i}'] = open(f"./Outputs/slides/output{i}.pdf", "rb")   

for pdf in d.values():
    pdf.add_bookmark(chapter_name,0)
    merger.append(pdf)

merger.write("merged-pdf.pdf")
merger.close()


