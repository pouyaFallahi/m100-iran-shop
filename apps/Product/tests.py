from django.test import TestCase
from .models import Category, Company, Product


class ModelsTestCase(TestCase):
    def setUp(self):
        category = Category.objects.create(name_category='Test Category')
        company = Company.objects.create(company_name='Test Company', datil='Test Details', email='test@example.com')
        product = Product.objects.create(name_product='Test Product', datil='Test Details', price=100, many=10,
                                         categotory=category, company=company)
        return category, company, product

    def test_category_str(self):
        category = Category.objects.get(name_category='Test Category')
        self.assertEqual(str(category), 'Test Category')

    def test_company_str(self):
        company = Company.objects.get(company_name='Test Company')
        self.assertEqual(str(company), 'Test Company')

    def test_product_str(self):
        product = Product.objects.get(name_product='Test Product')
        self.assertEqual(str(product), 'Test Product')

    # add Products

    def test_add_product_to_database(self):
        # ایجاد یک محصول جدید
        category, company, product = self.setUp()

        # بررسی وجود محصول در دیتابیس
        self.assertIsNotNone(product.id)

        # بررسی صحت مقادیر وارد شده
        self.assertEqual(product.name_product, 'Test Product')
        self.assertEqual(product.price, 100)
        self.assertEqual(product.many, 10)
        self.assertEqual(product.categotory, category)
        self.assertEqual(product.company, company)
