import os

from flask import Flask, request
from flask_cors import CORS, cross_origin

import firebase_admin
from firebase_admin import credentials, db, storage

from google.cloud import storage as gcs
from google.oauth2 import service_account

from dotenv import load_dotenv
import detect

# .env ファイルをロードして環境変数へ反映
load_dotenv()

app = Flask(__name__)
app.config['CORS_HEADERS'] = 'Content-Type'
CORS(app, resources={r"/*": {"origins": "*"}})

# firebaseの初期設定
credential = credentials.Certificate("./firebase-adminsdk.json")
firebase_database_url = os.getenv('FIREBASE_DATABASE_URL')
firebase_bucket = os.getenv('FIREBASE_BUCKET')
firebase_admin.initialize_app(credential, {
    'databaseURL': firebase_database_url,
    'databaseAuthVariableOverride': {
        'uid': 'my-service-worker'
    },
    'storageBucket': firebase_bucket
})

# gcpの設定
project_id = os.getenv('PROJECT_ID')
key_path = os.getenv('GOOGLE_CREDENTIALS')
credential = service_account.Credentials.from_service_account_file(key_path)
client = gcs.Client(project_id, credentials=credential)
bucket_name = os.getenv('BUCKET_NAME')
bucket = client.get_bucket(bucket_name)
gcp = {
    'client': client,
    'bucket_name': bucket_name,
    'bucket': bucket
}

@app.route('/', methods=['POST'])
def hello():
    return "Hello world!!"

@app.route('/download', methods=['POST'])
def download():
    post_data = request.json
    user_id = post_data['userId']
    timestamp = post_data['timestamp']
    print('user_id')
    print(user_id)
    print('timestamp')
    print(timestamp)
    detect.download_blob(gcp, user_id, timestamp)
    return "OK"

@app.route('/predict', methods=['POST'])
def predict():
    post_data = request.json
    user_id = post_data['userId']
    timestamp = post_data['timestamp']
    detect.main(gcp, user_id, timestamp)
    return "OK"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)