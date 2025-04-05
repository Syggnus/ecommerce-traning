from decimal import Decimal

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from produtos.models import Categoria, Produto


class CategoriaModelTest(TestCase):
    def test_create_categoria(self):
        """Test creating a new category"""
        categoria = Categoria.objects.create(nome="Eletrônicos")
        self.assertEqual(categoria.nome, "Eletrônicos")
        self.assertEqual(str(categoria), "Eletrônicos")

class ProdutoModelTest(TestCase):
    def setUp(self):
        self.categoria = Categoria.objects.create(nome="Roupas")
        self.image = SimpleUploadedFile(
            name='test_image.jpg',
            content=b'',
            content_type='image/jpeg'
        )
        self.produto = Produto.objects.create(
            nome="Camiseta",
            preco=Decimal('50.00'),
            categoria=self.categoria,
            discount=Decimal('10.00'),
            imagem=self.image
        )

    def test_create_produto(self):
        """Test creating a new product"""
        self.assertEqual(self.produto.nome, "Camiseta")
        self.assertEqual(self.produto.preco, Decimal('50.00'))
        self.assertEqual(self.produto.categoria.nome, "Roupas")
        self.assertEqual(str(self.produto), "Camiseta")

    def test_discounted_price(self):
        """Test the discounted_price method"""
        self.assertEqual(self.produto.discounted_price(), Decimal('45.00'))
        self.produto.discount = Decimal('20.00')
        self.assertEqual(self.produto.discounted_price(), Decimal('40.00'))

class HomeViewTest(TestCase):
    def setUp(self):
        self.categoria1 = Categoria.objects.create(nome="Roupa")
        self.categoria2 = Categoria.objects.create(nome="Eletrônicos")
      
        self.image = SimpleUploadedFile(
            name='test_image.jpg',
            content=b'',
            content_type='image/jpeg'
        )
        
        self.produto1 = Produto.objects.create(
            nome="Camiseta",
            preco=Decimal('50.00'),
            categoria=self.categoria1,
            imagem=self.image
        )
        self.produto2 = Produto.objects.create(
            nome="Calça",
            preco=Decimal('100.00'),
            categoria=self.categoria1,
            imagem=self.image
        )
        self.produto3 = Produto.objects.create(
            nome="Celular",
            preco=Decimal('1000.00'),
            categoria=self.categoria2,
            imagem=self.image
        )

    def test_home_view_status(self):
        """Test the status code of the home view"""
        response = self.client.get('/produtos/')
        self.assertEqual(response.status_code, 200)
        
    def test_home_view_context(self):
        """Test that the home view context contains expected data"""
        response = self.client.get('/produtos/')
        self.assertIn('produtos_recentes', response.context)
        self.assertIn('roupas', response.context)
        
        roupas = response.context['roupas']
        self.assertEqual(roupas.count(), 2)
        for produto in roupas:
            self.assertEqual(produto.categoria.nome, "Roupa")