import re
import os
import json
import configparser

class Page():
	template_filename = ""
	result_filename = ""
	template = ""
	template_params = {}

	def build(self) -> str:
		with open(self.template_filename, "r") as temp:
			self.template = temp.read()

		result = self.template

		for param in self.template_params.keys():
			result = re.sub(f"@/ {param} /@", self.template_params[param], result)

		result = self.process_includes(result)

		return result

	def process_includes(self, result):
		imports = re.findall("@/ include .* /@", result)
		split = re.split("@/ include .* /@", result)
		for imp in imports:
			values = re.findall("'[^']*=[^']*'", result)

			# clean values of the single quotes and save into dict
			params = {}
			for val in values:
				val = val.replace("'", "")
				val = val.split("=")
				params[val[0]] = val[1]

			if "file" not in params:
				print(f"Error in: {imp}, file parameter is missing!")

			res = Import(filename=params["file"], **params).result
			matc = re.search("@/ include .* /@", result)
			span = matc.span()
			result = result[0:span[0]] + res + result[span[1]:len(result)]
		return result

	def set_template(self, template:str) -> None:
		self.template_filename = template

	def set_params(self, **kwargs) -> None:
		self.template_params = kwargs

	def set_result_filename(self, filename):
		self.result_filename = filename

class Import(Page):
	def __init__(self, filename:str, **kwargs) -> str:
		self.template_filename = filename
		self.template_params = kwargs
		self.result = self.build()

class Chunk():
	template_filename = ""
	result_extensions = ".html"
	result_folder = os.getcwd
	items = {}

	def build(self):
		for item in self.items.keys():
			newpage = Page()
			newpage.template_filename = self.template_filename
			newpage.template_params = self.items[item]
			newpage.result_filename = os.path.join(self.result_folder, item, self.result_extensions)
			newpage.build()

class FileFolderChunk(Chunk):
	@classmethod
	def load_with_ini(cls, folder):
		files = os.listdir(folder)
		ini_files = []

		for file in files:
			if re.fullmatch(".*[.]ini", file) != None:
				ini_files.append(file)

		for file in ini_files:
			config = configparser.ConfigParser()
			config.read(file)

			items[file] = config["PARAMETERS"]

	@classmethod
	def load_with_json(cls, folder):
		files = os.listdir(folder)
		json_files = []

		for file in files:
			if re.fullmatch(".*[.]json", file) != None:
				json_files.append(file)

		for file in json_files:
			with open(file, "r") as fl:
				content = json.loads(fl.read())

			self.items[file] = content

class DataFileChunk():
	@classmethod
	def from_json(cls, json_string):
		pass

	@classmethod
	def from_json_file(cls, filename):
		pass

class Website():
	pages = []
	output_folder = os.getcwd()

	def build(self) -> list:
		generated_files = []

		if os.path.isdir(self.output_folder) == False:
			os.mkdir(self.output_folder)

		for page in self.pages:
			result = page.build()

			with open(os.path.join(self.output_folder, page.result_filename), "w") as file:
				file.write(result)

			generated_files.append(page.result_filename)

		return generated_files

	def set_output_folder(self, folder:str):
		self.output_folder = folder

	def add_page(self, page:Page):
		self.pages.append(page)
