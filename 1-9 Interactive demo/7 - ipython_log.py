# IPython log file

string = 'switchport mode access'

import re
if re.search(r'switchport mode (\w+)',string):
    match = re.search(r'switchport mode (\w+)', string)
    value = format(match.group(1))

class ReSearcher(object):
    match = None

    def __call__(self, pattern, string):
        self.match = re.search(pattern, string)
        return self.match

    def __getattr__(self, name):
        return getattr(self.match, name)
        
string = 'switchport mode trunk'
match = ReSearcher()
    
if match(r'switchport mode (\w+)',string):
    value = format(match.group(1))
    
