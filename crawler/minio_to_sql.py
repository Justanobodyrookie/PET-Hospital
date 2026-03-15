import os
import json
import boto3
import pymysql
from gmail import send_error
from synax import db_config, sql_insert

try:
	conn = pymysql.connect(**db_config)
	cursor = conn.cursor()
	endpoint = os.getenv('MINIO_ENDPOINT')
	access_key = os.getenv('MINIO_USER')
	secret_key = os.getenv('MINIO_PASSWORD')
	bucket_name = 'raw-data'
	s3 = boto3.client(
		's3',
		endpoint_url=endpoint,
		aws_access_key_id=access_key,
		aws_secret_access_key=secret_key,
		region_name='us-east-1'
		)
	response = s3.list_objects_v2(Bucket=bucket_name)
	stuff = []
	if 'Contents' in response:
		for obj in response['Contents']:
			s = obj['Key']
			file = s3.get_object(Bucket=bucket_name, Key=s)
			fie = file['Body'].read().decode('utf-8')
			fi = json.loads(fie)
			for a in fi.get('places', []):
				place_id = a['id']
				a_name = a['displayName']['text']
				if '預約' in a_name or '約診' in a_name:
					reg_type = 1
				else:
					reg_type = 0
				if '醫院' in a_name:
					cut_point = a_name.find('醫院') + 2
					name = a_name[:cut_point]
				else:
					name = a_name
				address = a.get('formattedAddress', '無地址資訊')
				if 'No' in address:
					start_point = address.find('No')
					address = address[start_point:]
				lat = a['location']['latitude']
				lon = a['location']['longitude']
				location_WKT = f"point({lon} {lat})"
				cursor.execute(sql_insert, (place_id, name, address, str(location_WKT), reg_type))
	conn.commit()
	cursor.close()
	conn.close()
except Exception as e:
	send_error(str(e), subject=f"寫進MySQL出問題: {e}")
	print(f"寫進MySQL出問題: {e}")