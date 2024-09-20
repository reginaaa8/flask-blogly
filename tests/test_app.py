from unittest import TestCase
from app import app
from models import db, User

# Configure the test database
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test'
app.config['SQLALCHEMY_ECHO'] = False
app.config['TESTING'] = True

class UserViewsTestCase(TestCase):
    """Tests for views for Users."""

    @classmethod
    def setUpClass(cls):
        """Set up application context and initialize the database before tests."""
        with app.app_context():
            db.drop_all()
            db.create_all()

    def setUp(self):
        """Add a sample user before each test."""
        with app.app_context():
            User.query.delete()  # Clear out any users from a previous test
            user = User(first_name="Sandy", last_name="Cheeks", image_url="https://images.unsplash.com/photo-1470130623320-9583a8d06241?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8NHx8c3F1aXJyZWx8ZW58MHx8MHx8fDA%3D")
            db.session.add(user)
            db.session.commit()

            self.user = user

            self.user_id = user.id  # Store the user id for later tests

    def tearDown(self):
        """Clean up the session after each test."""
        with app.app_context():
            db.session.rollback()

    def test_list_users(self):
        """Test if the homepage lists users."""
        with app.test_client() as client:
            resp = client.get("/users")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Sandy', html)

    def test_show_user(self):
        """Test if the user detail page shows the correct user."""
        with app.test_client() as client:
            resp = client.get(f"/users/{self.user.id}")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn(f'{self.user.first_name} {self.user.last_name}', html)

    def test_add_user(self):
        """Test adding a new user."""
        with app.test_client() as client:
            new_user = {"first_name": "Mr.", "last_name": "Krabs", "image_url": "https://images.unsplash.com/photo-1533759587370-e5616b8b6209?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MTJ8fGNyYWJ8ZW58MHx8MHx8fDA%3D"}
            resp = client.post("/users/new", data=new_user, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<li><a href="/users/2">Mr. Krabs</a></li>', html)

    def test_new_user_form(self):
        """Test that the 'Add User' form is displayed."""
        with app.test_client() as client:
            resp = client.get('/users/new')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h1>Add a New User</h1>', html)