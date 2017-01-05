from django.test import TestCase
from django.urls import reverse

from rango.models import Category


class CategoryMethodTests(TestCase):
    def test_ensure_views_are_positive(self):
        cat = Category(name='test', views=-1, likes=0)
        cat.save()
        self.assertEqual((cat.views >= 0), True)

    def test_slug_line_creation(self):
        cat = Category(name='Random Category String')
        cat.save()
        self.assertEqual(cat.slug, 'random-category-string')


class IndexViewTests(TestCase):
    def test_index_view_with_no_categories(self):
        response = self.client.get(reverse('rango:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "There are no categories present.")
        self.assertQuerysetEqual(response.context['categories'], [])

    def test_index_view_with_categories(self):
        add_cat('test', 1, 1)
        add_cat('tmp', 3, 2)
        add_cat('sdds sdd', 5, 5)
        response = self.client.get(reverse('rango:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "sdds sdd")
        num_cats = len(response.context['categories'])
        self.assertEqual(num_cats, 3)


def add_cat(name, views, likes):
    c = Category.objects.get_or_create(name=name)[0]
    c.views = views
    c.likes = likes
    c.save()
    return c
