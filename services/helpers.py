import os
from .models import File


class FileSystem():

	def __init__(self, filePath=None):
		self.children = []
		if filePath != None:
			try:
				self.name, child = filePath.split("/", 1)
				self.children.append(FileSystem(child))
			except ValueError:
				self.name = filePath

	def addChild(self, filePath):
		try:
			thisLevel, nextLevel = filePath.split("/", 1)
			try:
				if thisLevel == self.name:
					thisLevel, nextLevel = nextLevel.split("/", 1)
			except ValueError:
				self.children.append(FileSystem(nextLevel))
				return
			for child in self.children:
				if thisLevel == child.name:
					child.addChild(nextLevel)
					return
			self.children.append(FileSystem(thisLevel))
			for child in self.children:
				if thisLevel == child.name:
					child.addChild(nextLevel)
					return
		except:
			self.children.append(FileSystem(filePath))

	def getChildren(self):
		return self.children

	def printAllChildren(self, depth = -1):
		html = ''
		depth += 2
		if len(self.children) > 0:
			if self.name:
				html += "    "*depth + '<li class="is-folder">\n'
				html += "    "*(depth+1) + f"<span>{self.name}</span>\n"
				html += "    "*(depth+1) + "<ul>\n"
			for child in self.children:
				html+= child.printAllChildren(depth)
			html+= "    "*(depth+1) + "</ul>\n"
		else:
			if self.name:
				html += "    "*depth +'<li class="is-file">\n'
				html += "    "*(depth+1) + f"<span><a href=''>{self.name}</a></span>\n"
		if self.name:
			html += "    "*depth + "</li>\n"
		return html

	def makeDict(self):
		if len(self.children) > 0:
			dictionary = {self.name:[]}
			for child in self.children:
				dictionary[self.name].append(child.makeDict())
			return dictionary
		else:
			return self.name

	def __str__(self):
		return f'Children {self.children}'


def generate_tree(item):
	files =  item.files.all()
	if len(files) > 0:
		records = (file.path.split('/', 1)[1]
					for file in item.files.all())

		records = sorted(records, key=lambda path: -len(path.split('/')))
		records[0] = '/' + records[0]

		myFiles = FileSystem(records[0])
		for record in records[1:]:
			myFiles.addChild(record)
		
		return '<ul>\n' + myFiles.printAllChildren()
	return None



def get_zip_file(zip_file, item_path, slug):
	for dirname, subdirs, files in os.walk(item_path):
		path = dirname.split(slug, 1)[1].strip('/')
		for file in files:
			if path:
				zip_path = '/'.join((path, file))
			else:
				zip_path = file
			fpath = '/'.join((dirname, file))
			file_path = '/'.join((slug, zip_path))
			f = None
			try:
				f = File.objects.get(path = file_path)
			except:
				pass
			if f and f.content:
				zip_file.writestr(zip_path, f.content)
			else:
				zip_file.write(fpath, zip_path)

	return zip_file