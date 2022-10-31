from django.test import TestCase, Client
from django.urls import reverse
from website.models import Spot

class WebsiteViews(TestCase):
    """testing the views of the Website App"""
    def setUp(self):
        """creating some objects for the tests"""
        self.client = Client()
        self.search_url = reverse('search')
        category1 = Category.objects.create(name='category1')
        category2 = Category.objects.create(name='category2')
        Product.objects.create(name='test1', category=category1, nutriscore=15)
        Product.objects.create(name='test2', category=category1, nutriscore=10)
        Product.objects.create(name='test3', category=category1, nutriscore=25)
        Product.objects.create(name='test4', category=category1, nutriscore=15)
        Product.objects.create(name='test5', category=category2, nutriscore=5)
        Product.objects.create(name='test6', category=category2, nutriscore=15)

    #TEST SEARCH VIEWS
    def test_search_do_not_exist(self):
        """Testing when the search find no product match at all"""
        response = self.client.get(self.search_url, {'name':'dontExist'})
        self.assertTrue(response.context['error'])

    def test_search_perfect_fit_with_alt(self):
        """Testing when a product is named exactly like the search string
        !!! not case-sensible
        AND the product found got alternatives products
        """
        response = self.client.get(self.search_url, {'name':'tEsT3'})
        self.assertTrue(response.context['product'])
        self.assertTrue(response.context['alternatives'])
        self.assertEqual(len(response.context['alternatives']), 3)

    def test_search_perfect_fit_without_alt(self):
        """Testing when a product is named exactly like the search string
        !!! not case-sensible
        AND the product found got NO alternative product
        """
        response = self.client.get(self.search_url, {'name':'teSt2'})
        self.assertTrue(response.context['product'])
        self.assertTrue(response.context['no_alternatives'])

    def test_search_unmatching_with_multiple_find(self):
        """Testing when the research has no perfect fit but got several
        products that may match
        !!! not case-sensible
        """
        response = self.client.get(self.search_url, {'name': 'tEst'})
        self.assertEqual(len(response.context['products']), 6)

    def test_search_unmatching_with_one_find(self):
        """Testing when the research has no perfect fit but got 1 product
        that may match
        !!! not case-sensible
        """
        response = self.client.get(self.search_url, {'name': 'eSt1'})
        self.assertTrue(response.context['product'])

    #TEST PRODUCT VIEW
    def test_product_do_not_exist(self):
        """Testing when the product doesn't exist at all"""
        url = reverse('product', kwargs={'product_name':'Test15'})
        response = self.client.get(url)
        self.assertTrue(response.context['error'])

    def test_product_perfect_fit_with_alt(self):
        """Testing when the product got alternative products
        !!! not case-sensible
        """
        url = reverse('product', kwargs={'product_name':'Test3'})
        response = self.client.get(url)
        self.assertTrue(response.context['product'])
        self.assertTrue(response.context['alternatives'])
        self.assertEqual(len(response.context['alternatives']), 3)

    def test_product_perfect_fit_without_alt(self):
        """Testing when a product got no alternative product
        !!! not case-sensible
        """
        url = reverse('product', kwargs={'product_name':'Test5'})
        response = self.client.get(url)
        self.assertTrue(response.context['product'])
        self.assertTrue(response.context['no_alternatives'])