class Grupo(object):
    def __init__(self, name, users):
        self.name = name
        self.users = users

    @staticmethod
    def from_dict(source, users):
        grupo = Grupo(source['name'], users)
        return grupo

    def to_dict(self):
         return {u'name': self.name }

    def to_dict_user(self):
        users = []
        for user in self.users:
            users.append(user.to_dict())
        return users

    def __repr__(self):
        return(
            f'Grupo(name={self.name},users={self.users})'
        )

class User(object):
    def __init__(self, id):
        self.id = id

    def to_dict(self):
        return {u'id':self.id}

    def __repr__(self):
        return(
            f'User(id={self.id})'
        )
    
    @staticmethod
    def from_dict(source):
        user = User(source['id'])
        return user