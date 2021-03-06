
"""

 1- Load certificate
 2- Sign

"""

from lxml import etree
import logging
import subprocess
import os

class CertificateService:
	""" Properties """
	certificate = None
	key = None
	_pfx_password = ''
	_pfx_path = ''

	key_path = 'cert/keyfile.key'
	cert_path = 'cert/certificate.crt'
	sii_cert_path = 'cert/sii_public.cert'

	def __init__(self, pfx_file_path, pfx_password=''):
		self._pfx_password = pfx_password
		self._pfx_path = pfx_file_path

	def generate_certificate_and_key(self):
		""" Get logger """
		logger = logging.getLogger()
		logger.info("set_certificate::Loading certificate from " + str(self._pfx_path))

		""" Generate encrypted privated key """
		subprocess.run(["openssl", "pkcs12", "-in", self._pfx_path ,"-passin", "pass:" +self._pfx_password, "-passout","pass:" +self._pfx_password, "-out", self.key_path])
		""" Get certificate """
		subprocess.run(["openssl", "pkcs12", "-in", self._pfx_path, "-clcerts", "-nokeys", "-passin", "pass:" +self._pfx_password, "-passout","pass:" +self._pfx_password, "-out", self.cert_path])
		""" Decrypte private key """
		subprocess.run(["openssl", "rsa", "-in", self.key_path, "-passin", "pass:" +self._pfx_password, "-passout","pass:" +self._pfx_password, "-out", self.key_path])
		""" Load temporary created files and delete """
		self._load_certficate_and_key()
		self._remove_certificate_and_key()

	def read_file(self, f_name):
		with open(f_name, "rb") as f:
			return f.read()

	def _load_certficate_and_key(self):
		self.certificate = self.read_file(self.cert_path)
		self.key = self.read_file(self.key_path)

	def _remove_certificate_and_key(self):
		try:
			os.remove(self.key_path)
		except OSError as e:  ## if failed, report it back to the user ##
			print ("Error: %s - %s." % (e.filename, e.strerror))
		try:
			os.remove(self.cert_path)
		except OSError as e:  ## if failed, report it back to the user ##
			print ("Error: %s - %s." % (e.filename, e.strerror))

	def get_password(self):
		return self._pfx_password
