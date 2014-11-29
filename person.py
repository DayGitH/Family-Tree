class person():
    id = '000'
    nick_name = 'JD'
    real_name = 'John Doe'
    bday = '1000'
    gender = 'X'
    father_id = '000'
    mother_id = '000'
    marriage = 'S000'
    children = ''
    death_dte = '1000'
    imp_flg = 0
    notes = 'Holmes'
    
    def __init__(self,id,nick_name,real_name,bday,gender,father_id,mother_id,
                 marriage,children,death_dte,imp_flg,notes):
        self.id = id
        self.nick_name = nick_name
        self.real_name = real_name
        self.bday = bday
        self.gender = gender
        self.father_id = father_id
        self.mother_id = mother_id
        self.marriage = marriage
        self.children = children
        self.death_dte = death_dte
        self.imp_flg = imp_flg
        self.notes = notes
        
    def update(self,parameter,value):
        if parameter == 'nick_name':
            self.nick_name = value
        elif parameter == 'real_name':
            self.real_name = value
        elif parameter == 'bday':
            self.bday = value
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
        elif parameter == 'death_dte':
            self.death_dte = value
        elif parameter == 'imp_flg':
            self.imp_flg = value
        elif parameter == 'notes':
            self.notes = value
            
    def display(self):
        print('''ID: {}\nName: {}\nFull Name: {}\nBirthday: {}\nGender: {}\nFather ID: {}\nMother ID: {}\nMarriage: {}\nChildren: {}\nDeath: {}\nImportant: {}\nNotes: {}'''
              .format(self.id,self.nick_name,self.real_name,self.bday,
                      self.gender,self.father_id,self.mother_id,self.marriage,
                      self.children,self.death_dte,self.imp_flg,self.notes))
        
    def fetch(self):
        return self.id, self.nick_name, self.real_name, self.bday, self.gender, self.father_id, self.mother_id, self.marriage, self.children, self.death_dte, self.imp_flg,self.notes
  
if __name__ == '__main__':      
    bob = person('001','Bob','Robert','1982','M','002','003','004','','',True,'This isn\'t really Robert')
    bob.display()
    
    [id, nick_name, real_name, bday, gender, father_id, mother_id, marriage, children, death_dte, imp_flg, notes] = bob.fetch()
    
    x = 'asd'