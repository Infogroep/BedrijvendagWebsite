import smtplib

from email.mime.text import MIMEText
import config

def send_recovery_email(to, hash):
	me = config.mail_from
	text = """Someone has specified you forgot your login credentials for bedrijvendag.infogroep.be,
if this is not the case, you can ignore this message. Otherwise, go to 
http://bedrijvendag.infogroep.be/recover/%s 
to complete the recovery process.

Infogroep""" % hash

	msg = MIMEText(text, 'plain')
	msg["Subject"] = "Password recovery for bedrijvendag.infgroep.be"
	msg["From"] = me
	msg["To"] = to

	s = smtplib.SMTP_SSL(host=config.mail_host, port=config.mail_port)
	s.login(config.mail_user, config.mail_password)
	s.sendmail(me, to, msg.as_string())
	s.quit()