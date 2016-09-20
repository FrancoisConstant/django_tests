from django.test.testcases import TestCase as DjangoTest
from django_webtest import WebTest
from rest_framework import status
from rest_framework.test import APITestCase as DrfTest


class TestMixin(object):

    def reload_object(self, obj):
        return obj.__class__.objects.get(id=obj.id)

    def reload_objects(self, *objects):
        return [self.reload_object(obj) for obj in objects]

    def assert_query_set_equals(self, qs, result):
        self.assertQuerysetEqual(qs, map(repr, result), ordered=False)


class ApiTest(DrfTest, TestMixin):
    """
    For all DRF tests.
    Abstract out `self.client`
    + `test_login_required`
    + `test_cannot_delete`
    """

    @property
    def base_path(self):
        raise NotImplementedError("ex: /api/requests/")

    def get_path(self, obj=None):
        if obj is not None:
            return "{base_path}{id}/".format(base_path=self.base_path, id=obj.id)
        else:
            return self.base_path

    def login(self, user):
        return self.client.force_login(user)

    def get(self, path, user=None, status_code=status.HTTP_200_OK, print_response=False):
        """ shortcut for login + client.get(...) + status checked """
        if user is not None:
            self.login(user)
        response = self.client.get(path)

        # debug
        if print_response:
            print(response)
            print(response.json())

        self.assertEquals(response.status_code, status_code)
        return response

    def post(self, path, data, user, status_code=status.HTTP_201_CREATED, print_response=False):
        """ shortcut for login + client.post(...) + status checked """
        self.login(user)
        response = self.client.post(path, data=data)

        # debug
        if print_response:
            print(response)
            print(response.json())

        self.assertEquals(response.status_code, status_code)
        return response

    def put(self, path, data, user, status_code=status.HTTP_200_OK, print_response=False):
        """ shortcut for login + client.put(...) + status checked """
        self.login(user)
        response = self.client.put(path, data=data)

        # debug
        if print_response:
            print(response)
            print(response.json())

        self.assertEquals(response.status_code, status_code)
        return response
        
    def options(self, path, user, status_code=status.HTTP_200_OK, print_response=False):
        """ shortcut for login + client.options(...) + status checked """
        self.login(user)
        response = self.client.options(path)

        # debug
        if print_response:
            print(response)
            print(response.json())

        self.assertEquals(response.status_code, status_code)
        return response

    def delete(self, path, user, status_code=status.HTTP_204_NO_CONTENT, **extra):
        self.login(user)
        response = self.client.delete(path=path, user=user, **extra)
        self.assertEquals(response.status_code, status_code)

    def test_login_required(self):
        self.get(self.get_path(), user=None, status_code=status.HTTP_403_FORBIDDEN)

    def test_cannot_delete(self):
        raise NotImplementedError("We need to make sure that no one can delete anything via the API")


class SimpleTest(DjangoTest, TestMixin):
    pass


class RegularTest(WebTest, TestMixin):
    pass
