from value_objects import Name

class Person:
    def __init__(self, name: Name):
        self.name = name


def test_fahad_is_harry():
    fahad = Person(Name("Fahad", "Naveed"))
    fahad_clone = Person((Name("Fahad", "Naveed")))
    harry = fahad

    harry.name = Name("Harry", "Bombo")
    assert hash(harry) == hash(fahad)
    print(hash(fahad), hash(fahad_clone))
    assert fahad == fahad_clone