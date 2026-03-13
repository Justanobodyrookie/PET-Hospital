import os
import requests
import time
api_key = os.getenv('ASSC')
url = 'https://places.googleapis.com/v1/places:searchText'
headers={
	'Content-Type': 'application/json',
	'X-Goog-Api-Key': api_key,
	'X-Goog-FieldMask': 'places.displayName,places.formattedAddress,places.location,nextPageToken'
}
page_token = ''
while True:
	payload={
		'textQuery': '新北市 動物醫院'
	}
	if page_token:
		payload['pageToken'] = page_token
	response = requests.post(url, json=payload, headers=headers)
	result = response.json()
	for d in result.get('places', []):
		address = d['formattedAddress']
		lat = d['location']['latitude']
		lon = d['location']['longitude']
		name = d['displayName']['text']
		print(f"醫院名稱: {name}")
		print(f"醫院地址: {address}")
		print(f"緯度: {lat} | 經度: {lon}")
		print('-' * 10)
	page_token = result.get('nextPageToken')
	if not page_token:
		print(f'一共是 {len(name)} 間醫院')
		print(f'接下來是Lesson 5')
		break
	time.sleep(2)