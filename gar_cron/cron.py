import gar_cron
from gar_cron import __version__, __title__, __description__
from cfgsaver import cfgsaver
import json, os, argparse, requests
from datetime import datetime
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

#apppath = os.path.dirname(os.path.realpath(__file__))
#conf_file = os.path.join(apppath, 'config.json')
pkg_name = "gar_cron"
config_keys = ['github_username', 'alert_email']
config = cfgsaver.get(pkg_name)

def send_mail(to, subject, text, file_name = ""):
	try:
		#message = MIMEText(msg_content, 'html')
		message = MIMEMultipart()
		message['From'] = "GAR Admin <%s>" % config['smtp_email']
		message['To'] =  to #'Receiver Name <receiver@server>'
		#message['Cc'] = 'Receiver2 Name <receiver2@server>'
		message['Subject'] = subject
		message.attach(MIMEText(text))
		
		#Attach file
		if len(file_name) > 0:
			part = MIMEApplication(
				open(file_name, 'rb').read(),
				Name=os.path.basename(file_name)
			)
			part['Content-Disposition'] = 'attachment; filename="%s"' % os.path.basename(file_name)
			message.attach(part)

		#server = smtplib.SMTP(settings['email_smtp_server'] + ":" + str(settings['email_smtp_port']))
		server = smtplib.SMTP(config['smtp_server'], 587)
		server.starttls()
		server.login(config['smtp_username'], config['smtp_password'])
		server.sendmail(config['smtp_email'],
						[to],
						message.as_string())
		server.quit()	
	except Exception as e:
		print("Error occurred: " + str(e))
	print("email sent to %s" % to)
	
def parse_date(dt):
    format = "%Y-%m-%dT%H:%M:%S"
    if dt[-6] in ('+', '-'):
        return datetime.strptime(dt, format + '%z')
    elif dt[-1] == 'Z':
        return datetime.strptime(dt, format + 'Z')
    return datetime.strptime(dt, format)
	
def send_reminder(sub):
	text = """Hey Dude,

This is just a friendly reminder regarding your github activity.
It has been several days since your last commit, so let's get back to work buddy.

Cheers,
GAR Admin"""
	send_mail(config['alert_email'], sub, text)

def check_activity():
	url = "https://api.github.com/users/%s/events" % config['github_username']
	resp = requests.get(url)
	acts = json.loads(resp.text)
	if len(acts) == 0:
		print("Zero events found, is this the correct github repo I'm looking at?")
		print("Run the program again with --config parameter to set the correct values")
		return
	for i in range(len(acts)):
		act = acts[i]
		if act['type'] == 'PushEvent': #latest commit
			dt = parse_date(act['created_at'])
			delta = datetime.now() - dt
			days = delta.days
			hrs = delta.seconds // 3600
			mins = (delta.seconds // 60) % 60
			threshold = 3 #max days
			sub = "It has been %d days, %d hours and %d minutes since your last commit on github" % (days, hrs, mins)
			print(sub)
			if delta.days >= threshold:
				send_reminder(sub)
			return
	print("no commit events found on github")
	send_reminder("It has been quite a while since your last commit on github")
	return	
	

def main():
	global config
	banner = """%s version %s
%s

Copyright (c) 2019 Prahlad Yeri.

This work is licensed under the terms of the MIT license.  
For a copy, see <https://opensource.org/licenses/MIT>.
""" % (__title__, __version__, __description__)
	parser = argparse.ArgumentParser()
	parser.add_argument('-v', '--version',  default=False, action='store_true', help='display the version number')
	parser.add_argument('-c', '--config',  default=False, action='store_true', help='setup the app configuration')
	args = parser.parse_args()
	if args.version:
		print(banner)
		return
	if args.config:
		config = cfgsaver.get_from_cmd(pkg_name, config_keys)
		if config == None:
			print("Cound't read config values, please start the program again using --config parameter")
		return

	if config == None:
		config = cfgsaver.get_from_cmd(pkg_name, config_keys)
		if config == None:
			print("Cound't read config values, please start the program again using --config parameter")
			return
	# if config["github_username"] == "":
		# print("Configuration file is empty. Please put the appropriate values in this config file:\n")
		# print(conf_file)
		# return
	# else:
	check_activity()
	


if __name__ == "__main__":
	main()