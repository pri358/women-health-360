from run import app
import unittest


class FlaskTest(unittest.TestCase):

    # check for response code
    def test_home(self):
        tester = app.test_client(self)
        response = tester.get("/home")
        statusCode = response.status_code
        self.assertEqual(statusCode, 200)

    # check for response content
    def test_home_content(self):
        tester = app.test_client(self)
        response = tester.get("/home")
        self.assertTrue(b'Welcome' in response.data)


if __name__ == '__main__':
    unittest.main()
