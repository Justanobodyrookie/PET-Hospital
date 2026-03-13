import os
import requests
import time
import json
import boto3
from datetime import datetime
from gmail import send_error
from botocore.exceptions import ClientError

hos = '新北市動物醫院'
try:
	api_key = os.getenv('ASSC')
	url = 'https://places.googleapis.com/v1/places:searchText'
	headers={
		'Content-Type': 'application/json',
		'X-Goog-Api-Key': api_key,
		'X-Goog-FieldMask': 'places.id,places.displayName,places.formattedAddress,places.location,nextPageToken'
	}
	endpoint = os.getenv('MINIO_ENDPOINT')
	access_key = os.getenv('MINIO_USER')
	secret_key = os.getenv('MINIO_PASSWORD')
	bucket_name = 'raw-data'
	s3_client = boto3.client(
		's3',
		endpoint_url=endpoint,
		aws_access_key_id=access_key,
		aws_secret_access_key=secret_key,
		region_name='us-east-1'
	)
	try:
		s3_client.head_bucket(Bucket=bucket_name)
	except ClientError:
		s3_client.create_bucket(Bucket=bucket_name)
	page_token = ''
	count = 0
	page_num = 1
	while True:
		payload={
			'textQuery': f'{hos}'
		}
		if page_token:
			payload['pageToken'] = page_token
		response = requests.post(url, json=payload, headers=headers)
		result = response.json()
		page_token = result.get('nextPageToken')
		date = datetime.now().strftime('%Y-%m')
		s3_key = f"{date}/{hos}_page_{page_num}"
		json_file = json.dumps(result, ensure_ascii=False)
		s3_client.put_object(
			Bucket=bucket_name,
			Key=s3_key,
			Body=json_file,
			ContentType='application/json'
		)
		if not page_token:
			print(f'接下來是Lesson 5')
			print(f'一共是 {count} 間醫院')
			break
		time.sleep(2)
		page_num = page_num + 1
	print(f"已全數寫入MinIO")
except Exception as e:
	send_error(str(e), subject=f"與GoogleAPI串接出問題: {e}")
	print(f"API串接出問題: {e}")