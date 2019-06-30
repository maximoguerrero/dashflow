#!/usr/bin/env python
import argparse
from libs import load as pcld, send as pcsend, pdf as pcpdf


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--parameter', nargs="+",  help='parameters that are'
                                                         'to be passed to sql'
                                                         'statements')
    parser.add_argument('--configFile',  help='config file for mailing')
    parser.add_argument('--pdfFile',  help='name to use when generating the pdf file ')
    parser.add_argument('--pdfOnly', default=False,  help='do not send email only generate pdf')
    parser.add_argument('--sendAsAttachment', default=False,  help='send the report as pdf ')
    
    args = parser.parse_args()
    print(args)

    parameters = dict()
    if "parameter" in args:
        for arg in args.parameter:
            print(arg)
            parram = str(arg).split(':')
            parameters[parram[0]] = parram[1]

    configFile = ''
    if "configFile" in args:
        configFile = args.configFile

    pc = pcld(configFile, parameters)

    if "pdfFile" in args and "pdfOnly" in args and args.pdfOnly:
        pcpdf(pc, args.pdfFile)
    elif 'sendAsAttachment' in args and args.sendAsAttachment:
        if "pdfFile" in args:
            pcsend(pc, args.pdfFile, True)
        else:
            raise Exception("send as attachment must us pdffile")
    else:
        pcsend(pc)

    return

if __name__ == "__main__":
    # execute only if run as a script
    main()
