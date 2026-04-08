import PyPDF2
import docx


def read_pdf(file):

    text = ""

    pdf = PyPDF2.PdfReader(file)

    for page in pdf.pages:

        if page.extract_text():
            text += page.extract_text()

    return text


def read_docx(file):

    doc = docx.Document(file)

    text = ""

    for p in doc.paragraphs:
        text += p.text

    return text


def read_txt(file):

    return file.read().decode("utf-8")