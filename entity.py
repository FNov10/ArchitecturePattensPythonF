from value_objects import Name

class Person:
    def __init__(self, name: Name):
        self.name = name


def test_fahad_is_harry():
    fahad = Person(Name("Fahad", "Naveed"))
    harry = fahad

    harry.name = Name("Harry", "Bombo")
    assert hash(harry) == hash(fahad)
    assert fahad is harry