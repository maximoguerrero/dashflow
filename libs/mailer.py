import pugsql, os
import smtplib

from headless_pdfkit import generate_pdf as genpdf
from email.message import EmailMessage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication


class Mailer:
    configFile = ""
    configPath = ""
    htmlBody = ""
    recipients = []
    parameters = dict()

    def __init__(self, configFile, configPath, parameters, htmlBody):
        self.configFile = configFile
        self.configPath = configPath
        self.htmlBody = htmlBody
        self.parameters = parameters

        modPath = os.path.join(configPath, self.configFile["sqlfolder"])
        self.queries = pugsql.module(modPath)

        conn = self.configFile["connection"]
        if "<absolutePath>" in conn:
            conn.replace("<absolutePath>", configPath)
            
        self.queries.connect(conn)

        return
    
    def loadRecipients(self):
        self.recipients = []
        for item in self.configFile["to"]:
            if "string" == item["type"]:
                self.recipients += item["value"].split(",")

            if "database" == item["type"]:
                args = dict()
                if self.parameters and "moduleParameters" in item:
                    for mpKey in item["moduleParameters"]:
                        for gpKey in self.parameters.keys():
                            if(mpKey["name"] == gpKey):
                                args[gpKey] = self.parameters[gpKey]
                data = [i for i in getattr(self.queries, item["moduleName"])(**args)]

                for item in data:
                    self.recipients.append(item["email"])

        return ', '.join(self.recipients)

    def send(self, sendAsPDF=False, pdfFile='report.pdf'):
        print("starting to send")
        print(self.configFile['sendEngine'])
        msg = MIMEMultipart()

        if(not sendAsPDF):
            msg.attach(MIMEText(self.htmlBody, 'html'))
        else:
            ret = genpdf(self.htmlBody)
            pdffile = os.path.join(self.configPath, pdfFile)
            with open(pdffile, 'wb') as w:
                w.write(ret)

            with open(pdffile, "rb") as pdfData:
                pdfMime = MIMEApplication(pdfData.read())
                pdfMime['Content-Disposition'] = 'attachment; filename="%s"' % pdfFile
                msg.attach(pdfMime)



        msg['From'] = self.configFile['from']
        if self.configFile["isDebug"]:
            msg['To'] = 'maximo.guerrero@gmail.com'
            msg['Subject'] = "DEBUG " + self.configFile['subject']
        else:
            msg['To'] = self.loadRecipients()
            msg['Subject'] = self.configFile['subject']

        # Try to send the message.
        try:  
            print("start sending", msg['From'],  msg['To'])
            server = smtplib.SMTP(self.configFile['sendEngine']['host'], 
                                  self.configFile['sendEngine']['port'])
            server.ehlo()
            server.starttls()
            server.ehlo()

            if ("requiresAuthentication" in self.configFile['sendEngine'] and 
                 self.configFile['sendEngine']['requiresAuthentication']):
                if "useEnvVariable" in self.configFile["sendEngine"]:
                    server.login(os.environ[self.configFile["sendEngine"]
                                                           ["useEnvVariable"]
                                                           ["username"]],
                                 os.environ[self.configFile["sendEngine"]
                                                           ["useEnvVariable"]
                                                           ["password"]])
                else:
                    server.login(self.configFile['sendEngine']['username'],
                                 self.configFile['sendEngine']['password'])

            server.sendmail(msg['From'],  msg['To'], msg.as_string())
            server.close()
        # Display an error message if something goes wrong.
        except Exception as e:
            print("Error: ", e)
        else:
            print("Email sent!")

        return
