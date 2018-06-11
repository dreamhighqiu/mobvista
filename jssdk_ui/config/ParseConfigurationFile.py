#-*-coding:utf-8-*-
from ConfigParser import  ConfigParser
from VarConfig import pageElementLocatorPath
class ParseConfigfile(object):
    def __init__(self):
        self.cf =ConfigParser()
        self.cf.read(pageElementLocatorPath)

    def getItemSection(self,sectionName):
        optionsDict = dict(self.cf.items(sectionName))
        return  optionsDict
    def getOptionValue(self,sectionName,optionName):
        value = self.cf.get(sectionName,optionName)
        return value
if __name__ == "__main__":
    pc = ParseConfigfile()
    print (pc.getItemSection("jssdk_bv"))

    print (pc.getOptionValue("jssdk_bv","jssdk_video"))



