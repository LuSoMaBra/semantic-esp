import datetime
import scrapy
from db_tools import *
from urllib.parse import unquote
import json
from io import StringIO
from html.parser import HTMLParser

class MLStripper(HTMLParser):
    def __init__(self):
        super().__init__()
        self.reset()
        self.strict = False
        self.convert_charrefs= True
        self.text = StringIO()
    def handle_data(self, d):
        self.text.write(d)
    def get_data(self):
        return self.text.getvalue()

def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()

def cleanup(url):
    try:
        return unquote(url, errors='strict')
    except UnicodeDecodeError:
        return unquote(url, encoding='latin-1')


class NETEMPREGOSpider(scrapy.Spider):
    name = "NETEMPREGO_spider"

    option_dict = {'29': 'Administração / Secretariado', '39': 'Agricultura / Florestas / Pescas', '22': 'Arquitectura / Design', '40': 'Artes / Entretenimento / Media', '16': 'Banca / Seguros / Serviços ''Financeiros',
                   '47': 'Beleza / Moda / Bem Estar', '57': 'Call Center / Help Desk', '53': 'Comercial / Vendas', '8': 'Comunicação Social / Media', '51': 'Conservação / Manutenção / Técnica', '23': 'Construção Civil',
                   '15': 'Contabilidade / Finanças',
                   '28': 'Desporto / Ginásios', '44': 'Direito / Justiça', '11': 'Educação / Formação', '54': 'Engenharia ( Ambiente )', '45': 'Engenharia ( Civil )', '46': 'Engenharia ( Eletrotecnica )', '24': 'Engenharia ( Mecanica )',
                   '50': 'Engenharia ( Química / Biologia )', '41': 'Farmácia / Biotecnologia', '26': 'Gestão de Empresas / Economia', '32': 'Gestão RH', '9': 'Hotelaria / Turismo', '12': 'Imobiliário', '6': 'Indústria / Produção',
                   '38': 'Informática ( Analise de Sistemas )', '34': 'Informática ( Formação )', '37': 'Informática ( Gestão de Redes )', '35': 'Informática ( Internet )', '36': 'Informática ( Multimedia )', '5': 'Informática ( Programação )',
                   '49': 'Informática ( Técnico de Hardware )', '56': 'Informática (Comercial/Gestor de Conta)', '58': 'Limpezas / Domésticas', '30': 'Lojas / Comércio / Balcão', '19': 'Publicidade / Marketing', '18': 'Relações Públicas',
                   '42': 'Restauração / Bares / Pastelarias', '14': 'Saúde / Medicina / Enfermagem', '55': 'Serviços Sociais', '52': 'Serviços Técnicos', '1': 'Telecomunicações', '43': 'Transportes / Logística'}

    area_dict = {}

    data_raspagem = datetime.datetime.now()

    provenance_statement_id = 10

    fields = [
        'titulo',
        'descricao',
        'requisitos',
        'remuneracao',
        'localizacao',
        'modo',
        'area_curso',
        'provenance_statement_id'
    ]

    # link base: "Formação Superior", "Tempo Integral"
    link_base = 'https://www.net-empregos.com/pesquisa-empregos.asp?chaves=Forma%E7%E3o+Superior&cidade=&categoria={}&zona=0&tipo=1'

    areas = selectDB(connectDB(), 'select cn.areacnaef from curso c, curso_cnaef cn where c.curso_cnaef_id = cn.id')

    start_urls = []
    all_areas_list = []
    for x in areas:
        y = x[0].split(' - ')[1].split(' ')
        base_world = []
        for i in y:
            if len(i) > 3:
                base_world.append(i)
        print('base_world', base_world)
        option_list = []
        for i in base_world:
            for key, value in option_dict.items():
                if i in value:
                    option_list.append(key)
        print('option_list', option_list)
        option_list = list(set(option_list)) # retira duplicados
        area_dict[x[0]] = option_list
        all_areas_list = all_areas_list + option_list

    all_areas_list = list(set(all_areas_list))
    for i in all_areas_list:
        start_urls.append(link_base.format(i))

    def parse(self, response):

        links_jobs = response.css('.div-right a ::attr(href)')

        yield from response.follow_all(links_jobs, self.parse_job)

        next_page = response.css('a .page-link .d-none .d-lg-block ::attr(href)').extract_first()
        print('next_page', next_page)
        if next_page and next_page not in self.urls:
            yield scrapy.Request(
                response.urljoin(next_page),
                callback = self.parse
            )

    def parse_job(self, response):

        def extract_with_css(response, query):
            return response.css(query).extract_first(default='')

        def extract_list_with_css(response, query):
            return response.css(query)

        link = extract_list_with_css(response, '.job-details-page')
        for x in link:
            titulo = extract_with_css(x, 'h1 ::text')
            print('TITLE', titulo)
            description = extract_list_with_css(x, 'p')
            for y in description:
                # print(strip_tags(y))
                _y = extract_list_with_css(y, '::text')
                descricao = ''
                for k in _y:
                    descricao = descricao + (k.get().lstrip().rstrip() + ' ').replace("'", "")

            localizacao = 'Veja em Descrição'
            modo = 'Veja em Descrição'

            categoria = cleanup(str(response.request.headers['Referer'].decode("utf-8")).split('categoria=')[1].split('&zona')[0].replace('+', ' '))

            remuneracao = 'Não informada'

            if titulo:
                for key, value in self.area_dict.items():
                    if categoria in value:
                        area_curso = key
                        requisitos = area_curso.split(' - ')[1]
                        insertDB(connection=connectDB(), tabela='trabalho', fields=self.fields, values=[titulo, descricao, requisitos, remuneracao, localizacao, modo, area_curso, self.provenance_statement_id])
