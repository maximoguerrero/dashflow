[Home](/) | [Config](/config)
---

# Config File Documentation

The config file drives the entire applicaiton, from creation of the HTML email to sending the email to its recipients. The following are properties of the json config file.

We recommend that when creating a dashboard, you create a folder to house all the files. Similar to to the sample provided

---

### isDebug
*true* |  then a subject line is prepended with DEBUG: and email is sent to a hardcoded value instead of recepient list.

---

### connection

This is a sqlAlchemy compatible connections string [https://docs.sqlalchemy.org/en/14/core/engines.html](https://docs.sqlalchemy.org/en/14/core/engines.html)

When working with sqlite database you can either pass in a absolute path to the database. Or if you use the following syntax we will inject the current working directory you are executing form.

```
sqlite:///<absolutePath>/sample.db
```
---

### sqlfolder

This is a the folder containig the sql files from which the sections will be generated. This should a relative path from the config file.

---

### quickChartsUrl

This should point to your own hosted version of [quickcharts.io](http://quickcharts.io). You may use our default just for testing. *(charts may not dispay or timeout during high load)*

```
https://quickcharts.dashflow.io/chart?bkg=white&c=
```

---

### title

The tile to be used at the top of the email. Will use an H1 tag. Leave as empty string if you dont want it displayed.

---

### description

This will be renderd under the title as the first paragraph. Leave as empty string if you dont it displayed.

---

### subject

The subject line to be used in the email

---

### from

The from address for the email

---

### to

Takes a collection of objects. Can be either a string or a database lookup.

*STRING*
```
    "to": [
        {
            "type": "string",
            "value": "someone@somewhere.com"
        }
    ]
```
*DATABASE*
```
    "to": [
        {
            "type": "database",
            "moduleName": "send_list"
        }
    ]
```

---

### sendEngine
**type**:  smtp

**host**:  ip address or hostname to the smtp server

**port**:  port to use for connecting to the smtp server

**enableTLS**: where or not to start tls connection

**requiresAuthentication**: where or not a username and password is used to log into the server.

*OPTIONAL*

**username**: username to login

**password**: password to login

**useEnvVariable**: enviroment variables for username and password to use when login into smtp server

```
    "useEnvVariable": {
        "username": "SMTP_USER",
        "password": "SMTP_PWD"
    }
```

---
## Sections

sections is a list of section configuration types. The types can be any of the following **"database"**, **"text/html"**, or **"chart"**.

see [sample configue files](https://github.com/maximoguerrero/dashflow/blob/master/sample/sample-config.json) for exmaples of use.

**text/html** will just render html markup and not database interactions.

**database** sections can be renderd either as a *table* or as *markup*.  When using markup you can inject results form a query into markup by referencing column valus, your query must return one row.  *moduleName* should be used for the sql querie you created.

**chart** section will render a chart along with a description at the bottom of the chart and a title at the top of the chart. see [sample file](https://github.com/maximoguerrero/dashflow/blob/master/sample/sample-config.json) for proper usage.