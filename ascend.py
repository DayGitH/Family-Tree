import csv_handle
import node
import numpy

def create_scene(list,person_id):
    pos_list = get_pos(person_id,list,get_up_levels(list,person_id))
    print(pos_list)

    n_list = {}
    for l in range(len(pos_list)):
        if pos_list[l][2] == '':
            pass
        else:
            attr = list[pos_list[l][2]].fetch()
            n_list[l] = (node.Actor(attr[0],attr[1],attr[2],attr[3],attr[4],attr[5],attr[6],attr[7],attr[8],attr[9]))
            n_list[l].setPos(pos_list[l][0],pos_list[l][1])
    print('done')
    return n_list
    
def get_up_levels(list,person_id):
    if not (list[person_id].get_father() and list[person_id].get_mother()):
        return 1
    else:
        a1 = 0
        a2 = 0
        if list[person_id].get_father():
            a1 = get_up_levels(list,list[person_id].get_father())
        if list[person_id].get_mother():
            a2 = get_up_levels(list,list[person_id].get_mother())
        
        return max(a1,a2) + 1

def get_pos(p_id,p_list,level):
    l = {}
    n = level
    x_dist = 270
    y_dist = -225
    x = 2 ** (n - 1)
    diff = 2 ** (n - 1)
    for i in range((2 ** level) - 1):
        if i < 2 ** (level - 1):
            l[i] = [0 + (x_dist * i), y_dist * (n - 1)]
            count = -2 ** (level - 1)
            flip = False
        elif i == (2 ** level) - 2:
            l[i] = [numpy.mean([l[i-1][0], l[i-2][0]]), 0]
        else:
            if i == x:
                n -= 1
                x += 2 ** (n - 1)
            
            if not flip:
                l[i] = [numpy.mean([l[i+count][0], l[i+count+1][0], l[i+count+2][0], l[i+count+3][0]]) - (x_dist / 2), y_dist * (n - 1)]
                flip = not flip
            elif flip:
                l[i] = [numpy.mean([l[i+count-1][0], l[i+count][0], l[i+count+1][0], l[i+count+2][0]]) + (x_dist / 2), y_dist * (n - 1)]
                flip = not flip
                count += 2

            #l[i] = [numpy.mean([l[i-diff][0], l[i-diff+1][0]]), 200 * (n - 1)]
    l_str = lineage_str(level)
    for i in reversed(range((2 ** level) - 1)):
        if i == (2 ** level) - 2:
            l[i].append(p_id)
        else:
            x = lineage(p_list,p_id,l_str[len(l) - i - 2])
            l[i].append(x)

    x_offset = l[len(l)-1][0]
    print(x_offset)
    for i in l:
        l[i][0] -= x_offset
    return l

def lineage_str(level):
    l = []
    if level == 1:
        return l
    l.append('f')
    l.append('m')
    
    if level > 2:
        size = 1
        for i in range(level - 2):
            temp_list = []
            for element in l:
                if len(element) == size:
                    temp_list.append(element + 'f')
                    temp_list.append(element + 'm')
            size += 1
                
            l += temp_list
    
    return l

def lineage(ppl_list,ppl_id,string):
    if ppl_id == '':
        return ''
    elif string.lower() == 'm':
        return ppl_list[ppl_id].get_father()
    elif string.lower() == 'f':
        return ppl_list[ppl_id].get_mother()
    else:
        g = string[0]
        if g.lower() == 'm':
            return lineage(ppl_list,ppl_list[ppl_id].get_father(),string[1:])
        elif g.lower() == 'f':
            return lineage(ppl_list,ppl_list[ppl_id].get_mother(),string[1:])


if __name__ == '__main__':
    people = csv_handle.load('Family tree test.csv')
    
    #print(get_up_levels(people,'008'))
    # print(lineage_str(5))
    # print(lineage(people,'008','ff'))
    x = create_scene(people,'002')
    print(x)