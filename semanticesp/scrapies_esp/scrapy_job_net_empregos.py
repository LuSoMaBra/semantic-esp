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

def create_start_urls():
    link_base = 'https://www.net-empregos.com/pesquisa-empregos.asp?chaves={}&cidade=&categoria=0&zona=0&tipo=1'

    areas = selectDB(connectDB(), 'select area from perfil_curso')

    start_urls = []
    for x in areas:
        area = x[0].replace(' ', '+')
        start_urls.append(link_base.format(area))
    return start_urls


class NETEMPREGOSpider(scrapy.Spider):
    name = "NETEMPREGO_spider"

    start_urls = create_start_urls()
    # start_urls = ['https://www.net-empregos.com/pesquisa-empregos.asp?chaves=&cidade=&categoria=9&zona=0&tipo=1']

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

    def parse(self, response):

        links_jobs = response.css('.div-right a ::attr(href)')

        # print('+++++++++++++++++++++', links_jobs)

        # for link in links_jobs:
        #     scrapy.Request(url=link, callback=self.parse_job)

        yield from response.follow_all(links_jobs, self.parse_job)

        NEXT_PAGE_SELECTOR = 'a .page-link .d-none .d-lg-block ::attr(href)'
        next_page = response.css(NEXT_PAGE_SELECTOR).extract_first()
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
                    descricao = descricao + k.get().lstrip().rstrip() + ' '
                    # print(k.get().replace('\n', ' ').replace('\r', '').lstrip())
                    # print('          ', k.xpath('::text'))
                print(descricao)

            print('============================job:', titulo, '======================')

            localizacao = 'Veja em Descrição'
            modo = 'Veja em Descrição'

            requisitos = cleanup(str(response.request.headers['Referer'].decode("utf-8")).split('chaves=')[1].split('&cidade')[0].replace('+', ' '))

            remuneracao = 'Não informada'

            print(titulo)
            print(descricao)
            print('99999999999999999', requisitos)
            print(remuneracao)
            print(localizacao)
            print(modo)

            values = [
                titulo,
                descricao,
                requisitos,
                remuneracao,
                localizacao,
                modo,
                self.data_raspagem
            ]

            if titulo:
                insertDB(connection=connectDB(), tabela='perfil_trabalho', fields=self.fields, values=values)
