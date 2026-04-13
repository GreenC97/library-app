from flask_cors import CORS
from pymongo import MongoClient
from datetime import datetime
app = Flask(__name__)
CORS(app)
client = MongoClient("mongodb+srv://Banasafari:library20090@cluster0.qst4mml.mongodb.net/?appName=Cluster0")
db = client["library"]
books = db["books"]
loans = db["loans"]
@app.route("/scan", methods=["POST"])
def scan_barcode():
    data = request.json
    barcode = data.get("barcode")
    book = books.find_one({"barcode": barcode})
    if not book:
        return jsonify({"error": "Book not found"}), 404
    return jsonify({"title": book["title"], "status": book["status"]})
@app.route("/checkout", methods=["POST"])
def checkout():
    data = request.json
    barcode = data.get("barcode")
    borrower = data.get("borrower")
    book = books.find_one({"barcode": barcode})
    if not book or book["status"] == "checked_out":
        return jsonify({"error": "Unavailable"}), 400
    books.update_one({"barcode": barcode}, {"$set": {"status": "checked_out"}})
    loans.insert_one({
        "barcode": barcode,
        "borrower": borrower,
        "checkout_date": datetime.now(),
        "return_date": None})
    return jsonify({"message": f"Checked out to {borrower}"})
@app.route("/return", methods=["POST"])
def return_book():
    data = request.json
    barcode = data.get("barcode")
    books.update_one({"barcode": barcode}, {"$set": {"status": "available"}})
    loans.update_one(
        {"barcode": barcode, "return_date": None},
        {"$set": {"return_date": datetime.now()}})
    return jsonify({"message": "Book returned"})
@app.route("/return", methods=["POST"])
def return_book_v2():
    data = request.json
    barcode = data.get("barcode")
    books.update_one({"barcode": barcode}, {"$set": {"status": "available"}})
    loans.update_one(
        {"barcode": barcode, "return_date": None},
        {"$set": {"return_date": datetime.now()}} )
    return jsonify({"message": "Book returned"})
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    app.run(host="0.0.0.0", port=port)
