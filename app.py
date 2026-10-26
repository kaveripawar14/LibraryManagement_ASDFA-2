from flask import Flask, request, redirect, url_for, render_template_string

app = Flask(__name__)

# Simple in-memory sample data for a classroom demonstration.
books = [
    {"id": 1, "title": "Python Basics", "author": "John Smith", "status": "Available"},
    {"id": 2, "title": "Web Development", "author": "Mary Jones", "status": "Available"},
    {"id": 3, "title": "Data Structures", "author": "Alex Brown", "status": "Issued"},
]

PAGE = """
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Library Management System</title>
<style>
*{box-sizing:border-box} body{font-family:Arial,sans-serif;background:#f3f6fb;margin:0;color:#1f2937}
header{background:#173b67;color:white;padding:26px 8%;} header h1{margin:0 0 8px}
main{max-width:1000px;margin:28px auto;padding:0 18px}
.card{background:white;padding:22px;border-radius:12px;box-shadow:0 4px 16px #102a4312;margin-bottom:20px}
form{display:flex;gap:10px;flex-wrap:wrap} input{padding:11px;border:1px solid #cbd5e1;border-radius:7px;flex:1;min-width:160px}
button{padding:11px 15px;border:0;border-radius:7px;background:#176b4d;color:white;cursor:pointer;font-weight:bold}
table{width:100%;border-collapse:collapse} th,td{text-align:left;padding:13px;border-bottom:1px solid #e5e7eb}
th{background:#edf3f8}.status{font-weight:bold}.available{color:#16804a}.issued{color:#b45309}
.actions{display:flex;gap:7px;flex-wrap:wrap}.actions form{display:inline}
.small{color:#64748b;font-size:14px}
@media(max-width:650px){table{font-size:13px}th,td{padding:8px}}
</style>
</head>
<body>
<header><h1>📚 Library Management System</h1><div>Manage books, issue books and record returns</div></header>
<main>
{% with messages = get_flashed_messages() %}{% if messages %}<div class="card">{{ messages[0] }}</div>{% endif %}{% endwith %}
<section class="card">
<h2>Add a Book</h2>
<form action="{{ url_for('add_book') }}" method="post">
<input name="title" placeholder="Book title" required>
<input name="author" placeholder="Author name" required>
<button type="submit">Add Book</button>
</form>
<p class="small">Demo application: sample data resets when the server restarts.</p>
</section>
<section class="card">
<h2>Book Catalogue ({{ books|length }} books)</h2>
<table><thead><tr><th>ID</th><th>Title</th><th>Author</th><th>Status</th><th>Action</th></tr></thead>
<tbody>{% for book in books %}
<tr><td>{{ book.id }}</td><td>{{ book.title }}</td><td>{{ book.author }}</td>
<td class="status {{ 'available' if book.status == 'Available' else 'issued' }}">{{ book.status }}</td>
<td><div class="actions">
{% if book.status == 'Available' %}
<form action="{{ url_for('issue_book', book_id=book.id) }}" method="post"><button type="submit">Issue</button></form>
{% else %}
<form action="{{ url_for('return_book', book_id=book.id) }}" method="post"><button type="submit">Return</button></form>
{% endif %}
</div></td></tr>{% endfor %}</tbody></table>
</section>
</main></body></html>
"""

@app.get("/")
def index():
    return render_template_string(PAGE, books=books)

@app.post("/books")
def add_book():
    title = request.form.get("title", "").strip()
    author = request.form.get("author", "").strip()
    if title and author:
        next_id = max((book["id"] for book in books), default=0) + 1
        books.append({"id": next_id, "title": title, "author": author, "status": "Available"})
    return redirect(url_for("index"))

@app.post("/issue/<int:book_id>")
def issue_book(book_id):
    book = next((b for b in books if b["id"] == book_id), None)
    if book and book["status"] == "Available":
        book["status"] = "Issued"
    return redirect(url_for("index"))

@app.post("/return/<int:book_id>")
def return_book(book_id):
    book = next((b for b in books if b["id"] == book_id), None)
    if book and book["status"] == "Issued":
        book["status"] = "Available"
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
