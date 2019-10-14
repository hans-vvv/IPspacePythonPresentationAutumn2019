# IPython log file

portinfo = {}
portinfo['speed'] = '100'
portinfo['switchport mode'] = 'access'
portinfo #display dict

portinfo.pop('switchport mode')
portinfo # display dict
portinfo['speed'] # returns value of '100'
portinfo['switchport mode'] # returns KeyError

portinfo.get('switchport mode') # returns None
portinfo.get('switchport mode') == None # returns True
'switchport mode' in portinfo.keys() # returns False
'speed' in portinfo.keys() # return True
portinfo['switchport mode'] = 'trunk'

portinfo

for k in portinfo:
    print(k)
    
for k,v in portinfo.items():
    print('The key is "{}" and the value is "{}"'.format(k,v))
