[Home](/) | [Config](/config) | [Cli](/cli)
---

# CLI parrameters

---

**--parrameter**

Use this flag to  pass parramets to your sql modules. Format must be delimited by a colon "key:value". 
For multiple parrmeters just repeat qouted key-value pairs;
```
./df-cli.py --configFile ./sample/sample-config.json --parrameter "kind:audio" "test:test"
```

---

**--configFile**

This is the relative path to config file. Application will create an absolute path based on current working directory and the file

---

**--pdfFile**

Name for the pdf file to be generated.

---

**--pdfOnly**

This will not send an email, but it will save a pdf to the same folder as the config flie.

---

**--sendAsAttachment**

Send dashboard as a pdf attachment.

