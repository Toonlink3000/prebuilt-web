import prebuilt_web

class MyWebsite(prebuilt_web.BuildWeb):
	output_folder = "output"

class MainPage(prebuilt_web.Page):
	template_filename = "main.html"
	result_filename = "built.html"
	template_params = {
					"web_name": "My webstie"
	}

def main():
	web = MyWebsite()
	web.add_page(MainPage())
	web.build()

if __name__ == '__main__':
	main()
