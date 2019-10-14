# IPython log file

from collections import defaultdict
vlan_list = defaultdict(list)

vlan_list['switch1'] = [1,2,3]
vlan_list['switch2'] = [2,3,4]

result_list = []
for hostname in vlan_list:
    for item in vlan_list[hostname]:
        result_list.append(item)

print(result_list)

result_list = list(set(result_list))

#result_list = [item for hostname in vlan_list for item in vlan_list[hostname]]


