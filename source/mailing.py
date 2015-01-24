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
    msg["Subject"] = "Password recovery for bedrijvendag.infogroep.be"
    msg["From"] = me
    msg["To"] = to

    s = smtplib.SMTP(host=config.mail_host, port=config.mail_port)
    s.starttls()
    s.login(config.mail_user, config.mail_password)
    s.sendmail(me, to, msg.as_string())
    s.quit()


def send_enlist_mail(company):
    me = config.mail_from
    text = """%s has enlisted for the next edition of bedrijvendag.
    Please confirm his participation or put him in the queue.
    When they have to be put in the queue,
    don't forget to mail them with the extra information why he has been put in the queue

    Infogroep""" % company

    msg = MIMEText(text, "plain")
    msg["Subject"] = """%s has enlisted""" % company
    msg["From"] = me
    msg["To"] = me

    s = smtplib.SMTP(host=config.mail_host, port=config.mail_port)
    s.starttls()
    s.login(config.mail_user, config.mail_password)
    s.sendmail(me, me, msg.as_string())
    s.quit()


def send_confirmation_mail(to):
    print "sending mail"

    me = config.mail_from

    to_address = to
    cc_address = []
    bcc_address = [me]

    text = """Beste,


Bij deze bevestigen wij uw inschrijving voor de Bedrijvendag 2015. U kan steeds een logo uploaden voor uw bedrijf.
Indien u nog geen logo op de website heeft geplaatst raden wij u ten zeerste aan dit alsnog te doen.
De "bedrijvendagboek" pagina(s) kan/kunnen nog altijd aangepast worden om te passen in de daarvoor voorziene ruimte.
De beschikbare ruimte hangt af van uw formule. Je kan dit altijd controleren op http://bedrijvendag.infogroep.be/pricelist.
Je kan ook steeds ruimte bijkopen zolang je het contract niet hebt aangevraagd.
Vergeet zeker niet om een contract aan te vragen, zodat we de inschrijving definitief kunnen maken.
We zijn altijd beschikbaar voor vragen en opmerkingen op bedrijvendag@infogroep.be


Bedankt voor uw interesse en tot op de Bedrijvendag,


Met vriendelijke groeten,
Kwinten Pardon
Elyn Meert


--------------------------
ENGLISH VERSION
--------------------------

Dear,

We hereby confirm your company's registration for Bedrijvendag 2015. You can always upload your company's logo.
We recommend you to upload your company's logo if you haven't done this yet.
The "bedrijvendagboek" (companies book) pages can always be edited by the organisation to fit in the space available to you.
This depends on your formula which is visible at http://bedrijvendag.infogroep.be/pricelist.
You can also buy more space until your contract has been requested.
Don't forget to request your contract to complete the registration and make it final.
We are always available for questions and remarks at bedrijvendag@infogroep.be


Thank you for your interest and we're hoping to welcome you at the Bedrijvendag.


Best regards,
Kwinten Pardon
Elyn Meert

"""

    msg = MIMEText(text, "plain")
    msg["Subject"] = """Bevestiging inschrijving / Confirmation registration Bedrijvendag 2015"""

    msg["From"] = me
    msg["To"] = to

    to_addresses = [to_address] + cc_address + bcc_address

    s = smtplib.SMTP(host=config.mail_host, port=config.mail_port)
    s.starttls()
    s.login(config.mail_user, config.mail_password)
    s.sendmail(me, to_addresses, msg.as_string())
    s.quit()

