import os
import uuid
from User import *
class Tool:

    def __init__(self, toolName, toolBrand, toolOwner = '', dayRate = 0):

        self.tool_name = toolName
        self.tool_brand = toolBrand
        self.tool_owner = toolOwner
        self.day_rate = dayRate

    def __str__(self):
        var += self.tool_name + '\n' + self.tool_brand + '\n' + str(self.day_rate)
        return var

    def __repr__(self):
        var += self.tool_name + '\n' + self.tool_brand + '\n' + str(self.day_rate)
        return var
#------------------------------------------------------------------
    def getToolName(self):
        return self.tool_name

    def getToolBrand(self):
        return self.tool_brand
    
    def getToolOwner(self):
        return self.tool_owner

    def getDayRate(self):
        return self.day_rate
    
    def createTool(toolName, toolBrand, toolOwner, dayRate):
        
        nTool = Tool(toolName, toolBrand, toolOwner, dayRate)
        
        nTool.buildFile()
        filePath = Tool.Path('tooldata')
        storedtools = []
        for file in os.listdir(filePath):
            if file.endswith(".txt"):
                with open(filePath+file,'r') as myfile:
                    tooldata = myfile.readlines()
                    tooldata = tooldata[1].strip('\n') #stored names in memory,
                                                       #could be a class but im lazy
                    storedtools.append(tooldata)        
#------------------------------------------------------------------
    def readFile(self):
        filePath = self.Path()
        fileName = filePath + str(self.toolName)
        with open(fileName + '.txt' , 'r') as myfile:
            data = myfile.readlines()
        
    def buildFile(self):
        filePath = self.Path()
        self.createToolFile(filePath)
        fileName = filePath + '/' + str(self.tool_name)
        self.writeTTF(fileName)

    def createToolFile(self, filePath):          
        if not os.path.exists(filePath):
            os.makedirs(filePath)

    def writeTTF(self, fileName):      
        output_file = open(fileName + '.txt', 'w')
        output_file.write(self.tool_name + '\n'
                          + self.tool_brand + '\n'
                          + self.day_rate + '\n'
                          + self.tool_owner + '\n'
                            )
        output_file.close()
        
    def Path(self):
        return 'ToolData/'


