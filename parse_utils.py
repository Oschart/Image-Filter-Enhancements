#%%
import re

trans_format = '''
Please insert a list of your transformations in the following format:
...<trans_key ...args>
Available transormations:
<TRANS offset>
<SCALE Sx Sy>
<ROT angle Px Py>
<NTHP n>
<HE>
'''

def parse_trans(trans_str):
    ptrans = re.findall(r'\<(.*?)\>', trans_str)
    sep_trans = []
    for trans in ptrans:
        sp = trans.split(' ')
        sep_trans.append([sp[0], [float(st) for st in sp[1:]]])
    return sep_trans

#print(parse_trans("<TRANS ssss sss> <SCALE >"))
# %%
