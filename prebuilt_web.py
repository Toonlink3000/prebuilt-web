import re

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

		return result

	def set_template(self, template:str) -> None:
		self.template_filename = template

	def set_params(self, **kwargs) -> None:
		self.template_params = kwargs

	def set_result_filename(self, filename):
		self.result_filename = filename

class BuildWeb():
	pages = []
	output_folder = ""

	def build(self) -> list:
		generated_files = []
		for page in self.pages:
			result = page.build()

			with open(page.result_filename, "w") as file:
				file.write(result)

			generated_files.append(page.result_filename)

		return generated_files

	def set_output_folder(self, folder:str):
		self.output_folder = folder

	def add_page(self, page:Page):
		self.pages.append(page)


