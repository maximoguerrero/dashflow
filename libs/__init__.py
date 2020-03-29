import json
import os
from headless_pdfkit import generate_pdf as genpdf
from . import compiler as pcomp
from . import mailer as mailer

__version__ = "1.0"

cwd = os.getcwd()


def load(configFile, parameters=None):
    configFile = os.path.realpath(os.path.join(cwd, configFile))
    configPath = os.path.dirname(configFile)
    with open(configFile) as f:
        config = json.load(f)
        compiler = pcomp.Compiler(config, configPath, parameters)
    return compiler


def send(pc, filename=None, sendAsAttachment=False):
    htmlEmail = pc.build()
    m = mailer.Mailer(pc.getConfig(),
                      pc.getConfigPath(),
                      pc.getparameters(),
                      htmlEmail)
    m.send(sendAsAttachment, filename)
    return


def pdf(pc, filename):
    htmlEmail = pc.build()
    ret = genpdf(htmlEmail)
    pdffile = os.path.join(pc.getConfigPath(), filename)
    print(pdffile)
    with open(pdffile, 'wb') as w:
        w.write(ret)


__all__ = ["load", "send" "__version__"]
