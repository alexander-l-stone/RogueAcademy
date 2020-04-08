from source.entity.character import Character

def test_can_instantiate_character():
    assert Character
    character = Character(0, 1, 1, '@', (255, 255, 255))
    assert isinstance(character, Character)

#TODO: Rework movement tests to work with action queue

def test_character_can_move_legally(test_area):
    character = Character(0, 1, 1, '@', (255, 255, 255))
    test_area.add_object(character)
    if character.can_move(0, 1, 0, test_area):
        character.move(0, 1, 0, test_area)
    assert character.x == 2

def test_character_cannot_move_illegally(test_area):
    character = Character(0, 2, 2, '@', (255, 255, 255))
    test_area.add_object(character)
    if character.can_move(0, 1, 0, test_area):
        character.move(0, 1, 0, test_area)
    assert character.x == 2
