from api import PetFriends
from settings import *
import os

pf = PetFriends()


def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    """ Проверка возможности получения api-ключа (запрос возвращает статус 200 и в результате содержится слово key)"""
    status, result = pf.get_api_key(email, password)
    assert status == 200
    assert 'key' in result


def test_get_all_pets_with_valid_key(filter=''):
    """ Проверка того, что запрос всех питомцев возвращает не пустой список.
        Для этого сначала необходимо получить api ключ и сохранить его в переменную auth_key.
        Далее необходимо запросить список всех питомцев и проверить, что список не пустой.
        Доступное значение параметра filter - 'my_pets' либо '' """
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status == 200
    assert len(result['pets']) > 0


def test_new_pet_with_valid_data(name='Eevee', animal_type='Pokemon',
                                 age=3, pet_photo='images/eevee.jpg'):
    """Проверка возможности добавления питомца с корректными данными"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    pet_photo = os.path.join(os.path.dirname('C:\Users\User\PycharmProjects\PetFriendsApiTests/\tests'),
                             pet_photo)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status == 200
    assert result['name'] == name


def test_successful_delete_pet(pet_id=''):
    """Проверка возможности удаления питомца"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, "Sylveon", "Pokemon", 2, "images/sylveon.jpg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    assert status == 200
    assert pet_id not in my_pets.values()


def test_successful_update_self_pet_info(name='Eevee', animal_type='PokemonKanto', age=5):
    """Проверка возможности обновления информации о питомце"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'],
                                            name, animal_type, age)
        assert status == 200
        assert result['name'] == name
    else:
        raise Exception("There is no my pets")


def test_get_api_key_for_invalid_email(email=invalid_email, password=valid_password):
    """Проверка возможности получения api-ключа по некорректному email"""
    status, result = pf.get_api_key(email, password)
    assert status == 403
    assert 'key' not in result


def test_get_api_key_for_invalid_password(email=valid_email, password=invalid_password):
    """Проверка возможности получения api-ключа по некорректному паролю"""
    status, result = pf.get_api_key(email, password)
    assert status == 403
    assert 'key' not in result


def test_get_my_pets_with_valid_key(filter='my_pets'):
    """ Проверка возможности запроса списка питомцев пользователя """
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status == 200
    assert len(result['pets']) > 0


def test_failed_get_all_pets_with_invalid_filter(filter='all_pets'):
    """ Проверка возможности запроса списка питомцев по несуществующему значению фильтра (all_pets).
    Тест должен завершиться провалом (failed)"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status == 200
    assert len(result['pets']) > 0


def test_new_pet_with_invalid_age(name='Eevee', animal_type='Pokemon',
                                  age=-3, pet_photo='images/eevee.jpg'):
    """Проверка возможности добавления питомца с некорректными данными (возраст)"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    pet_photo = os.path.join(os.path.dirname('C:\Users\User\PycharmProjects\PetFriendsApiTests/\tests'),
                             pet_photo)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status == 400


def test_failed_new_pet_with_one_empty_field_of_data(name='Eevee', animal_type=None,
                                                     age=3, pet_photo='images/eevee.jpg'):
    """Проверка возможности добавления питомца с одним незаполненным полем (тип животного).
    Тест должен завершиться провалом (failed)"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    pet_photo = os.path.join(os.path.dirname('C:\Users\User\PycharmProjects\PetFriendsApiTests/\tests'),
                             pet_photo)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status == 200
    assert result['name'] == name


def test_failed_delete_pet_with_nonexistent_id(pet_id='123456'):
    """Проверка возможности удаления питомца по несуществующему ID.
    Тест должен завершиться провалом (failed)"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, "Sylveon", "Pokemon", 2, "images/sylveon.jpg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    status, _ = pf.delete_pet(auth_key, pet_id)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    assert status == 200


def test_update_pet_info_with_one_empty_field_of_data(name='Eevee', animal_type='KantoPokemon', age=None):
    """Проверка возможности обновления информации о питомце с одним незаполненным полем (возраст)"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'],
                                            name, animal_type, age)
        assert status == 400
    else:
        raise Exception("There is no my pets")


def test_new_pet_without_photo_with_valid_data(name='Raichu', animal_type='AlolaPokemon', age=5):
    """Проверка возможности добавления питомца без фотографии с корректными данными"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)
    assert status == 200
    assert result['name'] == name


def test_add_photo_of_my_pet(pet_id='', pet_photo='images/sylveon.jpg'):
    """Проверка возможности добавления фото питомца"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    pet_photo = os.path.join(os.path.dirname('C:\Users\User\PycharmProjects\PetFriendsApiTests/\tests'),
                             pet_photo)
    if len(my_pets['pets']) > 0:
        status, result = pf.add_photo_of_pet(auth_key, my_pets['pets'][0]['id'], pet_photo)
        assert status == 200
    else:
        raise Exception("There is no my pets")
