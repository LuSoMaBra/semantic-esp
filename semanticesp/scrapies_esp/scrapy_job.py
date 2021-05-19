import datetime
import scrapy
from db_tools import *


def create_start_urls():
    # este link está configurado para buscar ofertas de trabalho full time adicionadas nos últimos 7 dias (padrão indeed.com)
    link_base = 'https://pt.indeed.com/ofertas?q={}&l=Portugal&jt=fulltime&fromage=7'

    areas = selectDB(connectDB(), 'select area from perfil_curso')

    start_urls = []
    for x in areas:
        area = x[0].replace(' ', '+')
        start_urls.append(link_base.format(area))
    return start_urls


class INDEEDSpider(scrapy.Spider):
    name = "INDEED_spider"

    start_urls = create_start_urls()

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

        links_jobs = response.css('.title ::attr(href)')

        print(links_jobs)

        # yield from response.follow_all(links_jobs, self.parse_job)


        # NEXT_PAGE_SELECTOR = '.pe-pagination a ::attr(href)'
        # next_page = response.css(NEXT_PAGE_SELECTOR).extract_first()
        # if next_page and next_page not in self.urls:
        #     yield scrapy.Request(
        #         response.urljoin(next_page),
        #         callback = self.parse
        #     )


    def parse_job(self, response):

        def extract_with_css(query):
            return response.css(query).get(default='').strip()

        def extract_list_with_css(query):
            return response.css(query)

        titulo = extract_with_css('h1.entry-title ::text')

        print('============================job:', titulo, '======================')

        dados_job = extract_list_with_css('.pe-tabs .row')

        descricao = dados_job[0].css('div .col-xs-12').extract_first(default='').replace('<br>', '').replace('</div>', '').replace('<div class="col-xs-12 col-md-8">', '')
        requisitos = dados_job[1].css('div .col-xs-12').extract_first(default='').replace('<br>', '').replace('</div>', '').replace('<div class="col-xs-12 col-md-8">', '')
        remuneracao = dados_job[2].css('div .col-xs-12').extract_first(default='').replace('<br>', '').replace('</div>', '').replace('<div class="col-xs-12 col-md-8">', '').split(' <a ')[0]
        localizacao = dados_job[2].css('div .col-xs-12').extract_first(default='').replace('<br>', '').replace('</div>', '').replace('<div class="col-xs-12 col-md-8">', '').split(' <a ')[0]
        modo = dados_job[5].css('div .col-xs-12').extract_first(default='').replace('<br>', '').replace('</div>', '').replace('<div class="col-xs-12 col-md-8">', '')

        values = [
            titulo,
            descricao,
            requisitos,
            remuneracao,
            localizacao,
            modo,
            self.data_raspagem
        ]

        insertDB(connection=connectDB(), tabela='perfil_trabalho', fields=self.fields, values=values)

        # for x in dados_job:
        #     print(x.css('div').get() )#.replace('\n', '').replace('\t', ''),)

        # valor_anual_nacional = extract_with_css('.author-description::text')
        # valor_anual_internacional = extract_with_css('.author-description::text')
        # duracao = extract_with_css('.author-description::text')
        # modo = extract_with_css('.author-description::text')


        # result_scrappy.append([url, nome, qualificacao, descricao, area, campo_estudo, duracao, modo])

