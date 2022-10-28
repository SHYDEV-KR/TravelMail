import requests
import json
import datetime

from private import private 

private_keys = private.my_keys()

headers = {
    "Authorization": f"{private_keys['notion_api_token']}",
    "Accept": "application/json",
    "Notion-Version": "2022-06-28"
}

def get_queries_from_database(database_id, body={}):
  notion_api_url = f'https://api.notion.com/v1/databases/{database_id}/query'
  response = requests.post(notion_api_url, json=body, headers=headers)

  if response.status_code == 200:
    json_data = json.loads(response.text)
    return json_data['results']
  else:
    print(response.text)
    return None


def retrieve_page(page_id):
  notion_api_url = f'https://api.notion.com/v1/pages/{page_id}'
  response = requests.get(notion_api_url, headers=headers)

  if response.status_code == 200:
    json_data = json.loads(response.text)
    return json_data
  else:
    return f"Error : {response.status_code}"


def get_order_data_from_single_query(json_data):
  properties_json = json_data['properties']
  currency_code = properties_json['currency_code']['select']['name']
  departure_date = properties_json['departure_date']['date']['start']
  arrival_date = properties_json['arrival_date']['date']['start']
  
  if datetime.datetime(*map(int, arrival_date.split("-"))) < datetime.datetime(*map(int, departure_date.split("-"))):
    return f"Invalid Date"

  departure_city_id = properties_json['departure_city']['relation'][0]['id']
  departure_city_properties = retrieve_page(departure_city_id)['properties']
  departure_city = {
    'name' : departure_city_properties['name']['title'][0]['plain_text'],
    'code_eng' : departure_city_properties['code_eng']['rich_text'][0]['plain_text'],
  }
  arrival_city_id = properties_json['arrival_city']['relation'][0]['id']
  arrival_city_properties = retrieve_page(arrival_city_id)['properties']
  arrival_city = {
    'name' : arrival_city_properties['name']['title'][0]['plain_text'],
    'code_eng' : arrival_city_properties['code_eng']['rich_text'][0]['plain_text'],
  }

  user_ids = [user_id_dict['id'] for user_id_dict in properties_json['users']['relation']]
  users = []
  for user_id in user_ids:
    email = retrieve_page(user_id)['properties']['email']['email']
    users.append(email)

  url = f"https://flights.myrealtrip.com/air/b2c/AIR/INT/AIRINTSCH0100100010.k1?initform=RT&domintgubun=I&depctycd={departure_city['code_eng']}&depctycd={arrival_city['code_eng']}&depctycd=&depctycd=&depctynm={departure_city['name']}&depctynm={arrival_city['name']}&depctynm=&depctynm=&arrctycd={arrival_city['code_eng']}&arrctycd={departure_city['code_eng']}&arrctycd=&arrctycd=&arrctynm={arrival_city['name']}&arrctynm={departure_city['name']}&arrctynm=&arrctynm=&depdt={departure_date}&depdt={arrival_date}&depdt=&depdt=&opencase=N&opencase=N&opencase=N&openday=&openday=&openday=&depdomintgbn=I&secrchType=FARE&maxprice=&availcount=250&tasktype=B2C&adtcount=2&chdcount=0&infcount=0&cabinclass=Y&nonstop=Y&freebag=&orgDepctycd=&orgDepctycd=&orgDepctycd=&orgDepctycd=&orgArrctycd=&orgArrctycd=&orgArrctycd=&orgArrctycd=&orgPreferaircd=&preferaircd=&KSESID=air%3Ab2c%3ASELK138RB%3ASELK138RB%3A%3A00"
  order = {
    "departure_city" : departure_city,
    "currency_code" : currency_code,
    "departure_date" : departure_date,
    "arrival_date" : arrival_date,
    "departure_city" : departure_city,
    "arrival_city" : arrival_city,
    "users" : users,
    "url" : url,
  }
  
  return order


def generate_new_page_in_currency_db(db_id, currencies, date=datetime.datetime.today()):
  request_url = "https://api.notion.com/v1/pages"
  body_data = {
    "parent" : { "database_id" : db_id },
    "properties": {
                    "JPY": {
                        "number": currencies["JPY"]
                    },
                    "date": {
                        "date": {
                            "start": f"{date.year}-{str(date.month).zfill(2)}-{str(date.day).zfill(2)}"
                        }
                    },
                    "USD": {
                        "number": currencies["USD"]
                    },
                    "": {
                        "title": []
                    }
                }
  } 

  response = requests.post(request_url, json=body_data, headers=headers)
  if response.status_code == 200:
    json_data = json.loads(response.text)
    return json_data
  else:
    return f"{response.status_code} Error"