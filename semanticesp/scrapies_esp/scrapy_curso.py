import datetime
import scrapy
from db_tools import *

class UTADSpider(scrapy.Spider):
    name = "UTAD_spider"
    start_urls = ['https://www.utad.pt/estudar/inicio/licenciaturas-mestrados-integrados/', 'https://www.utad.pt/estudar/inicio/licenciaturas-mestrados-integrados/page/2/']
    instituicao_id = 1  # important
    valor_anual_nacional = 697
    valor_anual_internacional = 1500
    data_raspagem = datetime.datetime.now()
    fields = [
        'instituicao_id',
        'nome',
        'qualificacao',
        'url',
        'descricao',
        'campo_estudo',
        'area_curso',
        'valor_anual_nacional',
        'valor_anual_internacional',
        'duracao',
        'modo',
        'data_raspagem'
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
        qualificacao = dados_curso[0].css('div .col-xs-12').extract_first(default='').replace('<br>', '').replace('</div>', '').replace('<div class="col-xs-12 col-md-8">', '')
        descricao = dados_curso[1].css('div .col-xs-12').extract_first(default='').replace('<br>', '').replace('</div>', '').replace('<div class="col-xs-12 col-md-8">', '')
        area_curso = dados_curso[2].css('div .col-xs-12').extract_first(default='').replace('<br>', '').replace('</div>', '').replace('<div class="col-xs-12 col-md-8">', '').split(' <a ')[0].split('(')[0]
        campo_estudo = dados_curso[2].css('div .col-xs-12').extract_first(default='').replace('<br>', '').replace('</div>', '').replace('<div class="col-xs-12 col-md-8">', '').split(' <a ')[0]
        duracao = dados_curso[6].css('div .col-xs-12').extract_first(default='').replace('<br>', '').replace('</div>', '').replace('<div class="col-xs-12 col-md-8">', '')
        modo = dados_curso[5].css('div .col-xs-12').extract_first(default='').replace('<br>', '').replace('</div>', '').replace('<div class="col-xs-12 col-md-8">', '')

        values = [
            self.instituicao_id,
            nome,
            qualificacao,
            url,
            descricao,
            campo_estudo,
            area_curso,
            self.valor_anual_nacional,
            self.valor_anual_internacional,
            duracao,
            modo,
            self.data_raspagem
        ]

        insertDB(connection=connectDB(), tabela='perfil_curso', fields=self.fields, values=values)

