import typing


def lmap(func, *iterables):
    return list(map(func, *iterables))


def line_to_num_list(string_in,base=10):
    out = []
    curnum = ""
    for ch in string_in.lower():
        if ord(ch) >= ord('0') and ord(ch) <= ord('9'):
            curnum += ch
        elif base > 10 and ord(ch) >= ord('a') and ord(ch) <= (ord('a')+(base-11)):
            curnum += ch
        else:
            if len(curnum) > 0:
                out.append(int(curnum,base=base))
            curnum = ""
    if len(curnum) > 0: # handle the case where the line ends while parsing a number
        out.append(int(curnum,base=base))
    return out
    

def make2dList(val=None, width=10, height=20):
  return [[val for i in range(width)] for j in range(height)]
