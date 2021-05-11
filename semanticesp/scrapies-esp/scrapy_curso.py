import scrapy

class UTADSpider(scrapy.Spider):
    name = "UTAD_spider"
    start_urls = ['https://www.utad.pt/estudar/inicio/licenciaturas-mestrados-integrados/']

    def parse(self, response):
        SET_SELECTOR = '.rowlist'
        for curso in response.css(SET_SELECTOR):
            NOME_SELECTOR = 'li a ::text'
            LINK_SELECTOR = 'li a ::attr(href)'
            # yield {
            #     'nome': curso.css(NOME_SELECTOR).extract_first().replace('\n', '').replace('\t', ''),
            #     'link': curso.css(LINK_SELECTOR).extract_first(),
            # }
            print(curso.css(NOME_SELECTOR).extract_first().replace('\n', '').replace('\t', ''))

        NEXT_PAGE_SELECTOR = '.pe-pagination a:active ::attr(href)'
        next_page = response.css(NEXT_PAGE_SELECTOR).extract_first()
        # print(next_page)
        if next_page:
            yield scrapy.Request(
                response.urljoin(next_page),
                callback=self.parse
            )
