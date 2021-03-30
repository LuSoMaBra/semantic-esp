from pdfminer.pdfinterp import PDFResourceManager, process_pdf
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from io import StringIO

from urllib.request import urlopen
import PyPDF2

def get_sites_to_recover():
    sites = []
    sites.append({'titulo': 'Instituições de Ensino Superior', 'url': 'https://dados.gov.pt/pt/datasets/r/59ed02b9-410c-4f68-81ef-a3755ca66400', 'tipo': 'json'})
    sites.append({'titulo': 'Classificação Nacional', 'url': 'https://dados.gov.pt/pt/datasets/r/1b8c4f59-a102-4cf3-9347-a2fca406762d', 'tipo': 'json'})

    # para ver com calma
    sites.append({'titulo': 'Indicadores de docentes', 'url': 'https://dados.gov.pt/pt/datasets/indicadores-relativos-a-docentes-no-sistema-de-educacao-e-formacao', 'tipo': 'xls'})

    # para ver com calma
    sites.append({'titulo': 'Doutoramentos', 'url': 'https://dados.gov.pt/pt/datasets/r/6e923177-f1ce-4126-8107-9e2d3969abd1', 'tipo': 'xls'})

    # interessante para promover decisão
    sites.append({'titulo': 'Volume de negócios das empresas', 'url': 'https://dados.gov.pt/pt/datasets/r/61882622-51b4-4ddc-adbc-5d34913e8972', 'tipo': 'xls'})
    sites.append({'titulo': 'Número de empresas', 'url': 'https://dados.gov.pt/pt/datasets/r/98271e8f-d65f-4828-8eaf-d3ba63738035', 'tipo': 'xls'})

    sites.append({'titulo': '1ª Fase - Médias de Ingresso no Acesso ao Ensino Superior', 'url': 'https://orientacao-vocacional.com.pt/wp-content/uploads/documentos/media_2020_1.pdf', 'tipo': 'pdf'})
    sites.append({'titulo': '2ª Fase - Médias de Ingresso no Acesso ao Ensino Superior', 'url': 'https://orientacao-vocacional.com.pt/wp-content/uploads/documentos/media_2020_2.pdf', 'tipo': 'pdf'})

    return sites

def lerPDF(arquivoPDF):
    # PDFResourceManager Usado para armazenar recursos compartilhados
    # como fontes e imagens
    recursos = PDFResourceManager()
    buffer = StringIO()
    layoutParams = LAParams()
    dispositivo = TextConverter(recursos, buffer, laparams=layoutParams)
    process_pdf(recursos, dispositivo, arquivoPDF)
    dispositivo.close()
    conteudo = buffer.getvalue()
    buffer.close()
    return conteudo

# esta função recebe o caminho do arquivo pdf e retorna seu texto extraido num string
def getPDFContent(filename):
    content = ""
    file = open(filename, "rb")
    pdf = PyPDF2.PdfFileReader(file)
    for i in range(0, pdf.getNumPages()):
        content += pdf.getPage(i).extractText() + "\n"
    file.close()
    return content
