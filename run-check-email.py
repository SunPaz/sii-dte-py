from imap_tools import MailBox
from lib.models.dte import DTEBuidler
from lib.pdf_generator import PDFGenerator
import json
from instance.config import SII_INBOX_EMAIL_ACCOUNT, SII_INBOX_EMAIL_SERVER, SII_INBOX_EMAIL_PASSWORD, SII_INBOX_IMAP_CRITERIA
from instance.config import JSON_LAST_SEEN_PATH

def save_last_seen_uid(uid):
	try:
		with open(JSON_LAST_SEEN_PATH, "w") as write_file:
			context = json.dumps({'last_seen_uid': str(uid)}, indent=4, sort_keys=True)
			write_file.write(context)
	except:
		print("save_last_seen_uid:: Error")

def load_last_seen_uid():
	try:
		with open(JSON_LAST_SEEN_PATH,) as read_file:
			context = json.load(read_file)
			return context.last_seen_uid
	except:
		print("load_last_seen_uid:: Error")
		return 0;

last_seen_uid = load_last_seen_uid()
pdf = PDFGenerator()
builder = DTEBuidler()

# get all attachments for each email from INBOX folder
with MailBox(SII_INBOX_EMAIL_SERVER).login(SII_INBOX_EMAIL_ACCOUNT, SII_INBOX_EMAIL_PASSWORD) as mailbox:
	""" Filter out analysis result from SII """
	for msg in mailbox.fetch(SII_INBOX_IMAP_CRITERIA, mark_seen=False):
		if int(msg.uid) > int(last_seen_uid):
			last_seen_uid = msg.uid
			for att in msg.attachments:
				""" Only XML """
				if att.filename.upper().endswith(".XML"):
					print("Getting " + att.filename, att.content_type)
					try:
						_, _, dte_object = builder.from_string(att.payload)
						pdf.generate(dte_object, output_path="", filename=str(dte_object._document_id) + "-" + str(dte_object._header.sender.get_attr("RUT")) + ".pdf")
					except:
						print("Could not process file " + att.filename)

save_last_seen_uid(last_seen_uid)
