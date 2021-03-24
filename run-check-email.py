import imaplib
import json
from instance.config import SII_INBOX_EMAIL_ACCOUNT, SII_INBOX_EMAIL_SERVER, SII_INBOX_EMAIL_PASSWORD, JSON_LAST_SEEN_PATH

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

# connect to host using SSL
imap = imaplib.IMAP4_SSL(SII_INBOX_EMAIL_SERVER)

## login to server
imap.login(SII_INBOX_EMAIL_ACCOUNT, SII_INBOX_EMAIL_PASSWORD)

imap.select('Inbox', readonly=True)

tmp, data = imap.search(None, 'RECENT')
for num in data[0].split():
	tmp, data = imap.fetch(num, '(RFC822)')
	uid = int.from_bytes(num, "little")  
	if uid > last_seen_uid:
		""" Not seen """
		last_seen_uid = uid
imap.close()

save_last_seen_uid(last_seen_uid)
