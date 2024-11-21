from django.test import TestCase, Client
from django.urls import reverse
from restaurant.models import Menu

class MenuViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.menu_item = Menu.objects.create(
            name='IceCream',
            price=80,
            inventory=100,
            menu_item_description='testing'
        )
        self.list_url = reverse('menu')  # Nom de la vue pour la liste
        self.detail_url = reverse('menu_item', args=[self.menu_item.id])  # Vue détail

    def test_menu_list_view(self):
        """Test de la vue pour afficher la liste des éléments du menu."""
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'IceCream')  # Vérifie si le nom apparaît dans la réponse


