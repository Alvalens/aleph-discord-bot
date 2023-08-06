from client import RestClient
from dotenv import load_dotenv
import os
import time


load_dotenv()

# get login data
login = os.getenv("login")
password = os.getenv("password")

if login is None or password is None:
    print("You have not set your login details in the .env file")
    exit()
elif login == "" or password == "":
    print("You have not set your login details in the .env file")
    exit()

# try to connect to the API
try:
    client = RestClient(login, password)
    print("Connected to the API")
except:
    print("Failed to connect to the API")
    exit()

post_data = dict()
def task(keyword):
    # image search
    post_data[len(post_data)] = dict(
        language_code="en",
        location_code=2840,
        keyword=keyword,
        depth=1,
        max_crawl_pages=1,
        
    )

    try:
        response = client.post("/v3/serp/google/images/task_post", post_data)

        task_id = response["tasks"][0]["id"]
        # task_id = "08060347-6480-0066-0000-61fdf042832e"
        print(f"task id: {task_id}")
        # wait until task is completed
        while True:
            try:
                response = client.get(
                    f"/v3/serp/google/images/task_get/advanced/{task_id}")
                if 'result' in response['tasks'][0] and response['tasks'][0]['result'] is not None:
                    break
                else:
                    print(f"waiting for completion...")
                    time.sleep(5)

            except Exception as e:
                print(f"Error making API request: {e}")
                exit()
        # access results image url
        result = response['tasks'][0]['result'][0]['items'][1]['source_url']
        print(result)
        return result
                    

    except Exception as e:
        print(f"Error making API request: {e}")
        exit()





