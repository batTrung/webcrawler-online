import os
import asyncio
import aiohttp
import shutil
import re
from collections import namedtuple
from urllib.parse import urlparse, urlsplit, urljoin
from celery.task.control import revoke
import requests
from django.conf import settings
from .models import File

my_headers = {
	'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)\
				AppleWebKit/537.36 ' + ' (KHTML, like Gecko)\
				Chrome/61.0.3163.100 Safari/537.36'
}


re_static = re.compile(r'([^\s|\'|\"|\(]+(\.png|\.bmp|\.svg|\.gif|\.json|\.css|\.js|\.jpg|\.jpeg|\.ico))')
re_html = re.compile(r'(<a[^>]+href=[\'\"](\S+)[\'\"][^>]*>)')
re_replace_href = re.compile(r'(href=[\'\"])(\S+)([\'\"])')
re_css_css = re.compile(r'@import\s*?(?:url\()?[\'\"]?(([\w\.\/]+\.css))[\'\"]?')

staticList = ('.png', '.webp', '.bmp', '.svg', '.gif', '.css', '.js', '.jpg', '.jpeg', '.ico')
imgList = ('.png', '.webp', '.bmp', '.svg', '.gif', '.jpg', '.jpeg', '.ico')

staticCSS = ('.png', '.bmp', '.svg', '.gif', '.jpg', '.jpeg',
			'.eot', '.woff2', '.woff', '.ttf', '.svg', '.css')

staticCSS2 = ('.png', '.bmp', '.svg', '.gif', '.jpg', '.jpeg',
			'.eot', '.woff2', '.woff', '.ttf', '.svg')

reStaticCSS = '(' + '|'.join(staticCSS) + '))'
re_css_static = re.compile(r'url\([\'\"]?([^\) ]+' + reStaticCSS)

re_js_static = re.compile(r'([^\s|\'|\"|\(]+(\.png|\.bmp|\.svg|\.gif|\.jpg|\.jpeg|\.ico))')


def validate_url(url):
	try:
		s = requests.Session()
		s.headers = my_headers
		s.headers.update({'Referer': url})
		r = s.get(url,
					headers=my_headers,
					timeout=15)
	except Exception as e:
		return None

	if r.status_code == 200:
		return url

	elif r.status_code == 403:
		r = requests.get(url)
		if r.status_code == 200:
			return url
	else:
		return None

def get_content(url, type_='text'):
	s = requests.Session()
	s.headers = my_headers
	s.headers.update({'Referer': url})
	try:
		r = s.get(url, timeout=15)
		if type_ == 'text':
			return r.content.decode('utf8')
		elif type_ == 'byte':
			return r.content
	except:
		return None

def isFile(path, type_):
	if type_ == 'static':
		real_path = '/'.join((settings.STATIC_PATH, path))
	elif type_ == 'html':
		real_path = '/'.join((settings.TEMP_PATH, path))
	return os.path.isfile(real_path)


def createDir(path):
	os.makedirs(os.path.dirname(path),\
						exist_ok=True)

	
def clean(link, fo, type_=None, path_js=None):
	result = None
	Result = namedtuple('Result', 'link path url rep')

	if link.startswith('http'):
		path = urlparse(link).path.strip('/')
		url = link
		rep = get_link(fo, path)
		if (urlparse(fo.url).netloc \
				in urlparse(link).netloc)\
				or type_=='static':
			result =  Result(link, path, url, rep)

	elif link.startswith('//'):
		rep = 'http:' + link
		url = 'http:' + link
		if (urlparse(fo.url).netloc \
				in urlparse(url).netloc)\
				or type_=='static':
			path = urlparse(url).path.strip('/')
			rep = get_link(fo, path)
			result =  Result(link, path, url, rep)

	elif link.startswith('/'):
		url = urljoin(fo.url, link)
		path = link.strip('/')
		rep = get_link(fo, path)
		result =  Result(link, path, url, rep)

	elif link and link[0].isalpha():
		if path_js:
			path_split = urlsplit(path_js[1])
		else:
			path_split = urlsplit(fo.url)

		x_path = path_split.path
		ps = x_path.split('.')
		if len(ps) > 1:
			x_path = ps[0].rsplit('/', 1)[0]

		new_url = path_split.scheme + '://' \
					+ path_split.netloc + x_path \
					+ '/'

		url = urljoin(new_url, link)
		if path_js:
			path = get_path(path_js[0], link)
		else:
			path = get_path(fo.path, link)
		rep = link
		result =  Result(link, path, url, rep)

	elif link.startswith('../'):
		url = urljoin(fo.url, link)
		if len(fo.path.split('/')) == 2:
			path = link.strip('../')
			rep = path
		else:
			url_path = 'http://xx.com/' + fo.path
			new_url = urljoin(url_path, link)
			path = urlparse(new_url).path.strip('/')
			path = path.split('/', 1)[1]
			rep = link
		result =  Result(link, path, url, rep)

	if result:
		if validate_url(result.url):
			result = result._replace(path = os.path.normpath(path))
			result = result._replace(rep = os.path.normpath(rep))
			return result

	return None

def clean_static(link, fo, type_, path_js=None):
	return clean(link, fo, type_, path_js)


def clean_html(link, fo):
	item =  clean(link, fo)
	if item:
		item = item._replace(path = add_html(fo, item.path))
		item = item._replace(rep = add_html(fo, item.rep))
	
	return item

def add_html(fo, path):
	if path and (not path.endswith(('.html', '.php'))):
		path = urlparse(path).path.strip('/')
		if path:
			xstrip = path.rsplit('/', 1)
			start = xstrip[0]
			if len(xstrip) == 2:
				end = xstrip[1]
				pattern = re.compile('[^a-zA-Z0-9]')
				end = pattern.sub('-', end).strip('-')
				end = end + '.html'
				path = start + '/' + end
			else:
				path = start + '.html'
		else:
			path = 'index.html'
		if path == '..html':
			path = 'index.html'

	return path


def get_link(fo, path):
	x_split = fo.path.split('/')
	num = len(x_split) - 2
	rep = '../'*num + path

	return rep


def get_path(path, link):
	xr = path.split('/')
	if len(xr) < 3:
		path = link
	else:
		path = '/'.join(xr[1:-1] + [link])

	return path


def folder_size(path):
	total = 0
	for entry in os.scandir(path):
		if entry.is_file():
			total += entry.stat().st_size
		elif entry.is_dir():
			total += folder_size(entry.path)
	
	return total


def get_size_item(item):
	static_size_by_bytes = 0
	temp_size_by_bytes = 0

	static_path = '/'.join((settings.STATIC_PATH, item.item.slug))
	temp_path = '/'.join((settings.TEMP_PATH, item.item.slug))
	
	if os.path.isdir(static_path):
		static_size_by_bytes = folder_size(static_path)/10**6
	if os.path.isdir(temp_path):
		temp_size_by_bytes = folder_size(temp_path)/10**6
		
	return static_size_by_bytes + temp_size_by_bytes


def save_file(fo_id, text=None, item=None):

	try:
		fo = File.objects.get(id = fo_id)
		createDir(fo.root_path())

		if fo.path.endswith(staticCSS2):
			byte = get_content(fo.url, 'byte')
			if byte:
				try:
					with open(fo.root_path(), 'wb+') as f:
						f.write(byte)
				except:
					pass
		else:
			if text is None:
				text = get_content(fo.url, 'text')
				if text:
					fo.content = text
					fo.save()
			if text:
				try:
					with open(fo.root_path(), 'w') as f:
						f.write(text)
				except:
					pass

	except File.DoesNotExist:
		pass

def replace_path(text, item):
	if item:
		rep = '/'.join(('/static/websites', item.path))
		text = text.replace(item.link, rep)

	return text

def replace_rep(text, item):
	if item:
		text = text.replace(item.link, item.rep)

	return text

def replace_path_html(text, item):
	if item:
		text = text.replace(item.a_link, item.a_path)

	return text

def replace_rep_html(text, item):
	if item:
		text = text.replace(item.a_link, item.a_rep)

	return text

def clean_dirs():
	for dir in os.listdir(settings.TEMP_PATH):
		dir = '/'.join((settings.TEMP_PATH, dir))
		if os.path.isdir(dir):
			shutil.rmtree(dir)
	for dir in os.listdir(settings.STATIC_PATH):
		dir = '/'.join((settings.STATIC_PATH, dir))
		if os.path.isdir(dir):
			shutil.rmtree(dir)


def get_set_path(results):
	reps = []
	for item in results:
		if item:
			if item.path not in reps:
				yield item
			reps.append(item.path)

def get_set_rep(results):
	reps = []
	for item in results:
		if item:
			if item.rep not in reps:
				yield item
			reps.append(item.rep)

def get_set_html(results):
	reps = []
	links = set()
	for item in results:
		if item:
			if item.a_link not in links:
				reps.append(item)
				links.add(item.a_link)
	return reps

def clear_dirs(slug):
	temp_path = '/'.join((settings.TEMP_PATH, slug))
	if os.path.isdir(temp_path):
		shutil.rmtree(temp_path)
	static_path = '/'.join((settings.STATIC_PATH, slug))
	if os.path.isdir(static_path):
		shutil.rmtree(static_path)
	