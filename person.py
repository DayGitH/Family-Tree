import datetime

months = {'01':'Jan', '02':'Feb', '03':'Mar', '04':'Apr', '05':'May', 
          '06':'Jun', '07':'Jul', '08':'Aug', '09':'Sep', '10':'Oct', 
          '11':'Nov', '12':'Dec'}

class person():
    id = '000'
    nick_name = 'JD'
    real_name = 'John Doe'
    bday = '1000'
    birth = ''
    gender = 'X'
    father_id = '000'
    mother_id = '000'
    marriage = 'S000'
    children = ''
    dday = '1000'
    death = ''
    imp_flg = 0
    notes = 'Holmes'
    
    age = 100
    
    def __init__(self,id,nick_name,real_name,bday,gender,father_id,mother_id,
                 marriage,children,dday,imp_flg,notes):
        self.id = id
        self.nick_name = nick_name
        self.real_name = real_name
        self.bday = bday
        self.gender = gender
        self.father_id = father_id
        self.mother_id = mother_id
        self.marriage = marriage
        self.children = children
        self.dday = dday
        self.imp_flg = imp_flg
        self.notes = notes
        
        self.processBday()
        if self.dday:
            self.processDday()
            
        
    def update(self,parameter,value):
        if parameter == 'nick_name':
            self.nick_name = value
        elif parameter == 'real_name':
            self.real_name = value
        elif parameter == 'bday':
            self.bday = value
            self.processBday()
            if self.dday:
                self.processDday()
        elif parameter == 'gender':
            self.gender = value
        elif parameter == 'father_id':
            self.father_id = value
        elif parameter == 'mother_id':
            self.mother_id = value
        elif parameter == 'marriage':
            self.marriage = value
        elif parameter == 'children':
            self.children = value
        elif parameter == 'dday':
            self.dday = value
            if self.dday:
                self.processDday()
            else:
                self.death = ''
        elif parameter == 'imp_flg':
            self.imp_flg = value
        elif parameter == 'notes':
            self.notes = value
        else:
            print('bad parameter')
            
    def display(self):
        print('''ID: {}\nName: {}\nFull Name: {}\nBirthday: {}\nGender: {}\nFather ID: {}\nMother ID: {}\nMarriage: {}\nChildren: {}\nDeath: {}\nImportant: {}\nNotes: {}'''
              .format(self.id, self.nick_name, self.real_name, self.birth,
                      self.gender, self.father_id, self.mother_id, self.marriage,
                      self.children, self.death, self.imp_flg, self.notes))
        
    def fetch(self):
        return self.id, self.nick_name, self.real_name, self.bday, \
               self.gender, self.father_id, self.mother_id, self.marriage, \
               self.children, self.dday, self.imp_flg, self.notes
    
    def get_father(self):
        return self.father_id
    
    def get_mother(self):
        return self.mother_id
    
    def get_children(self):
        return self.children
    
    def get_birthday(self):
        return self.birth
    
    def get_deathday(self):
        return self.death
    
    def processBday(self):
        l = []
        year = ''
        month = ''
        day = ''
        if len(self.bday) >= 4 and self.bday[0:4] != 'xxxx':
            year = int(self.bday[0:4])
            l.append(self.bday[0:4])
        if len(self.bday)>= 6:
            month = int(self.bday[4:6])
            l.append(months[self.bday[4:6]])
        if len(self.bday) >= 8:
            day = int(self.bday[6:8])
            l.append(self.bday[6:8])
            
        self.birth = '-'.join(l)  
        
        now = datetime.datetime.now()
        self.age = -1
        if year:
            if month:
                if day:
                    if (now.month > month) or (now.month == month and now.day >= day):
                        self.age = now.year - year
                    else:
                        self.age = now.year - year - 1
                else:
                    if now.month >= month:
                        self.age = now.year - year
                    else:
                        self.age = now.year - year - 1
            else:
                self.age = now.year - year
        
    def processDday(self):
        l = []
        b_year = ''
        b_month = ''
        b_day = ''
        d_year = ''
        d_month = ''
        d_day = ''        
        if len(self.bday) >= 4 and self.bday[0:4] != 'xxxx':
            b_year = int(self.bday[0:4])
        if len(self.bday)>= 6:
            b_month = int(self.bday[4:6])
        if len(self.bday) >= 8:
            b_day = int(self.bday[6:8])
        if len(self.dday) >= 4:
            d_year = int(self.dday[0:4])
            l.append(self.dday[0:4])
        if len(self.dday)>= 6:
            d_month = int(self.dday[4:6])
            if len(l) == 1:
                l.append(months[self.dday[4:6]])
        if len(self.dday) >= 8:
            d_day = int(self.dday[6:8])
            if len(l) == 2:
                l.append(self.dday[6:8])
                
        self.death = '-'.join(l)
            
        self.age = -1
        if b_year and d_year:
            if b_month and d_month:
                if b_day and d_day:
                    if (d_month > b_month) or (d_month == b_month and d_day >= b_day):
                        self.age = d_year - b_year
                    else:
                        self.age = d_year - b_year - 1
                else:
                    if d_month >= b_month:
                        self.age = d_year - b_year
                    else:
                        self.age = d_year - b_year - 1
            else:
                self.age = d_year - b_year
  
if __name__ == '__main__':      
    bob = person('001','Bob','Robert','19820101','M','002','003','004','','203001',True,'This isn\'t really Robert')
    bob.display()
    
    #[id, nick_name, real_name, bday, gender, father_id, mother_id, marriage, children, dday, imp_flg, notes] = bob.fetch()
    
    print(bob.get_father())