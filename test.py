import pugsql
import sys, os
from libs import load as pcld, send as pcsend

sys.path.append(os.path.dirname(os.path.abspath(__file__)))


# Load all of the *sql files in the queries/ directory into a single module.
queries = pugsql.module('sample/sql/')
queries.connect('sqlite:///sample/sample.db')

'''
print("Connected")

most_sold = [i for i in getattr(queries, "most_sold")()]
print("most_sold \n", most_sold)

pugsql.get_modules().clear()
'''

# test my loader
parameters = dict({"kind": "audio"})
pc = pcld('sample/sample-config.json', parameters)
html = pc.build()

f = open("test.html", "w")
f.write(html)
f.close()



pcsend(pc)




