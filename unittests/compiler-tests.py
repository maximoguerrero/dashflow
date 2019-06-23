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
        self.assertTrue(comp is not None)
        self.assertTrue(comp.getConfig() is not None)
        self.assertTrue(comp.getConfigPath() is not None)

    def testBuildTest(self):
        comp = compiler.Compiler(configFile, configPath)
        self.assertTrue(comp.build() is not None)
        self.assertTrue(len(comp.build()) > 0)

    def testDataTest(self):
        comp = compiler.Compiler(configFile, configPath)
        self.assertTrue(comp.getData(configFile["sections"][0]) is not None)
        self.assertTrue(len(comp.getData(configFile["sections"][0])) > 0)



if __name__ == '__main__':
    unittest.main()