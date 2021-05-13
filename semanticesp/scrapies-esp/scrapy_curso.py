import datetime
import scrapy
#
# class AuthorSpider(scrapy.Spider):
#     name = 'author'
#
#     start_urls = ['http://quotes.toscrape.com/']
#
#     def parse(self, response):
#         author_page_links = response.css('.author + a')
#         yield from response.follow_all(author_page_links, self.parse_author)
#
#         pagination_links = response.css('li.next a')
#         yield from response.follow_all(pagination_links, self.parse)
#
#
#     def parse_author(self, response):
#         def extract_with_css(query):
#             return response.css(query).get(default='').strip()
#
#         yield {
#             'name': extract_with_css('h3.author-title::text'),
#             'birthdate': extract_with_css('.author-born-date::text'),
#             'bio': extract_with_css('.author-description::text'),
#         }
#
#         print('========================================AUTHOR=========================================================')

class UTADSpider(scrapy.Spider):
    name = "UTAD_spider"
    start_urls = ['https://www.utad.pt/estudar/inicio/licenciaturas-mestrados-integrados/', 'https://www.utad.pt/estudar/inicio/licenciaturas-mestrados-integrados/page/2/']
    # urls = []

    def parse(self, response):

        # self.urls.append(response.url)

        # for curso in response.css('.rowlist'):
            # yield {
            #     'nome': curso.css('li a ::text').extract_first().replace('\n', '').replace('\t', ''),
            #     'link': curso.css('li a ::attr(href)').extract_first(),
            # }
        links_cursos = response.css('.linklist ::attr(href)')

        # for x in links_cursos:
        #     print(x)
        yield from response.follow_all(links_cursos, self.parse_curso)


        # NEXT_PAGE_SELECTOR = '.pe-pagination a ::attr(href)'
        # next_page = response.css(NEXT_PAGE_SELECTOR).extract_first()
        # if next_page and next_page not in self.urls:
        #     yield scrapy.Request(
        #         response.urljoin(next_page),
        #         callback = self.parse
        #     )


    def parse_curso(self, response):

        def extract_with_css(query):
            return response.css(query).get(default='').strip()

        def extract_list_with_css(query):
            return response.css(query)

        nome = extract_with_css('h1.entry-title ::text')

        if nome != 'Engenharia Informática':
            return

        print('============================CURSO:', nome, '======================')

        dados_curso = extract_list_with_css('.pe-tabs .row')

        url = response.url
        qualificacao = dados_curso[0].css('div .col-xs-12').extract_first(default='').replace('<br>', '').replace('</div>', '').replace('<div class="col-xs-12 col-md-8">', '')
        descricao = dados_curso[1].css('div .col-xs-12').extract_first(default='').replace('<br>', '').replace('</div>', '').replace('<div class="col-xs-12 col-md-8">', '')
        area = dados_curso[2].css('div .col-xs-12').extract_first(default='').replace('<br>', '').replace('</div>', '').replace('<div class="col-xs-12 col-md-8">', '').split(' <a ')[0]
        campo_estudo = dados_curso[2].css('div .col-xs-12').extract_first(default='').replace('<br>', '').replace('</div>', '').replace('<div class="col-xs-12 col-md-8">', '').split(' <a ')[0]
        duracao = dados_curso[6].css('div .col-xs-12').extract_first(default='').replace('<br>', '').replace('</div>', '').replace('<div class="col-xs-12 col-md-8">', '')
        modo = dados_curso[5].css('div .col-xs-12').extract_first(default='').replace('<br>', '').replace('</div>', '').replace('<div class="col-xs-12 col-md-8">', '')

        dados_instituicao = extract_list_with_css('.pe-tabs .row')

        # nome_instituicao
        # localizacao
        # requisitos_entrada

        # print(dados_curso[1].css('div .col-xs-12').extract_first().replace('<br>', '').replace('</div>', '').replace('<div class="col-xs-12 col-md-8">', ''))

        print('url', url)
        print('nome', nome)
        print('qualificacao', qualificacao)
        print('descricao', descricao)
        print('area', area)
        print('campo_estudo', campo_estudo)
        print('duracao', duracao)
        print('modo', modo)

        # for x in dados_curso:
        #     print(x.css('div').get() )#.replace('\n', '').replace('\t', ''),)

        # valor_anual_nacional = extract_with_css('.author-description::text')
        # valor_anual_internacional = extract_with_css('.author-description::text')
        # duracao = extract_with_css('.author-description::text')
        # modo = extract_with_css('.author-description::text')
        data_raspagem = datetime.datetime.now()



        # yield {
        #     'nome': extract_with_css('h1.entry-title::text'),
        #     'qualificacao': extract_with_css('.author-born-date::text'),
        #     'url': extract_with_css('.author-description::text'),
        #     'descricao': extract_with_css('.author-description::text'),
        #     'campo_estudo': extract_with_css('.author-description::text'),
        #     'area': extract_with_css('.author-description::text'),
        #     'valor_anual_nacional': extract_with_css('.author-description::text'),
        #     'valor_anual_internacional': extract_with_css('.author-description::text'),
        #     'duracao': extract_with_css('.author-description::text'),
        #     'modo': extract_with_css('.author-description::text'),
        #     'data_raspagem': datetime.datetime.now(),
        # }









