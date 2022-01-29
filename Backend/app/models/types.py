from enum import Enum, EnumMeta

# https://stackoverflow.com/questions/63335753/how-to-check-if-string-exists-in-enum-of-strings
class MetaEnum(EnumMeta):
    def __contains__(cls, item):
        try:
            cls(item)
        except:
            return False

        return True

class BaseEnum(Enum, metaclass=MetaEnum):
    pass

class Genre(str, BaseEnum):
    ACTION = 'ACTION'
    ADVENTURE = 'ADVENTURE'
    COMEDY = 'COMEDY'
    DOCUMENTARY = 'DOCUMENTARY'
    DRAMA = 'DRAMA'
    FANTASY = 'FANTASY'
    HORROR = 'HORROR'
    MYSTERY = 'MYSTERY'
    ROMANCE = 'ROMANCE'
    SCI_FI = 'SCI-FI'
    THRILLER = 'THRILLER'
    WESTERN = 'WESTERN'

class Platform(str, BaseEnum):
    NETFLIX = 'NETFLIX'
    PRIME = 'PRIME'
    APPLE = 'APPLE'
    DISNEY = 'DISNEY'
    CINEMA = 'CINEMA'
    FILMIN = 'FILMIN'
    HBO = 'HBO'
    HBO_MAX = 'HBO MAX'
    MOVISTAR = 'MOVISTAR PLUS'
