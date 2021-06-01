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

    fields = [
        'titulo',
        'descricao',
        'requisitos',
        'remuneracao',
        'localizacao',
        'modo',
        'data_raspagem'
    ]

    # link base: "Formação Superior", "Tempo Integral"
    link_base = 'https://www.net-empregos.com/pesquisa-empregos.asp?chaves=Forma%E7%E3o+Superior&cidade=&categoria={}&zona=0&tipo=1'

    areas = selectDB(connectDB(), 'select area from perfil_curso')

    start_urls = []
    all_areas_list = []
    for x in areas:
        y = x[0].split(' ')
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

        print('+++++++++++++++++++++', links_jobs)

        # for link in links_jobs:
        #     scrapy.Request(url=link, callback=self.parse_job)

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

        # x = '<option value=0>( Todas as Categorias )</option><option value=29>Administração / Secretariado</option><option value=39>Agricultura / Florestas / Pescas</option><option value=22>Arquitectura / Design</option><option value=40>Artes / Entretenimento / Media</option><option value=16>Banca / Seguros / Serviços Financeiros</option><option value=47>Beleza / Moda / Bem Estar</option><option value=57>Call Center / Help Desk</option><option value=53>Comercial / Vendas</option><option value=8>Comunicação Social / Media</option><option value=51>Conservação / Manutenção / Técnica</option><option value=23>Construção Civil</option><option value=15>Contabilidade / Finanças</option><option value=28>Desporto / Ginásios</option><option value=44>Direito / Justiça</option><option value=11>Educação / Formação</option><option value=54>Engenharia ( Ambiente )</option><option value=45>Engenharia ( Civil )</option><option value=46>Engenharia ( Eletrotecnica )</option><option value=24>Engenharia ( Mecanica )</option><option value=50>Engenharia ( Química / Biologia )</option><option value=41>Farmácia / Biotecnologia</option><option value=26>Gestão de Empresas / Economia</option><option value=32>Gestão RH</option><option value=9>Hotelaria / Turismo</option><option value=12>Imobiliário</option><option value=6>Indústria / Produção</option><option value=38>Informática ( Analise de Sistemas )</option><option value=34>Informática ( Formação )</option><option value=37>Informática ( Gestão de Redes )</option><option value=35>Informática ( Internet )</option><option value=36>Informática ( Multimedia )</option><option value=5>Informática ( Programação )</option><option value=49>Informática ( Técnico de Hardware )</option><option value=56>Informática (Comercial/Gestor de Conta)</option><option value=58>Limpezas / Domésticas</option><option value=30>Lojas / Comércio / Balcão</option><option value=19>Publicidade / Marketing</option><option value=18>Relações Públicas</option><option value=42>Restauração / Bares / Pastelarias</option><option value=14>Saúde / Medicina / Enfermagem</option><option value=55>Serviços Sociais</option><option value=52>Serviços Técnicos</option><option value=1>Telecomunicações</option><option value=43>Transportes / Logística</option>'
        # x = x.split('<option ')
        # option_dict = {}
        # for y in x:
        #     try:
        #         option_dict[y.split('value=')[1].split('>')[0]] = y.split('>')[1].split('<')[0]
        #     except:
        #         pass
        # print(option_dict)
        # return
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
                    descricao = descricao + k.get().lstrip().rstrip() + ' '
                    # print(k.get().replace('\n', ' ').replace('\r', '').lstrip())
                    # print('          ', k.xpath('::text'))
                print(descricao)

            print('============================job:', titulo, '======================')

            localizacao = 'Veja em Descrição'
            modo = 'Veja em Descrição'

            categoria = cleanup(str(response.request.headers['Referer'].decode("utf-8")).split('categoria=')[1].split('&zona')[0].replace('+', ' '))

            remuneracao = 'Não informada'

            if titulo:
                for key, value in self.area_dict.items():
                    if categoria in value:
                        requisitos = key
                        insertDB(connection=connectDB(), tabela='perfil_trabalho', fields=self.fields, values=[titulo, descricao, requisitos, remuneracao, localizacao, modo, self.data_raspagem])




# class NETEMPREGOSpider(scrapy.Spider):
#     name = "NETEMPREGO_spider"
#
#     start_urls = create_start_urls()
#     # start_urls = ['https://www.net-empregos.com/pesquisa-empregos.asp?chaves=&cidade=&categoria=9&zona=0&tipo=1']
#
#     data_raspagem = datetime.datetime.now()
#
#     fields = [
#         'titulo',
#         'descricao',
#         'requisitos',
#         'remuneracao',
#         'localizacao',
#         'modo',
#         'data_raspagem'
#     ]
#
#     def parse(self, response):
#
#         links_jobs = response.css('.div-right a ::attr(href)')
#
#         # print('+++++++++++++++++++++', links_jobs)
#
#         # for link in links_jobs:
#         #     scrapy.Request(url=link, callback=self.parse_job)
#
#         yield from response.follow_all(links_jobs, self.parse_job)
#
#         NEXT_PAGE_SELECTOR = 'a .page-link .d-none .d-lg-block ::attr(href)'
#         next_page = response.css(NEXT_PAGE_SELECTOR).extract_first()
#         if next_page and next_page not in self.urls:
#             yield scrapy.Request(
#                 response.urljoin(next_page),
#                 callback = self.parse
#             )
#
#
#     def parse_job(self, response):
#
#         def extract_with_css(response, query):
#             return response.css(query).extract_first(default='')
#
#         def extract_list_with_css(response, query):
#             return response.css(query)
#
#         link = extract_list_with_css(response, '.job-details-page')
#         for x in link:
#             titulo = extract_with_css(x, 'h1 ::text')
#             print('TITLE', titulo)
#             description = extract_list_with_css(x, 'p')
#             for y in description:
#                 # print(strip_tags(y))
#                 _y = extract_list_with_css(y, '::text')
#                 descricao = ''
#                 for k in _y:
#                     descricao = descricao + k.get().lstrip().rstrip() + ' '
#                     # print(k.get().replace('\n', ' ').replace('\r', '').lstrip())
#                     # print('          ', k.xpath('::text'))
#                 print(descricao)
#
#             print('============================job:', titulo, '======================')
#
#             localizacao = 'Veja em Descrição'
#             modo = 'Veja em Descrição'
#
#             requisitos = cleanup(str(response.request.headers['Referer'].decode("utf-8")).split('chaves=')[1].split('&cidade')[0].replace('+', ' '))
#
#             remuneracao = 'Não informada'
#
#             print(titulo)
#             print(descricao)
#             print('99999999999999999', requisitos)
#             print(remuneracao)
#             print(localizacao)
#             print(modo)
#
#             values = [
#                 titulo,
#                 descricao,
#                 requisitos,
#                 remuneracao,
#                 localizacao,
#                 modo,
#                 self.data_raspagem
#             ]
#
#             if titulo:
#                 insertDB(connection=connectDB(), tabela='perfil_trabalho', fields=self.fields, values=values)
