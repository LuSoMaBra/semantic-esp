import datetime
import scrapy
from db_tools import *

class UTADSpider(scrapy.Spider):
    name = "UTAD_spider"
    start_urls = ['https://www.utad.pt/estudar/inicio/licenciaturas-mestrados-integrados/', 'https://www.utad.pt/estudar/inicio/licenciaturas-mestrados-integrados/page/2/']
    mask_university = '12'  # important - colocado manualmente após a importação dos dados abertos do governo (primeiros 2 dígitos do código da instituição)
    provenance_statement_id = 9 # important - definido quando da programação do código da UTAD
    valor_propina_nacional = 697
    valor_propina_internacional = 1500
    data_raspagem = datetime.datetime.now()

    fields = [
        'url',
        'descricao',
        'valor_propina_nacional',
        'valor_propina_internacional',
        'duracao',
        'modo',
        'curso_cnaef_id',
        'provenance_statement_id'
    ]

    def parse(self, response):
        links_cursos = response.css('.linklist ::attr(href)')
        yield from response.follow_all(links_cursos, self.parse_curso)

    def parse_curso(self, response):

        def extract_with_css(query):
            return response.css(query).get(default='').strip()

        def extract_list_with_css(query):
            return response.css(query)

        nome = extract_with_css('h1.entry-title ::text')
        dados_curso = extract_list_with_css('.pe-tabs .row')
        url = response.url
        # qualificacao = dados_curso[0].css('div .col-xs-12').extract_first(default='').replace('<br>', '').replace('</div>', '').replace('<div class="col-xs-12 col-md-8">', '')
        descricao = dados_curso[1].css('div .col-xs-12').extract_first(default='').replace('<br>', '').replace('</div>', '').replace('<div class="col-xs-12 col-md-8">', '')
        area_curso = dados_curso[2].css('div .col-xs-12').extract_first(default='').replace('<br>', '').replace('</div>', '').replace('<div class="col-xs-12 col-md-8">', '').split(' <a ')[0].split('(')[0]
        # campo_estudo = dados_curso[2].css('div .col-xs-12').extract_first(default='').replace('<br>', '').replace('</div>', '').replace('<div class="col-xs-12 col-md-8">', '').split(' <a ')[0]
        duracao = dados_curso[6].css('div .col-xs-12').extract_first(default='').replace('<br>', '').replace('</div>', '').replace('<div class="col-xs-12 col-md-8">', '')
        modo = dados_curso[5].css('div .col-xs-12').extract_first(default='').replace('<br>', '').replace('</div>', '').replace('<div class="col-xs-12 col-md-8">', '')

        curso_cnaef_id = selectDB(connectDB(),
                                  "select id from curso_cnaef where estabelecimento like '{}__' and nome like '____ - {}' and niveldeformacao like 'Licenciatura%' ".format(
                                      self.mask_university, nome))
        print(nome, curso_cnaef_id)

        if curso_cnaef_id:
            deleteDB(connectDB(), tabela='curso', criterio = "curso_cnaef_id = {}".format(curso_cnaef_id[0][0]))
            values = [
                url,
                descricao,
                self.valor_propina_nacional,
                self.valor_propina_internacional,
                duracao,
                modo,
                curso_cnaef_id[0][0],
                self.provenance_statement_id,
            ]
            insertDB(connection=connectDB(), tabela='curso', fields=self.fields, values=values)


