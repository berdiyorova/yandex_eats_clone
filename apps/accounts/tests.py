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
        # Create a test user
        self.user = UserModel.objects.create_user(
            username='testuser', email='testuser@example.com', password='testpassword'
        )

    def test_get_profile(self):
        """
        Test that the user can retrieve their own profile
        """
        # Log in the test user
        self.client.force_authenticate(user=self.user)

        # Send a GET request to the profile endpoint
        url = reverse('profile')
        response = self.client.get(url)

        # Assert that the response has a status code of 200 (OK)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Assert that the response data matches the user's serialized data
        serializer = UserSerializer(self.user)
        self.assertEqual(response.data, serializer.data)

    def test_update_profile(self):
        """
        Test that the user can update their own profile
        """
        # Log in the test user
        self.client.force_authenticate(user=self.user)

        # Send a PATCH request to the profile endpoint with updated data
        url = reverse('profile')
        updated_data = {
            'email': 'newemail@example.com',
            'first_name': 'New',
            'last_name': 'User',
        }
        response = self.client.patch(url, updated_data, format='json')

        # Assert that the response has a status code of 200 (OK)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Assert that the user's profile has been updated
        self.user.refresh_from_db()
        self.assertEqual(self.user.email, updated_data['email'])
        self.assertEqual(self.user.first_name, updated_data['first_name'])
        self.assertEqual(self.user.last_name, updated_data['last_name'])

    def test_delete_profile(self):
        """
        Test that the user can delete their own profile
        """
        # Log in the test user
        self.client.force_authenticate(user=self.user)

        # Send a DELETE request to the profile endpoint
        url = reverse('profile')
        response = self.client.delete(url)

        # Assert that the response has a status code of 204 (No Content)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Assert that the user has been deleted from the database
        with self.assertRaises(UserModel.DoesNotExist):
            self.user.refresh_from_db()
