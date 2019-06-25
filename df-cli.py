#!/usr/bin/env python
import argparse
from libs import load as pcld, send as pcsend, pdf as pcpdf


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--parrameter', nargs="+",  help='parrameters that are'
                                                         'to be passed to sql'
                                                         'statements')
    parser.add_argument('--configFile',  help='config file for mailing')
    parser.add_argument('--pdfFile',  help='config file for mailing')
    
    args = parser.parse_args()
    print(args)

    parrameters = dict()
    if "parrameter" in args:
        for arg in args.parrameter:
            print(arg)
            parram = str(arg).split(':')
            parrameters[parram[0]] = parram[1]

    configFile = ''
    if "configFile" in args:
        configFile = args.configFile

    pc = pcld(configFile, parrameters)

    if "pdfFile" in args:
        pcpdf(pc, args.pdfFile)

    else:
        pcsend(pc)

    return

if __name__ == "__main__":
    # execute only if run as a script
    main()
