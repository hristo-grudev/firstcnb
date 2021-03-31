import scrapy

from scrapy.loader import ItemLoader
from w3lib.html import remove_tags

from ..items import FirstcnbItem
from itemloaders.processors import TakeFirst


class FirstcnbSpider(scrapy.Spider):
	name = 'firstcnb'
	start_urls = ['https://www.firstcnb.com/About/Unbelievably-Good-Banking/News-Notices']

	def parse(self, response):
		post_links = response.xpath('//div[@id="dnn_ctr28050_HtmlModule_lblContent"]/child::node()').getall()
		description = []
		title = ''
		date = ''
		for el in post_links:
			tag = el[1:3]

			if tag == 'h1':

				if len(description) > 1 and len(title) > 1:
					description = [p.strip() for p in description]
					description = ' '.join(description).strip()
					item = ItemLoader(item=FirstcnbItem(), response=response)
					item.default_output_processor = TakeFirst()
					item.add_value('title', title)
					item.add_value('description', description)
					item.add_value('date', date)

					yield item.load_item()

				description = []
				title = ''
				date = remove_tags(el)
			elif tag == 'h2':
				title = remove_tags(el)
			else:
				description.append(remove_tags(el))

		description = [p.strip() for p in description]
		description = ' '.join(description).strip()
		item = ItemLoader(item=FirstcnbItem(), response=response)
		item.default_output_processor = TakeFirst()
		item.add_value('title', title)
		item.add_value('description', description)
		item.add_value('date', date)

		yield item.load_item()


	def parse_post(self, response):
		title = response.xpath('//h1/text()').get()
		description = response.xpath('//text()[normalize-space()]').getall()
		description = [p.strip() for p in description]
		description = ' '.join(description).strip()
		date = response.xpath('/text()').get()

		item = ItemLoader(item=FirstcnbItem(), response=response)
		item.default_output_processor = TakeFirst()
		item.add_value('title', title)
		item.add_value('description', description)
		item.add_value('date', date)

		return item.load_item()
