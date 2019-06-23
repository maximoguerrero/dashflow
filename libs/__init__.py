import json, os
from . import compiler as pcomp
from . import mailer as mailer

__version__ = "1.0"

cwd = os.getcwd()

def load(configFile, parrameters=None):
    configFile = os.path.realpath(os.path.join(cwd, configFile))
    configPath = os.path.dirname(configFile)
    with open(configFile) as f:
        config = json.load(f)
        compiler = pcomp.Compiler(config, configPath, parrameters)
    return compiler


def send(pc):
    htmlEmail = pc.build()
    m = mailer.Mailer(pc.getConfig(), pc.getConfigPath(), pc.getParrameters(), htmlEmail)
    m.send()
    return

__all__ = ["load", "send" "__version__"]
