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

### googleStaticChartsUrl

This should point to your own hosted version of [quickcharts.io](http://quickcharts.io). You may use our default just for testing. *(charts may not dispay or timeout during high load)*

```https://quickcharts.dashflow.io/chart?bkg=white&c=```

---

