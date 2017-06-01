from django.test import TestCase, Client
import unittest


class TestClient(Client):
    csrf_enforced_client = Client(enforce_csrf_checks=True)


class TestGetStudentList(TestCase):
    client_class = TestClient

    # unittest.skip("Not finished")
    # def test_post_response(self):
    #     response = self.client_class.get('/getStudentList/')
    #     print(response)
