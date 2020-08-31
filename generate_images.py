import os
import requests

GSTATIC_API_KEY = "API_KEY"
AWS_ACCESS_KEY = ""
AWS_SECRET_KEY = ""

# In case you want to save the dataset to s3
# session = boto3.session.Session(region_name='eu-north-1', 
#                                 aws_access_key_id=AWS_ACCESS_KEY, 
#                                 aws_secret_access_key='AWS_SECRET_KEY')
# s3_client = session.client('s3', config=boto3.session.Config(signature_version='s3v4'))

input_ = []
with open("sweden_input.csv", encoding='utf8') as inc:
    for stuff in inc:        
        input_.append(stuff.split(","))
        
hashmap_ = {}     
for i in range(1, len(input_)):
    hashmap_[input_[i][0]] = {'Lat': input_[i][5], 'Long': input_[i][6]}

session = requests.Session()

for i in hashmap_:

    coordinates = hashmap_[i]["Lat"] + "," + hashmap_[i]["Long"]
    uri = (f"https://maps.googleapis.com/maps/api/staticmap?center={coordinates}"
           f"&zoom=17&size=700x700&scale=4&format=PNG32&maptype=satellite"
           f"&key={GSTATIC_API_KEY}")
    
    try:
            response = session.get(uri)
            # session_id = session.cookies.get_dict()
            # cookies = response.cookies
            # headers = response.headers
            with open(f"{i}.png", 'wb') as output_bytes:
                output_bytes.write(response.content)
            # upload to s3
            # try:
            #     s3_client.put_object(Bucket="msc-s3", Key=f"Sweden-v2/{i}.png", Body=response.content)
            # except ClientError as error_:
            #     with open("errors_s3","a", encoding='utf8') as output:
            #         output.write(f"Error {error_} when uploading image {i}\n")
    
    except Exception as exc:
        with open("errors_os","a", encoding='utf8') as output:
            output.write(f"Error {exc} when saving image {i}\n")