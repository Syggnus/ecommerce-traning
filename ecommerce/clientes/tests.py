from clientes.forms import UserCreateForm
from clientes.models import User
from django.test import TestCase
from django.urls import reverse


class UserModelTest(TestCase):
    def test_create_user(self):
        """Test creating a regular user"""
        user = User.objects.create_user(
            email="test@example.com",
            password="testpass123"
        )
        self.assertEqual(user.email, "test@example.com")
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_admin)
        self.assertFalse(user.is_staff)
        self.assertEqual(str(user), "test@example.com")

    def test_create_superuser(self):
        """Test creating a superuser"""
        admin_user = User.objects.create_superuser(
            email="admin@example.com",
            password="adminpass123"
        )
        self.assertEqual(admin_user.email, "admin@example.com")
        self.assertTrue(admin_user.is_active)
        self.assertTrue(admin_user.is_admin)
        self.assertTrue(admin_user.is_staff)

class UserCreateFormTest(TestCase):
    def test_form_with_valid_data(self):
        """Test form with valid data"""
        form = UserCreateForm({
            'email': 'newuser@example.com',
            'password': 'newpass123'
        })
        self.assertTrue(form.is_valid())
        
    def test_form_with_missing_data(self):
        """Test form with missing data"""
        form = UserCreateForm({
            'email': '',
            'password': 'newpass123'
        })
        self.assertFalse(form.is_valid())
        self.assertTrue('email' in form.errors)

class UserCreateViewTest(TestCase):
    def test_view_url_exists(self):
        """Test that the user creation URL exists"""
        response = self.client.get('/clientes/cadastrar/')
        self.assertEqual(response.status_code, 200)
        
    def test_view_uses_correct_template(self):
        """Test that the view uses the correct template"""
        response = self.client.get('/clientes/cadastrar/')
        self.assertTemplateUsed(response, 'criar_cliente.html')
        
    def test_user_creation(self):
        """Test that a user can be created through the view"""
        response = self.client.post('/clientes/cadastrar/', {
            'email': 'viewtest@example.com',
            'password': 'viewpass123'
        })
 
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(email='viewtest@example.com').exists())

class UserLoginTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="logintest@example.com",
            password="loginpass123"
        )
        
    def test_login_successful(self):
        """Test successful login"""
        response = self.client.post('/clientes/entrar/', {
            'username': 'logintest@example.com',
            'password': 'loginpass123'
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.wsgi_request.user.is_authenticated)
        
    def test_login_unsuccessful(self):
        """Test unsuccessful login"""
        response = self.client.post('/clientes/entrar/', {
            'username': 'logintest@example.com',
            'password': 'wrongpassword'
        })
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.wsgi_request.user.is_authenticated)