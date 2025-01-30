
from flask import Flask, request, jsonify
from pymongo import MongoClient
import gridfs
app = Flask(__name__)

uri = "mongodb+srv://Prasham:passpass@cluster0.aopixi8.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(uri)
db = client['new']
user_collection = db["user"]
fs = gridfs.GridFS(db)
print('Success connection.')

# Function to upload PDF file
def upload_pdf(file_path):
    with open(file_path, 'rb') as f:
        file_id = fs.put(f, filename=file_path)
    return file_id

# Function to download PDF file
def download_pdf(file_id, output_path):
    file_data = fs.get(file_id).read()
    with open(output_path, 'wb') as f:
        f.write(file_data)



# Route: Register User
@app.route("/register", methods=["POST"])
def register_user():
    data = request.json
    if not data or not all(k in data for k in ("username", "password", "pdfs")):
        return jsonify({"error": "Missing fields"}), 400

    if users_collection.find_one({"username": data["username"]}):
        return jsonify({"error": "User already exists"}), 409

    users_collection.insert_one(data)
    return jsonify({"message": "User registered successfully"}), 201

# Route: Get User Details
@app.route("/user/<username>", methods=["GET"])
def get_user(username):
    user = users_collection.find_one({"username": username}, {"_id": 0})
    if not user:
        return jsonify({"error": "User not found"}), 404
    return jsonify(user), 200

# Route: Update PDFs for User
@app.route("/user/<username>", methods=["PUT"])
def update_pdfs(username):
    data = request.json
    if "pdfs" not in data:
        return jsonify({"error": "PDF list is required"}), 400

    result = users_collection.update_one(
        {"username": username}, {"$set": {"pdfs": data["pdfs"]}}
    )
    if result.matched_count == 0:
        return jsonify({"error": "User not found"}), 404

    return jsonify({"message": "PDF list updated"}), 200

# Route: Delete User
@app.route("/user/<username>", methods=["DELETE"])
def delete_user(username):
    result = users_collection.delete_one({"username": username})
    if result.deleted_count == 0:
        return jsonify({"error": "User not found"}), 404
    return jsonify({"message": "User deleted successfully"}), 200





# Run the Flask app
if __name__ == "__main__":
    app.run(debug=True)


