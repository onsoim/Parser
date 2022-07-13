from Type.code.__BASE__ import __BASE__

import re


class JAVA(__BASE__):
    def getMethod(self, API):
        target  = [ m.start(0) for m in re.finditer(r'[\w ]{1,} ' + API, self.code) ][0]
        bracket = [ m.start(0) for m in re.finditer(r'\{|\}', self.code) ]

        cnt = 0
        marker = -1
        for i in bracket:
            cnt += 1 if self.code[i] == '{' else -1

            if i < target:
                marker = cnt
            elif marker == cnt:
                return self.code[target:i + 1]
