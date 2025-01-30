from flask import Flask, request, jsonify
from pymongo import MongoClient
import gridfs

app = Flask(__name__)

# Connect to MongoDB
uri = "mongodb+srv://Prasham:passpass@cluster0.aopixi8.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(uri)
db = client['new']
users_collection = db["user"]
fs = gridfs.GridFS(db)
print('Success connection.')


# Helper Function: Authenticate User
def authenticate(username, password):
    user = users_collection.find_one({"username": username})
    if user and user["password"] == password:
        return user
    return None

# Route: Register User (For Testing Purposes)
@app.route("/register", methods=["GET","POST"])
def register():
    username = request.form.get("username")
    password = request.form.get("password")
    
    if not username or not password:
        return jsonify({"error": "Missing user fields"}), 400

    if users_collection.find_one({"username": username}):
        return jsonify({"error": "User already exists"}), 409

    users_collection.insert_one({
        "username": username,
        "password": password,
        "pdfs": []  # Initialize empty PDF list
    })
    return jsonify({"message": "User registered successfully"}), 201

# Route: List all PDFs
@app.route("/user/pdfs", methods=["POST"])
def list_pdfs():
    username = request.form.get("username")
    password = request.form.get("password")
    
    if not username or not password:
        return jsonify({"error": "Missing user fields"}), 400

    user = authenticate(username, password)
    
    if not user:
        return jsonify({"error": "Invalid credentials"}), 401

    a = [fs.get(x).filename for x in user.get("pdfs", []) ]
    return jsonify({"pdfs": a}), 200

# Route: Add a PDF
@app.route("/user/add_pdf", methods=["POST"])
def add_pdf():
    username = request.form.get("username")
    password = request.form.get("password")
    if not username or not password:
        return jsonify({"error": "Missing user fields"}), 400

    user = authenticate(username, password)
    
    if not user:
        return jsonify({"error": "Invalid credentials"}), 401

    if "file" not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files["file"]

    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    if not file.filename.endswith(".pdf"):
        return jsonify({"error": "Invalid file type, only PDFs allowed"}), 400
    
    # Save PDF file
    file_id = fs.put(file, filename=file.filename)
    users_collection.update_one(
        {"username": username},
        {"$push": {"pdfs": file_id}}
    )
    
    return jsonify({"message": "File uploaded successfully", "file_name": file.filename}), 200

# Route: Remove a PDF
@app.route("/user/remove_pdf", methods=["PUT"])
def remove_pdf():
    username = request.form.get("username")
    password = request.form.get("password")
    pdf_id = request.form.get("pdf_id")

    if not username or not password or not pdf_id:
        return jsonify({"error": "Missing user fields"}), 400

    user = authenticate(username, password)
    
    if not user:
        return jsonify({"error": "Invalid credentials"}), 401

    if pdf_id not in user["pdfs"]:
        return jsonify({"error": "PDF not found"}), 404

    users_collection.update_one(
        {"username": username},
        {"$pull": {"pdfs": "pdf_id"}}
    )
    return jsonify({"message": "PDF removed successfully"}), 200

# Run Flask App
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
