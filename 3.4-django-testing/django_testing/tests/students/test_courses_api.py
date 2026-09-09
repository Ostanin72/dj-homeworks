import pytest
from model_bakery import baker

from rest_framework.test import APIClient

from students.models import Student, Course


# Фикстура для api-client
@pytest.fixture
def client():
    return APIClient()


# Фикстура для фабрики курсов
@pytest.fixture
def course_factory():
    def factory(*args, **kwargs):
        return baker.make(Course, *args, **kwargs)

    return factory


# Фикстура для фабрики студентов
@pytest.fixture
def student_factory():
    def factory(*args, **kwargs):
        return baker.make(Student, *args, **kwargs)

    return factory


# проверка получения первого курса (retrieve-логика)
@pytest.mark.django_db
def test_get_course(client, course_factory):
    course = course_factory(_quantity=1)[0]

    response = client.get(f'/api/v1/courses/{course.id}/')

    assert response.status_code == 200
    assert response.json()['id'] == course.id
    assert response.json()['name'] == course.name


# проверка получения списка курсов (list-логика)
@pytest.mark.django_db
def test_get_courses(client, course_factory):
    courses = course_factory(_quantity=10)

    response = client.get('/api/v1/courses/')

    assert response.status_code == 200
    assert len(response.json()) == 10


# проверка фильтрации списка курсов по `id`
@pytest.mark.django_db
def test_get_course_id(client, course_factory):
    courses = course_factory(_quantity=10)
    target_course = courses[5]

    response = client.get(f'/api/v1/courses/?id={target_course.id}')

    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]['id'] == target_course.id


# проверка фильтрации списка курсов по `name`
@pytest.mark.django_db
def test_get_course_name(client, course_factory):
    courses = course_factory(_quantity=10)
    target_course = courses[5]

    response = client.get(f'/api/v1/courses/?name={target_course.name}')

    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]['name'] == target_course.name


# тест успешного создания курса
@pytest.mark.django_db
def test_post_course(client):

    response = client.post(
        '/api/v1/courses/',
        data={'name': 'test'}
    )

    assert response.status_code == 201

    response_data = response.json()
    assert response_data['name'] == 'test'

    list_response = client.get('/api/v1/courses/')
    assert list_response.status_code == 200

    list_data = list_response.json()
    assert list_data[0]['name'] == 'test'


# тест успешного обновления курса
@pytest.mark.django_db
def test_patch_course(client, course_factory):
    courses = course_factory(_quantity=10)
    target_course = courses[5]

    response = client.patch(
        f'/api/v1/courses/{target_course.id}/',
        data={'name': 'updated_test_name'}
    )

    assert response.status_code == 200

    response_data = response.json()
    assert response_data['id'] == target_course.id
    assert response_data['name'] == 'updated_test_name'

    get_response = client.get(f'/api/v1/courses/{target_course.id}/')
    assert get_response.status_code == 200

    get_data = get_response.json()
    assert (
            get_data['name'] == 'updated_test_name'
            and get_data['id'] == target_course.id
    )


# тест успешного удаления курса
@pytest.mark.django_db
def test_delete_course(client, course_factory):
    courses = course_factory(_quantity=10)
    target_course = courses[5]

    response = client.delete(f'/api/v1/courses/{target_course.id}/')

    assert response.status_code == 204

    get_response = client.get('/api/v1/courses/{target_course.id}/')
    assert get_response.status_code == 404

    list_response = client.get('/api/v1/courses/')
    assert list_response.status_code == 200
    assert len(list_response.json()) == 9
