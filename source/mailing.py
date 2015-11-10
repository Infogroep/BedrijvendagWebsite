import smtplib
from email.mime.text import MIMEText

import config


def send_recovery_email(to, hash):
    me = config.mail_from
    text = """Someone has specified you forgot your login credentials for bedrijvendag.infogroep.be,
if this is not the case, you can ignore this message. Otherwise, go to 
http://students2industry.be/recover/%s 
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

Bij deze bevestigen wij uw inschrijving voor Students2Industry 2016. U kan steeds een logo uploaden voor uw bedrijf.
Indien u nog geen logo op de website heeft geplaatst raden wij u ten zeerste aan dit alsnog te doen.
Uw Industry-book pagina(s) kan/kunnen nog altijd aangepast worden om te passen in de daarvoor voorziene ruimte.
De beschikbare ruimte hangt af van uw formule. Je kan dit altijd controleren op https://students2industry.be/pricelist
Je kan ook steeds ruimte bijkopen zolang je het contract niet hebt aangevraagd.
Vergeet zeker niet om een contract aan te vragen, zodat we de inschrijving definitief kunnen maken.
We zijn altijd beschikbaar voor vragen en opmerkingen op contact@students2industry.be

Bedankt voor uw interesse en tot op Students2Industry,

Kwinten Pardon
Badreddine Hachoumi
Linda de Corte


--------------------------
ENGLISH VERSION
--------------------------

Dear,

We hereby confirm your company's registration for Students2Industry 2016 You can always upload your company's logo.
We recommend you to upload your company's logo if you haven't done this yet.
your Industry-book (companies book) pages can always be edited by the organisation to fit in the space available to you.
This depends on your formula which is visible at http://students2industry.be/pricelist.
You can also buy more space until your contract has been requested.
Don't forget to request your contract to complete the registration and make it final.
We are always available for questions and remarks at contact@students2industry.be


Thank you for your interest and we're hoping to welcome you at Students2Industry.


Best regards,

Kwinten Pardon
Badreddine Hachoumi
Linda de Corte

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

