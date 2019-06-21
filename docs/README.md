This projec is built using the [pugSQL](https://pugsql.org/). Which affords us the ability for working with any Python DB-API2, that lets us support a large number of databases  like:  sqlite, postgreSQL, MySQL, and Oracle.

Requirements:
    
- Python 3
- pugSQL
- sqlAlchmey 
- Jinja Templating Engine
  

---
## Quickstart

1) Start by clonning the repo.


```
git clone https://github.com/maximoguerrero/dashflow.git
cd dashflow
```

2) Assuming your using and evironment running python3 install the required modules.
   

```
pip install -r ./requirments.txt
chmod u+x ./df-cli.py
```

3) Review the sample folders. You will find a sql folder in which you see the sql files that drive the dashboard. (see [pugSQL](https://pugsql.org) on how to configure the files.) Open up sample-config.json, for a on the configuration file visit (https://dashflow.io/config)[https://dashflow.io/config]