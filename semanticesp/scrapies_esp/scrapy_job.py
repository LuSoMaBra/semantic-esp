import datetime
import scrapy
from db_tools import *


def create_start_urls():
    # este link está configurado para buscar ofertas de trabalho full time adicionadas nos últimos 7 dias (padrão indeed.com)
    # link_base = 'https://pt.indeed.com/ofertas?q={}&l=Portugal&jt=fulltime&fromage=7'

    areas = selectDB(connectDB(), 'select area from perfil_curso')

    start_urls = []
    for x in areas:
        area = x[0].replace(' ', '+')
        start_urls.append(link_base.format(area))
    return start_urls


class INDEEDSpider(scrapy.Spider):
    name = "INDEED_spider"

    # start_urls = create_start_urls()
    # start_urls = ['https://www.net-empregos.com/pesquisa-empregos.asp?chaves=&cidade=&categoria=9&zona=0&tipo=1']
    start_urls = ['https://www.portalemprego.pt/anuncios/contrato-full-time/pesquisa-Turismo/mostrar-50/']


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

        links_jobs = response.css('.jobs ::attr(href)')

        print('+++++++++++++++++++++', links_jobs)

        yield from response.follow_all(links_jobs, self.parse_job)

        # yield from response.follow_all(links_jobs, self.parse_job)


        # NEXT_PAGE_SELECTOR = '.pe-pagination a ::attr(href)'
        # next_page = response.css(NEXT_PAGE_SELECTOR).extract_first()
        # if next_page and next_page not in self.urls:
        #     yield scrapy.Request(
        #         response.urljoin(next_page),
        #         callback = self.parse
        #     )


    def parse_job(self, response):

        def extract_with_css(response, query):
            return response.css(query).extract_first(default='')

        def extract_list_with_css(response, query):
            return response.css(query)

        # titulo = extract_with_css('script ::text')

        # print('============================job:', titulo, '======================')

        dados_job = extract_list_with_css(response, 'section')

        title = extract_with_css(dados_job[0], '.row h1 ::text') #.replace('<br>', '').replace('</div>', '').replace('<div class="col-xs-12 col-md-8">', '')
        print('title============', title)

        # if title != 'Empresa de referência mundial no setor do Vinícola com projetos inovadores em Enoturismo. (m/f)': return

        job_details = extract_list_with_css(dados_job[1], '.row .col-sm-8 ::text').getall()
        job_requisitos = extract_list_with_css(dados_job[1], 'li ::text').getall()

        descricao = ''
        localizacao = ''
        modo = ''
        for x in range(len(job_details)):
            if x > 1:
                current = job_details[x].replace('\n', '').lstrip()
                if (len(current) > 0):
                    if 'Distrito' in current:
                        localizacao = job_details[x + 2].replace('\n', '').lstrip()
                    elif 'Tipo de contrato' in current:
                        modo = job_details[x + 2].replace('\n', '').lstrip()
                        break
                    else:
                        descricao = descricao + current + '\n'

        print(descricao)

        requisitos = 'Vide descrição'
        remuneracao = 'Não informada'

        # for x in range(len(job_details)):
        #     print('xxxxxxx', x, ': ', job_details[x])
        #


        print(title)
        print(descricao)
        print(requisitos)
        print(remuneracao)
        print(localizacao)
        print(modo)





        # print('.cssssssss===', descricao[0].css('h4 ::text').extract_first(default='***'))
            # print(x.css('::text').extract_first(default=''))

        # pega perfil
        # job_details_list = extract_list_with_css(job_details[0], 'li')
        # requisitos = ''
        # for x in job_details_list:
        #     requisitos = requisitos + x.css('.c1 ::text').extract_first(default='') + '\n'
            # print(x.css('.c1 ::text').extract_first(default=''))

        # print('job_details============', extract_list_with_css(job_details[0], 'ul '))
        # descricao = dados_job[0].css('title').extract_first(default='').replace('<br>', '').replace('</div>', '').replace('<div class="col-xs-12 col-md-8">', '')
        # remuneracao = dados_job[2].css('div .col-xs-12').extract_first(default='').replace('<br>', '').replace('</div>', '').replace('<div class="col-xs-12 col-md-8">', '').split(' <a ')[0]
        # localizacao = dados_job[2].css('div .col-xs-12').extract_first(default='').replace('<br>', '').replace('</div>', '').replace('<div class="col-xs-12 col-md-8">', '').split(' <a ')[0]
        # modo = dados_job[5].css('div .col-xs-12').extract_first(default='').replace('<br>', '').replace('</div>', '').replace('<div class="col-xs-12 col-md-8">', '')
        #
        # values = [
        #     titulo,
        #     descricao,
        #     requisitos,
        #     remuneracao,
        #     localizacao,
        #     modo,
        #     self.data_raspagem
        # ]
        #
        # insertDB(connection=connectDB(), tabela='perfil_trabalho', fields=self.fields, values=values)


        # for x in dados_job:
        #     # print('==========', x)
        #     print(x.css('p').get() )#.replace('\n', '').replace('\t', ''),)

        # valor_anual_nacional = extract_with_css('.author-description::text')
        # valor_anual_internacional = extract_with_css('.author-description::text')
        # duracao = extract_with_css('.author-description::text')
        # modo = extract_with_css('.author-description::text')


        # result_scrappy.append([url, nome, qualificacao, descricao, area, campo_estudo, duracao, modo])

