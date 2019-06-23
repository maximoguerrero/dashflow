import pugsql, os, json, sys, random
import urllib
from jinja2 import Environment, FileSystemLoader, BaseLoader, select_autoescape


templateDir = os.path.join(os.path.dirname(
                            os.path.abspath(__file__)), "templates")
cwd = os.getcwd()

env = Environment(
    loader=FileSystemLoader(templateDir),
    autoescape=select_autoescape(['html', 'xml'])
)

colorPalette = ['#a62987', '#0d404f', '#dc8fa3', '#9dc352', '#b0106a',
                '#697832', '#96ac48', '#1d1681', '#aecc71', '#799542',
                '#266f93', '#596297', '#fb82e1', '#dd16b1', '#f37ef2',
                '#aa98e0', '#6273b7', '#5cb9b1', '#f69be8', '#3dac49',
                '#094d12', '#ca99dd', '#1f5b35', '#88b580', '#92b158',
                '#ada345', '#2689de', '#5dbe82', '#7a6c50', '#4b57b7',
                '#16de82', '#76b063', '#1e3305', '#b54319', '#c04027',
                '#60b170', '#1fcba4', '#9207bd', '#468f5d', '#44abcc',
                '#65ab0b', '#a15892', '#70d6b9', '#4b530d', '#4e0d49',
                '#af7517', '#ee9b9f', '#4aa4ae', '#5a8752', '#8eef90',
                '#241dff', '#39a294', '#9bed01', '#cc3016', '#5e0905',
                '#f87e1a', '#f5651e', '#a1190b', '#b16d81', '#a7eac4',
                '#a4ae30', '#eb3d26', '#92482e', '#9d534f', '#c74f15',
                '#8d2f13', '#7da20d', '#54730b', '#eb875b', '#22295e',
                '#b3dbc6', '#ad1b52', '#f2b07f', '#537907', '#678663',
                '#8fdc6b', '#501040', '#162180', '#162180', '#f09f6a',
                '#3a6885', '#9e628f', '#723922', '#e61f7f', '#34bc8a',
                '#4045af', '#83b17d', '#1B813E', '#7a0844', '#1B81A2',
                '#341dd3', '#d23c74', '#db9b6f', '#70d3ee', '#f6e82d',
                '#e11031', '#e6a775', '#d685d8', '#7b3beb', '#176cce']


class Compiler:
    configFile = {}
    configPath = ""
    queries = {}
    parrameters = None
    templateDir = ''
    baseCss = ''

    def __init__(self, configFile, configPath, parrameters=None):
        self.configFile = configFile
        self.configPath = configPath
        self.parrameters = parrameters

        modPath = os.path.join(configPath, self.configFile["sqlfolder"])
        self.queries = pugsql.module(modPath)
        
        conn = self.configFile["connection"]
        if "<absolutePath>" in conn:
            conn = conn.replace("<absolutePath>", configPath)

        self.queries.connect(conn)
        if "templates" in self.configFile and "css" in self.configFile["templates"]["css"]:
            with open(os.path.join(configPath,  self.configFile["templates"]["css"]), "r") as f:
                self.baseCss = f.read()

        else:
            with open(os.path.join(templateDir, "base_styles.css"), "r") as f:
                self.baseCss = f.read()

    def getConfig(self):
        return self.configFile
    
    def getConfigPath(self):
        return self.configPath
    
    def getParrameters(self):
        return self.parrameters

    def getData(self, section):
        args = dict()
        if self.parrameters and "moduleParrameters" in section:
            for mpKey in section["moduleParrameters"]:
                for gpKey in self.parrameters.keys():
                    if(mpKey["name"] == gpKey):
                        args[gpKey] = self.parrameters[gpKey]

        data = [i for i in getattr(self.queries, section["moduleName"])(**args)]
        return data

    def build(self):
        htmlSections = []
        sections = self.configFile["sections"]

        title = ""
        description = ""
        if "title" in self.configFile and len(self.configFile["title"]) > 0:
            title = self.configFile["title"]
        if "description" in self.configFile and len(self.configFile["description"]) > 0:
            description = self.configFile["description"]

        if title or description:
            htmlSections.append(self.buildHeader(title, description))

        for section in sections:
            print("===================================================\n")
            print("Section ", section['sectionTitle'])
            print("Type ", section['type'])

            keys = []
            data = []

            if("moduleName" in section):
                data = self.getData(section)
            
            if(len(data)):
                keys = data[0].keys()

            if "renderAs" in section:
                if "table" in section["renderAs"]:
                    htmlSections.append(self.buildHtmlTable(data, keys, section['sectionTitle'],))

                if "markup" in section["renderAs"]:
                    if len(data):
                        data = data[0]
                        data['title'] = section['sectionTitle']
                        htmlSections.append(self.buildMarkup(data, section["markup"], section['sectionTitle']))

            if "text/html" in section["type"]:
                markup = ""
                if("sectionTitle" in section and section["sectionTitle"]):
                    markup = "<h3>" + section["sectionTitle"] + "</h3>" + section["markup"]
                htmlSections.append(markup)

            if "chart" in section["type"]:
                description = section["description"]
                if section["chart"]["type"] in ("horizontalBarSimple",
                                                "doughnut",
                                                "pie"):
                    t = section["chart"]["type"]
                    if t == "horizontalBarSimple":
                        t = "horizontalBar"
                    chartSrc = self.buildHorizontalImgSimple(data, type=t)

                if not section["chart"]["type"] in ("horizontalBarSimple",
                                                    "doughnut",
                                                    "pie"):
                    stacked = False
                    if "stacked" in section["chart"]:
                        stacked = section["chart"]["stacked"]
                    chartSrc = self.buildChartImg(data,  section["groupBy"], section["chart"]["type"], stacked)

                htmlSections.append(self.buildHtmlChart(chartSrc, section['sectionTitle'], description))

            print("\n===================================================")

        basetemplate = env.get_template('base_template.html')
        body = '\n<hr/>\n'.join(htmlSections)
        return basetemplate.render(body=body, css=self.baseCss)

    def buildHeader(seld, title, description=''):
        template = env.get_template("header_template.html")
        return template.render(title=title, description=description)

    def buildHtmlTable(self, data, keys, title):
        template = env.get_template('table_template.html')
        return template.render(data=data, dataKeys=keys, title=title)

    def buildMarkup(self, data, markup, title=''):
        markup = "<h3>{{title}}</h3>" + markup
        template = Environment(loader=BaseLoader).from_string(markup)
        return template.render(data=data, title=title)

    def buildHtmlChart(self, chartSrc, title, description=''):
        template = env.get_template('chart_template.html')
        return template.render(chartSrc=chartSrc, title=title, description=description)

    def buildHorizontalImgSimple(self, data, type='horizontalBar'):
        labels = [i['label'] for i in data]
        values = [i['value'] for i in data]
        datasets = [{"data": values}]

        showLegend = True

        if(type == 'horizontalBar'):
            datasets[0]["backgroundColor"] = random.choice(colorPalette)
            showLegend = False

        toJson = {
                    "type": type,
                    "data": {
                        "labels": labels,
                        "datasets": datasets
                    },
                    "options": {
                            "legend": {
                                "display": showLegend
                            }
                        }
                    }

        toJson = json.dumps(toJson)
        qs = urllib.parse.quote(toJson)
        return self.configFile["googleStaticChartsUrl"] + qs

    def buildChartImg(self, data, groupBy, type="bar", stacked=True):
        labels = sorted(set([i['label'] for i in data]))
        values = [i['value'] for i in data]
        groupByData = sorted(set([i[groupBy] for i in data]))

        datasets = []
        tmp = []

        dtmp = dict()
        for l in labels:
            dtmp[l] = []
            for group in groupByData:

                v = 0
                for d in data:
                    if d[groupBy] == group and d["label"] == l:
                        v = d["value"]
                    
                dtmp[l].append(v)

        idx =0
        for d in sorted(dtmp.keys()):
            tdata = {
                    "label": d,
                    "data": dtmp[d]
                }
            if type == "horizontalBar": 
                tdata["backgroundColor"] = colorPalette[idx]

            idx += 1
            datasets.append(tdata)

        toJson = {
                    "type": type,
                    "data": {
                        "labels": groupByData,
                        "datasets": datasets
                    },
                    "options": {
                            "legend": {
                                "display": True
                            }
                        }
                    }
        if(stacked):
            toJson["options"]["scales"] = {
                    "xAxes": [{"stacked": stacked}],
                    "yAxes": [{
                        "stacked": stacked,
                    }],
                }

        toJson = json.dumps(toJson)
        qs = urllib.parse.quote(toJson)
        return self.configFile["googleStaticChartsUrl"] + qs

    
