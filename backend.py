from pymongo import MongoClient
import gridfs

uri = "mongodb+srv://Prasham:passpass@cluster0.aopixi8.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(uri)
db = client['new']
c = db["user"]
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


if __name__ == "__main__":
    file_id = upload_pdf('test.pdf')
    print(f'Uploaded file with ID: {file_id}')

    # # Download the PDF file
    download_pdf(file_id, 'save.pdf')
    print('File downloaded successfully')
    pass