import csv_handle
import node
import numpy

x_dist = 270
y_dist = 225

def create_scene(list,person_id):
    pos_list = state_machine(list,person_id)

    n_list = {}
    for l in range(len(pos_list)):
        attr = list[pos_list[l][2]].fetch()
        print(attr[0])
        n_list[l] = (node.Actor(attr[0],attr[1],attr[2],attr[3],attr[4],attr[5],attr[6],attr[7],attr[8],attr[9]))
        n_list[l].setPos(pos_list[l][0],pos_list[l][1])
    print('done')
    return n_list

def state_machine(list,person_id):
    pos_list = []
    t = True
    state = 0
    level = 0
    track = False
    cur_pos = [0,0]
    heirarchy = []
    s_heirarchy = []
    heirarchy.append(person_id)
    while t:
        if state == 0:
            person = get_first_spouse(list,heirarchy[-1],cur_pos,level)
            if person != '':
                cur_pos = person[0:2]
                s_heirarchy.append(person[2])
                pos_list.append(person)
                track = False

                state = 1
            else:
                state = 3
        elif state == 1:
            level += 1
            person =  get_first_kid(list,heirarchy[-1],s_heirarchy[-1],cur_pos,level)
            if person != '':
                cur_pos = person[0:2]
                heirarchy.append(person[2])
                pos_list.append(person)
                state = 0
                track = True
            else:
                state = 2
        elif state == 2:
            if track:
                cur_pos = [cur_pos[0] + x_dist, cur_pos[1]]
                track = False
            level -= 1
            person = get_next_spouse(list,heirarchy[-1],s_heirarchy[-1],cur_pos,level)
            s_heirarchy.pop()
            if person != '':
                cur_pos = person[0:2]
                s_heirarchy.append(person[2])
                pos_list.append(person)
                state = 0
            elif level == 0:
                t = False
            else:
                state = 3
        elif state == 3:
            person = get_next_kid(list,heirarchy[-2],s_heirarchy[-1],heirarchy[-1],cur_pos,level)
            heirarchy.pop()
            if person != '':
                cur_pos = person[0:2]
                heirarchy.append(person[2])
                pos_list.append(person)
                track = False
                state = 0
            else:
                cur_pos = [cur_pos[0], cur_pos[1] - y_dist]
                state = 2

    for p in pos_list:
        p.pop()
    return pos_list



def get_first_spouse(list,person_id,cur_pos,level):
    l = []
    l.append(cur_pos[0] + x_dist)
    l.append(cur_pos[1])
    l.append(list[person_id].marriage[-1][1:4])
    l.append(level)
    if l[2] != '000':
        return l
    else:
        return ''

def get_first_kid(list,person_id,spouse,cur_pos,level):
    l = []
    l.append(cur_pos[0] - x_dist)
    l.append(cur_pos[1] + y_dist)
    for i in list[person_id].children:
        if i in list[spouse].children:
            l.append(i)
            break
    else:
        l.append('')
    l.append(level)
    if l[2] != '':
        return l
    else:
        return ''

def get_next_spouse(list,person_id,spouse,cur_pos,level):
    l = []
    l.append(cur_pos[0] + x_dist)
    l.append(cur_pos[1])
    for a, i in enumerate(reversed(list[person_id].marriage)):
        if a > 0 and i[1:4] == spouse:
            l.append(list[person_id].marriage[a-1])
            l.append(level)
            return l
    return ''

def get_next_kid(list,person_id,spouse,kid,cur_pos,level):
    l = []
    l.append(cur_pos[0] + x_dist)
    l.append(cur_pos[1])
    next = False
    for i in list[person_id].children:
        if i in list[spouse].children:
            if next:
                l.append(i)
                break
            if i == kid:
                next = True
    else:
        l.append('')
    l.append(level)
    if l[2] != '':
        return l
    else:
        return ''

def siblings(list,person_id):
    father = list[person_id].father_id
    mother = list[person_id].mother_id

    c_father = list[father].children
    c_mother = list[mother].children

    l = []
    count = 0
    for i in c_father:
        for j in c_mother:
            if (i == j) and j != person_id:
                s = []
                s.append(-200 - (count * 120))
                count += 1
                s.append(0)
                s.append(j)
                l.append(s)

    return l

def spouse(list,pos,person):
    a_list = list[person].marriage
    s_list = []
    for m in a_list:
        a = m.split('_')[0]
        s_list.append(a)

    final_list = []
    count = 1
    for i in reversed(s_list):
        s = []
        s.append(pos[0] + (count * 270))
        count += 1
        s.append(pos[1])
        s.append(i[1:])
        final_list.append(s)

    return final_list

def kids(list,person_id,spouse,pos,singular=False):
    offset = 135 if singular else 270
    kid_list = []
    tot_list = []
    for a in list[person_id].children:
        for b in list[person_id].children:
            if a == b:
                kid_list.append(a)
                tot_list.append(a)
                m_list = []
                if list[a].marriage != ['S000']:
                    for m in reversed(list[a].marriage):
                        x = m.split('_')[0]
                        tot_list.append(x[1:])
    pos_list = []
    for i, j in enumerate(tot_list):
        l = []
        max_pos = i * 270
        l.append(max_pos)
        l.append(pos[1] + 225)
        l.append(tot_list[i])
        pos_list.append(l)

    for i in range(len(pos_list)):
        pos_list[i][0] = pos_list[i][0] - (max_pos / 2) + offset
    print(pos_list)

if __name__ == '__main__':
    people = csv_handle.load('Family tree test.csv')

    # print(siblings(people,'00H'))
    # print(spouse(people,[0,0],'00Y'))
    # kids(people,'00T','00U',[0,0])
    # get_pos(people,'002')
    # get_first_kid(people,'00Y',[0,0],1)
    # state_machine(people,'009')

    x = create_scene(people,'002')
    print(x)