# users/tests/test_permissions.py
from django.test import TestCase
from django.contrib.auth import get_user_model

User = get_user_model()

class RoleTestCase(TestCase):
    def setUp(self):
        self.admin = User.objects.create_user(
            username="admin1", password="pass", role="admin"
        )
        self.customer = User.objects.create_user(
            username="cust1", password="pass", role="customer"
        )

    def test_users_created_with_roles(self):
        self.assertEqual(self.admin.role, "admin")
        self.assertEqual(self.customer.role, "customer")