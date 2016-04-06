
import re

class CTruncateNum(float):
    def __init__(self,num):
        self.t = num
    def ChopNum(self):
        #Convert number to output format and wirte into output.txt file

        #truncate average_degree to 2 decimal float
        str1=str("%.3f" % self.t)
        str2='.'
        #write into output.txt in new line
        result = str1[:str1.index(str2)+3]+'\n'
        return result