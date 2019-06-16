import re
import os

class PrePro:    
    @staticmethod
    def filter(code):
        code = re.sub("('.*?)\n", '\n', code)
        code = os.linesep.join([s for s in code.splitlines() if s.split()])
        return code