import unittest

from app import app, books


class LibraryAppTests(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()
        self.original_books = [book.copy() for book in books]

    def tearDown(self):
        books[:] = [book.copy() for book in self.original_books]

    def test_home_page_shows_library(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Library Management System", response.data)
        self.assertIn(b"Python Basics", response.data)

    def test_add_book(self):
        response = self.client.post("/books", data={"title": "Testing 101", "author": "Sam Lee"})
        self.assertEqual(response.status_code, 302)
        self.assertTrue(any(b["title"] == "Testing 101" for b in books))

    def test_issue_available_book(self):
        response = self.client.post("/issue/1")
        self.assertEqual(response.status_code, 302)
        self.assertEqual(next(b for b in books if b["id"] == 1)["status"], "Issued")

    def test_return_issued_book(self):
        response = self.client.post("/return/3")
        self.assertEqual(response.status_code, 302)
        self.assertEqual(next(b for b in books if b["id"] == 3)["status"], "Available")

if __name__ == "__main__":
    unittest.main()
