"""

 Generate PDFs

 Needed : sudo apt install -y wkhtmltopdf
 Or Windows: https://wkhtmltopdf.org/downloads.html

"""

import pdfkit
import pdf417
import os
from lib.models.dte import DTE, DTEBuidler, DTECAF
from jinja2 import Environment, FileSystemLoader
from instance.config import WKHTMLTOPDF_EXE_PATH

FILE_DIR = os.path.dirname(os.path.realpath(__file__))

class PDFGenerator:
	__template_by_type = {
							52:'web/templates/sii_document_52.html',
							33:'web/templates/sii_document_33.html'
						}

	def generate(self, dte, output_path=""):
		# Use False instead of output path to save pdf to a variable
		ted = self._generate_png_ted(dte.generate_ted())
		html = self._populate_jinja_template(dte, ted)
		options = {
			'page-size': 'A3',
			'dpi': 600,
			'enable-local-file-access': None,
			'load-error-handling': 'ignore'
		}

		filename = str(dte.get_document_id()) + '.pdf'
		if output_path == "":
			output_path = FILE_DIR + '/../temp/'

		fullpath = output_path + filename

		""" Path to wkhtmltopdf """
		path_wkhtmltopdf = WKHTMLTOPDF_EXE_PATH
		config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)

		pdf = pdfkit.from_string(html, fullpath, options=options, configuration=config)
		return filename

	def generate_binary(self, dte):
		# Use False instead of output path to save pdf to a variable
		ted = self._generate_png_ted(dte.generate_ted())
		html = self._populate_jinja_template(dte, ted)
		options = {
			'page-size': 'A3',
			'dpi': 600
		}

		filename = str(dte.get_document_id()) + '.pdf'

		pdf = pdfkit.from_string(html, False, options=options)
		return filename, pdf

	def _populate_jinja_template(self, dte, ted):
		""" Get template path by type """
		document_type = dte.get_document_type()

		try:
			template_path = self.__template_by_type[int(document_type)]
		except:
			print("_populate_jinja_template:: Template not declared for document type " + str(document_type) + " using 33 by default.")
			template_path = self.__template_by_type[33]

		with open(template_path, encoding="utf-8") as f:
			template_str = f.read()
		""" Load template """
		template = Environment(loader=FileSystemLoader([FILE_DIR + '/web/templates', FILE_DIR + '/../temp'])).from_string(template_str)
		""" Get template parameters """
		template_parameters = dte.to_template_parameters()
		""" Render """
		html_str = template.render(parameters=template_parameters, ted=ted)
		return html_str

	def _generate_svg_ted(self, ted_string):
		codes = pdf417.encode(ted_string, security_level=5)
		svg = pdf417.render_svg(codes, scale=3, ratio=3)  # ElementTree object
		return svg

	def generate_test_svg_ted(self, ted_string, filepath=FILE_DIR + '/../temp/test.svg'):
		unique = 1
		filename = str(unique) + 'barcode.svg'
		filepath = FILE_DIR + '/../temp/' + filename
		codes = pdf417.encode(ted_string, security_level=5)
		svg = pdf417.render_svg(codes, scale=3, ratio=3)  # ElementTree object
		svg.write(filepath)
		return filename

	def _generate_png_ted(self, ted_string):
		unique = 1
		filename = str(unique) + 'barcode.png'
		filepath = FILE_DIR + '/../temp/' + filename
		""" Stripping white space and \n """
		ted_string = ted_string.replace(" ", "").replace("\n", "")
		codes = pdf417.encode(ted_string, columns=10, security_level=5)
		image = pdf417.render_image(codes, scale=3, ratio=3, padding=5)  # Pillow Image object
		image.save(filepath)
		return filepath
