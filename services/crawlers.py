import os
import re
import asyncio
import time
from lxml import html
import aiohttp
from bs4 import BeautifulSoup
from functools import partial
from threading import Thread
from multiprocessing import Pool
from functools import reduce
from collections import namedtuple
from django.shortcuts import get_object_or_404
from .models import File, Item
from .clean import get_content, \
					isFile, createDir, \
					save_file, \
					replace_path, \
					replace_path_html, \
					replace_rep_html, \
					get_set_path, \
					get_set_rep, \
					get_set_html, \
					replace_rep
from .clean import re_static, \
					re_html, \
					re_replace_href
from .clean import clean_static, \
					clean_html, \
					re_css_static, \
					re_js_static, \
					re_css_css


class Crawler():

	def __init__(self, item, task_id):
		self.item = item
		self.task_id = task_id

	def get_html_links(self, fo, text):
		print(f"============ FIND HTMLs ============")
		links = re_html.findall(text)
		if len(links) > 0:
			loop = asyncio.new_event_loop()
			results = loop.run_until_complete(self.async_html(loop, links, fo))
			paths = results
			reps = results
			text_path = reduce(replace_path_html, paths, text)
			text_rep = reduce(replace_rep_html, reps, fo.content)
			save_file(fo.id, text_path, self)
			fo.content = text_rep
			fo.save()
			loop.close()

			return paths

		print(f"============ END FIND HTMLs ============\n")

	async def async_html(self, loop, links, fo):
		futures = [asyncio.ensure_future(self.fetch_html(loop, link, fo)) for link in links]
		results = await asyncio.gather(*futures)
		return results
	
	async def fetch_html(self, loop, link, fo):
		return await loop.run_in_executor(None, self.get_item_html, link, fo)

	def get_item_html(self, link, fo):
		href = link[1]
		link = link[0]
		item = clean_html(href, fo)
		if item:
			item = item._replace(path = '/'.join((self.item.slug,
													item.path)))
			path = item.path
			newFile = None
			if not isFile(path, 'html'):
				try:
					newFile = File(
							path = path,
							url = item.url,
							category = 'html',
							item = self.item)
				
					newFile.save()
					save_file(newFile.id, None, self)
					x_path = path.split('/', 1)[1]
					print(f"SAVE: {x_path}")
				except:
					pass
			Result = namedtuple('Result', 'a_link a_path a_rep html_file')
			a_link = link
			x_path = '/'.join(('/demo', path))
			a_path = re_replace_href.sub(r'\g<1>' + x_path + r'\g<3>', link)
			a_rep = re_replace_href.sub(r'\g<1>' + item.rep + r'\g<3>', link)

			return Result(a_link, a_path, a_rep, newFile)

	def get_static_links(self, fo, text):
		# try:
		# 	fo = File.objects.get(id=fo_id)
		# except File.DoesNotExist:
		# 	print("not exitsssssssssssssssssssssssssssssssssssssss")
		# 	fo = File(id=fo_id)

		print(f"============ FIND CSS + JS + IMG ============")
		links = re_static.findall(text)
		if len(links) > 0:
			loop = asyncio.new_event_loop()
			results = loop.run_until_complete(self.async_html_statics(loop, links, fo))
			paths = get_set_path(results)
			reps = get_set_rep(results)
			text_path = reduce(replace_path, paths, text)
			text_rep = reduce(replace_rep, reps, text)
			with open('text_rep.html', 'w') as f:
				f.write(text_rep)
			save_file(fo.id, text_path, self)
			fo.content = text_rep
			print(fo.path)
			print(fo.item)
			fo.save()
			loop.close()
			print(f"============ END FIND CSS + JS + IMG ============\n")
			return text_path

	async def async_html_statics(self, loop, links, fo):
		futures = [asyncio.ensure_future(self.fetch_html_statics(loop, link[0], fo)) for link in links]
		results = await asyncio.gather(*futures)
		return results
	
	async def fetch_html_statics(self, loop, link, fo):
		return await loop.run_in_executor(None, self.get_item, link, fo)

	def get_item(self, link, fo, path_js=None):
		item = clean_static(link, fo, 'static', path_js)
		if item:
			item = item._replace(path = '/'.join((self.item.slug,
													item.path)))
			path = item.path
			if not isFile(path, 'static'):
				if path.endswith('.css'):
					category = 'css'
				elif path.endswith('.js'):
					category = 'js'
				elif path.endswith('.html'):
					category = 'html'
				else:
					category = 'static'

				try:
					newFile = File(
								path = path,
								url = item.url,
								category = category,
								item = self.item)
					newFile.save()
					save_file(newFile.id, None, self)

					x_path = path.split('/', 1)[1]
					print(f"SAVE: { x_path }")

				except Exception as e:
					pass
		return item

	def get_css_js_static_links(self, fo, regexList, path_js=None):
		# fo = File.objects.get(id = fo_id, item=self.item)
		text = get_content(fo.url, 'text')
		if text:
			links = []
			for regex in regexList:
				links += regex.findall(text)
			if len(links) > 0:
				loop = asyncio.new_event_loop()
				results = loop.run_until_complete(self.async_css_js_statics(loop, links, fo, path_js))
				paths = get_set_path(results)
				reps = get_set_rep(results)
				text_path = reduce(replace_path, paths, text)
				text_rep = reduce(replace_rep, reps, text)
				save_file(fo.id, text_path, self)
				fo.content = text_rep
				fo.save()
				loop.close()
				if results:
					cssFiles = [File.objects.get(path = result.path) for result in results if result and result.path.endswith('.css')]
					for file in cssFiles:
						self.get_css_js_static_links(file, [re_css_static, re_css_css])

	async def async_css_js_statics(self, loop, links, fo, path_js=None):
		futures = [asyncio.ensure_future(self.fetch_css_js_statics(loop,
																link[0],
																fo,
																path_js))
																for link in links]
		results = await asyncio.gather(*futures)
		return results
	
	async def fetch_css_js_statics(self, loop, link, fo, path_js=None):
		return await loop.run_in_executor(None, self.get_item, link, fo, path_js)

	def crawler_html(self, fo_id):
		try:
			fo = File.objects.get(id=fo_id)
		except File.DoesNotExist:
			return 
		
		print(f"============ START HTML ============")
		
		x_path = fo.path.split('/', 1)[1]
		
		print(f'#######################################')
		print(f'############ { x_path } ########################')
		print(f'######################################')
		
		text = get_content(fo.url, 'text')
		results = None
		if text:
			text = self.get_static_links(fo, text)
			self.crawler_static(type_ = 'css', regexList=[re_css_static, re_css_css])
			# Khong quet file static cua JS 
			# self.crawler_static(type_ = 'js',
			# 					regexList=[re_js_static],
			# 					path_js=(fo.path, fo.url))
			if text:
				results = self.get_html_links(fo, text)

		fo.crawled = True
		fo.save()
		if results:
			newFiles = (result.html_file for result in results if result)
			id_newFiles = (newFile.id for  newFile in newFiles if newFile and (not newFile.crawled))
			for id_file in id_newFiles:
				self.crawler_html(id_file)

		print(f"============ END HTML ============\n")

	async def async_crawler_html(self, loop, newFiles):
		futures = [asyncio.ensure_future(self.fetch_crawler_html(loop,
																newFile))
																for newFile in newFiles]
		results = await asyncio.gather(*futures)
		return results
	
	async def fetch_crawler_html(self, loop, file_id):
		return await loop.run_in_executor(None, self.crawler_html, loop, file_id)

	def crawler_static(self, type_, regexList, path_js=None):
		
		print(f"============ CRAWLER CSS +JS ============")
		
		files = self.item.files.filter(category=type_, crawled=False)
		if len(files) > 0:
			for file in files:
				self.get_css_js_static_links(file, regexList, path_js)
						
		files.update(crawled=True)
		
		print(f"============ END CRAWLER CSS +JS ============\n")

	def main(self):
		
		print('=============== INDEX =============')
		
		index_path = '/'.join((self.item.slug, 'index.html'))
		index = File(
			path = index_path,
			url = self.item.url,
			category = 'html',
			root = True,
			item = self.item)
		index.save()
		save_file(index.id, None, self)

		print('=============== START =============')

		self.crawler_html(index.id)

		print('=============== END ===============')
