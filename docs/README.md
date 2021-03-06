[Home](/) | [Config](/config) | [Cli](/cli)
---

Let’s be real in world where tableau, Qlik and Power Bi are the leaders in interactive dashboard. We still get asked for dashboards to be emailed or printed, and these request usually come from very high up (someone with a Cxx or VP) who don’t have the time for the extra clicks. Here is our solution to email dashboard that are also mobile responsive. 

This project is built using the <a target="_blank" href="http://pugsql.org">pugSQL</a> Python module. Which affords us the ability for working with any Python DB-API2, that lets us support a large number of databases  like:  sqlite, postgreSQL, MySQL, and Oracle.

See the documentation at <a target="_blank" href="http://dashflow.io/config">dashflow.io/config</a>.

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

2) Assuming your using an evironment running python3 install the required modules and make the cli script executable
   

```
pip install -r ./requirments.txt
chmod u+x ./df-cli.py

sudo apt install xvfb
```

3) Review the sample folders. You will find a sql folder in which you see the sql files that drive the dashboard. (see [pugSQL](https://pugsql.org){:target="_blank"} on how to configure the files.) Open up sample-config.json, for more on the configuration file visit [https://dashflow.io/config](https://dashflow.io/config). Edit the config file to point to your database, smtp server, and quick chart hosting.

4) Run the sample from the command line

```
./df-cli.py --configFile=sample/sample-config.json --parameters="kind:adio"
```

5) You will receive an email similar to this
<a _target="blank" href="https://dashflow.io/example.png">![alt="example of rendered email"](https://dashflow.io/example.png)</a>

---

## Run Unit Tests

```
cd unittests
python -m unittest  compiler-tests.py
```
