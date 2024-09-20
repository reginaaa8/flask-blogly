from unittest import TestCase

from app import app
from models import db, User

# Use test database 
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test'
app.config['SQLALCHEMY_ECHO'] = False

# Make Flask errors be real errors, rather than HTML pages with error info
app.config['TESTING'] = True

# This is a bit of hack, but don't use Flask DebugToolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

db.drop_all()
db.create_all()

class PetViewsTestCase(TestCase):
    """Tests for views for Users."""

    def setUp(self):
        """Add sample user."""

        User.query.delete()

        user = User(first_name="Sandy", last_name="Cheeks", image_url="https://images.unsplash.com/photo-1470130623320-9583a8d06241?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8NHx8c3F1aXJyZWx8ZW58MHx8MHx8fDA%3D")
        db.session.add(user)
        db.session.commit()

        self.id = user.id
        self.user = user
    
    def tearDown(self):
        """Clean up any fouled transaction."""

        db.session.rollback()

    def test_list_users(self):
        with app.test_client() as client:
            resp = client.get("/")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Sandy', html)

    def test_show_user(self):
        with app.test_client() as client:
            resp = client.get(f"/users/{self.id}")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn(f'<h1>{self.first_name} {self.last_name}</h1>', html)
            

    def test_add_user(self):
        with app.test_client() as client:
            new_user = {"first_name": "Mr.", "last_name": "Krabs", "image_url": "https://images.unsplash.com/photo-1533759587370-e5616b8b6209?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MTJ8fGNyYWJ8ZW58MHx8MHx8fDA%3D"}
            resp = client.post("/users/new", data=new_user, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("<li> Mr. Krabs </li>", html)


    def test_show_add_form(self):
        with app.test_client() as client:
            resp = client.get('/users/new')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h1>Add a New User</h1>', html)

            