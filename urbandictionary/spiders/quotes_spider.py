import scrapy
from scrapy import Spider, Request, Selector
from bs4 import BeautifulSoup

class QuotesSpider(Spider):

    name = "quotes"
    # allowed_domains = ['https://www.urbandictionary.com/']

    def start_requests(self):
      # [chr(k) for k in range(65, 91)]
        for latter in  ['A']:
          main_url = 'https://www.urbandictionary.com/browse.php?character=%s' %latter
          request = Request(url = main_url, callback = self.parse_latter)
          request.meta['str_main_url'] = main_url
          yield request
          yield Request(url = main_url, callback = self.parse_page)
    
 
    def parse_latter(self, response):
      link = str(response.xpath('//*[@id="content"]/div[2]/ul/li[8]/a/@href').extract_first()).split('=')
      for page_number in range(2, int(link[len(link) - 1]) + 1):
        word_url = response.meta['str_main_url'] + '&page=%d'%page_number
        yield Request(url = word_url, callback = self.parse_page)
    
    def parse_page(self, response):
      allowed_domains = "https://www.urbandictionary.com/"
      one_word = response.xpath('//*[@id="columnist"]/ul/li/a').extract()
      for word in one_word:
        word_url = word.xpath('/@href').extract()
        request = Request(url = allowed_domains + word_url, callback = self.parse_word)
        request.meta['word'] = word('/text()').extract()
        yield request

    def parse_word (self, response):
      word = response.meta['word']
      word_simple_name= response.xpath('//*[@id="content"]/div[1]/div[2]/a/text()').extract_first()
      word_definitions = response.xpath('//*[@id="content"]/div[@class="def-panel"]')
      print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!', word_definitions)
      full_information = {}
      for definition in word_definitions:
        full_information[word_simple_name]['meaning'] = BeautifulSoup(definition.xpath('div[@class="meaning"]').extract()[0], 'lxml').text
        full_information[word_simple_name]['example'] = BeautifulSoup(definition.xpath('div[@class="example"]').extract()[0], 'lxml').text
        'author' = BeautifulSoup(definition.xpath('div[@class="contributor"]').extract()[0], 'lxml').text.split(' ')[1]
        'date' = BeautifulSoup(definition.xpath('div[@class="contributor"]').extract()[0], 'lxml').text.split(' ')[ 2: ]
        full_information[word_simple_name]['author'] = BeautifulSoup(definition.xpath('div[@class="contributor"]').extract()[0], 'lxml').text
      # # result[word] = 
