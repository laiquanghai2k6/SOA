from flask import Flask,request,jsonify

app = Flask(__name__)
BOOKS = [{"id":1,"title":"Clean Code","author":"R. Martin","year":2005}]
_next = 2
def find(bid):
    return next((b for b in BOOKS if b["id"] == bid), None)

# LIST — GET /books
@app.route("/books", methods=["GET"])
def list_books():
    size = request.args.get("limit",100)
    q = request.args.get("q","")
    sort=request.args.get("sort","")
    result = BOOKS.copy()
    if q:
        result = [b for b in BOOKS if q in b['title'].lower() or q in b["author"].lower()]

    if sort == 'title':
        result = sorted(result,key = lambda x:x['title'].lower())
    return jsonify(result[:size]), 200
# DETAIL — GET /books/<int:id>
@app.route("/books/<int:bid>", methods=["GET"])
def get_book(bid):
    book = find(bid)
    if not book: return {"error":"not found"}, 404
    return jsonify(book), 200
# CREATE — POST /books
@app.route("/books", methods=["POST"])
def create_book():
    global _next
    body = request.get_json(silent=True) or {}
    t, a, y = body.get("title"), body.get("author"), body.get('year')


    if not t or not a or y is None:
        return jsonify({"error": "need title, author, and year"}), 400

    if not isinstance(y, int) or y < 1900: 
        return jsonify({"error": "year phai >= 1900"}), 400
    
    book = {"id":_next, "title":t, "author":a,"year": y}
    _next += 1; BOOKS.append(book)
    return jsonify(book), 201, {"Location":f"/books/{book['id']}"}
# UPDATE — PUT, DELETE — DELETE (xem bên phải)
@app.route("/books/<int:bid>", methods=["PUT", "DELETE"])
def modify_book(bid):
    book = find(bid)
    if not book: return {"error":"not found"}, 404
    if request.method == "PUT":
        body = request.get_json(silent=True) or {}

        if "year" in body:
            y = body["year"]
            if not isinstance(y, int) or y < 1900:
                return jsonify({"error": "year phai >= 1900"}), 400

        book.update(body)
        return jsonify(book), 200
    BOOKS.remove(book)
    return"", 204



if __name__ == "__main__":
    app.run(host='127.0.0.1',port=5000)