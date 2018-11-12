import scrapy
from scrapy import Spider, Request, Selector
from bs4 import BeautifulSoup
from dateparser import parse

class QuotesSpider(Spider):

    name = "quotes"
    # allowed_domains = ['https://www.urbandictionary.com/']
    full_result = []
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
      # for page_number in range(2, int(link[len(link) - 1]) + 1):
      #   word_url = response.meta['str_main_url'] + '&page=%d'%page_number
      #   yield Request(url = word_url, callback = self.parse_page)
    
    def parse_page(self, response):
      allowed_domains = "https://www.urbandictionary.com"
      one_word = response.xpath('//*[@id="columnist"]/ul/li/a')
      for word in one_word:
        word_url = word.xpath('@href').extract()
        request = Request(url = allowed_domains + word_url[0], callback = self.parse_word)
        request.meta['word'] = word.xpath('text()').extract()
        yield request

    def parse_word (self, response):
      result = {}
      word = response.meta['word']
      word_simple_name= response.xpath('//*[@id="content"]/div[1]/div[2]/a/text()').extract_first()
      word_definitions = response.xpath('//*[@id="content"]/div[@class="def-panel"]')
      full_information = {}
      full_information[word_simple_name] = {}
      for definition in word_definitions:
        full_information[word_simple_name]['meaning'] = BeautifulSoup(definition.xpath('div[@class="meaning"]').extract()[0], 'lxml').text
        full_information[word_simple_name]['example'] = BeautifulSoup(definition.xpath('div[@class="example"]').extract()[0], 'lxml').text
        full_information[word_simple_name]['author'] = BeautifulSoup(definition.xpath('div[@class="contributor"]').extract()[0], 'lxml').text
        date = BeautifulSoup(definition.xpath('div[@class="contributor"]').extract()[2: ], 'lxml').text
        date_str = ''
        for i in date:
          date_str += ' ' +  i
        full_information[word_simple_name]['date'] = parse(date_str)
        full_information[word_simple_name]['likes'] = definition.xpath('div[@class="def-footer"]//div/div/div/div/a[@class="up"]/span/text()').extract_first()
        full_information[word_simple_name]['dislikes'] = definition.xpath('div[@class="def-footer"]//div/div/div/div/a[@class="down"]/span/text()').extract_first()
      
      result[word] = full_information
      request = Request(url = response, callback = self.parse_latter)
      request.meta['result'] = result
      yield request

    def ending_parsing (self, response):
      self.full_result.append(response.meta['result'])
      print('!!!!!!!!!!!!!!!!!!!!', response.meta['result'])
    
    print('!!!!!!!!!!!!!!!!!!!!', full_result)


