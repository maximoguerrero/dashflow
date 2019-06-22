import pugsql, os
import smtplib

from email.message import EmailMessage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class Mailer:
    configFile = ""
    htmlBody = ""
    recipients = []
    parrameters = dict()

    def __init__(self, configFile, configPath, parrameters, htmlBody):
        self.configFile = configFile
        self.htmlBody = htmlBody
        self.parrameters = parrameters

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
                if self.parrameters and "moduleParrameters" in item:
                    for mpKey in item["moduleParrameters"]:
                        for gpKey in self.parrameters.keys():
                            if(mpKey["name"] == gpKey):
                                args[gpKey] = self.parrameters[gpKey]
                data = [i for i in getattr(self.queries, item["moduleName"])(**args)]

                for item in data:
                    self.recipients.append(item["email"])

        return ', '.join(self.recipients)

    def send(self):
        print("starting to send")
        print(self.configFile['sendEngine'])
        msg = MIMEMultipart()

        msg.attach(MIMEText(self.htmlBody, 'html'))

        if self.configFile["isDebug"]:
            msg['From'] = 'info@warriormill.com'
            msg['To'] = 'maximo.guerrero@gmail.com'
            msg['Subject'] = "DEBUG " + self.configFile['subject']
        else:
            msg['From'] = self.configFile['from']
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
