from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from apps.accounts.models import UserModel
from .serializers import UserSerializer

class ProfileViewTestCase(APITestCase):
    """
    Test cases for the ProfileView
    """
    def setUp(self):
        self.user = UserModel.objects.create_user(
            username='testuser', email='testuser@example.com', password='testpassword'
        )

    def test_get_profile(self):
        """
        Test that the user can retrieve their own profile
        """
        self.client.force_authenticate(user=self.user)

        url = reverse('profile')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        serializer = UserSerializer(self.user)
        self.assertEqual(response.data, serializer.data)

    def test_update_profile(self):
        """
        Test that the user can update their own profile
        """
        self.client.force_authenticate(user=self.user)

        url = reverse('profile')
        updated_data = {
            'email': 'newemail@example.com',
            'first_name': 'New',
            'last_name': 'User',
        }
        response = self.client.patch(url, updated_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.user.refresh_from_db()
        self.assertEqual(self.user.email, updated_data['email'])
        self.assertEqual(self.user.first_name, updated_data['first_name'])
        self.assertEqual(self.user.last_name, updated_data['last_name'])

    def test_delete_profile(self):
        """
        Test that the user can delete their own profile
        """
        self.client.force_authenticate(user=self.user)

        url = reverse('profile')
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        with self.assertRaises(UserModel.DoesNotExist):
            self.user.refresh_from_db()
