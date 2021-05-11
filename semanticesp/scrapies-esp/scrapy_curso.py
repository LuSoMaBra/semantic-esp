import scrapy

class UTADSpider(scrapy.Spider):
    name = "UTAD_spider"
    start_urls = ['https://www.utad.pt/estudar/inicio/licenciaturas-mestrados-integrados/']
    urls = []

    def parse(self, response):

        self.urls.append(response.url)

        SET_SELECTOR = '.rowlist'
        for curso in response.css(SET_SELECTOR):
            NOME_SELECTOR = 'li a ::text'
            LINK_SELECTOR = 'li a ::attr(href)'
            yield {
                'nome': curso.css(NOME_SELECTOR).extract_first().replace('\n', '').replace('\t', ''),
                'link': curso.css(LINK_SELECTOR).extract_first(),
            }
            curso_parsed = parse_curso(self, response)  PAREI AQUI
            # print(curso.css(NOME_SELECTOR).extract_first().replace('\n', '').replace('\t', ''))

        NEXT_PAGE_SELECTOR = '.pe-pagination a ::attr(href)'
        next_page = response.css(NEXT_PAGE_SELECTOR).extract_first()
        if next_page and next_page not in self.urls:
            yield scrapy.Request(
                response.urljoin(next_page),
                callback = self.parse
            )

        self.logger.info('A response from %s just arrived!', response.url)


    def parse_curso(self, response):

        self.urls.append(response.url)
