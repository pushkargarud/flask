import unittest
from app import app, db, Name  # Import your Flask app, db, and models

class FlaskTestCase(unittest.TestCase):
    # Set up the app for testing
    def setUp(self):
        # Use a temporary database for testing (in-memory SQLite database)
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        self.app = app.test_client()  # Create a test client for sending requests
        self.app_context = app.app_context()  # Create the app context
        self.app_context.push()  # Push the app context

        # Create tables
        db.create_all()

    # Tear down the testing environment
    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    # Test if the home route is rendering correctly
    def test_home(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Enter Your Name', response.data)  # Check if "Enter Your Name" text is present

    # Test the result route for handling POST requests and saving data
    def test_result_post(self):
        response = self.app.post('/result', data={'name': 'John Doe'})
        print(response.data)  # Print the response content
        self.assertEqual(response.status_code, 302)  # Should redirect to /names
        self.assertEqual(response.location, '/names')  # Check redirection URL

    # Test if the /names route displays saved names
    def test_all_names(self):
        # First, add a name
        self.app.post('/result', data={'name': 'John Doe'})
        
        # Now, test the /names route to ensure the name appears
        response = self.app.get('/names')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'John Doe', response.data)  # Check if the name is in the response

if __name__ == '__main__':
    unittest.main()
