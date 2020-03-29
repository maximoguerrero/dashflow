import unittest, os, sys, json

sys.path.insert(0, '../libs')
import compiler

cwd = os.getcwd()

configFile = os.path.realpath(os.path.join(cwd, "test-config.json"))
configPath = os.path.dirname(configFile)

with open(configFile) as f:
    configFile = json.load(f)


class TestCompiler(unittest.TestCase):

    def testConfigTest(self):
        comp = compiler.Compiler(configFile, configPath)

        self.assertIsNot(comp, None)
        self.assertIsNot(comp.getConfig(), None)
        self.assertIsNot(comp.getConfigPath(), None)

    def testBuildTest(self):
        comp = compiler.Compiler(configFile, configPath)
        html = comp.build()

        self.assertIsNot(html, None)
        self.assertTrue(len(html) > 0)
        self.assertIn(configFile["title"], html)
        self.assertTrue("quickcharts.dashflow.io/chart" in html)

    def testDataTest(self):
        comp = compiler.Compiler(configFile, configPath)
        section = configFile["sections"][0]
        data = comp.getData(section)

        self.assertIsNot(data, None)
        self.assertTrue(len(data) > 0)
        self.assertIsNot(comp.buildHtmlTable(data, data[0].keys(), section["sectionTitle"]), None)


if __name__ == '__main__':
    unittest.main()
