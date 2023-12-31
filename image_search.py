import asyncio
from client import RestClient
from dotenv import load_dotenv
import os
import random
import sys

load_dotenv()

# get login data
login = os.getenv("login")
password = os.getenv("password")

if login is None or password is None:
    print("You have not set your login details in the .env file")
    sys.exit()
elif login == "" or password == "":
    print("You have not set your login details in the .env file")
    sys.exit()

# try to connect to the API
try:
    client = RestClient(login, password)
    print("Connected to the API")
except:
    print("Failed to connect to the API")
    sys.exit()


async def task(keyword):
    """
    Performs an image search for the given keyword using the API.

    Args:
        keyword (str): The keyword to search for.

    Returns:
        A list of image URLs.
    """
    # image search
    post_data = dict()
    post_data[0] = dict(
        language_code="en",
        location_code=2840,
        keyword=keyword,
        depth=1,
        max_crawl_pages=1,
    )

    try:
        response = await client.post_async("/v3/serp/google/images/task_post", post_data)

        task_id = response["tasks"][0]["id"]
        # task_id = "08060347-6480-0066-0000-61fdf042832e"
        print(f"task id: {task_id}")
        # wait until task is completed
        while True:
            try:
                response = await client.get_async(f"/v3/serp/google/images/task_get/advanced/{task_id}")
                if 'result' in response['tasks'][0] and response['tasks'][0]['result'] is not None:
                    task_id = response["tasks"][0]["id"]
                    result = response['tasks'][0]['result'][0]['items']
                    # get all image urls
                    images = []
                    if result is None:
                        print("Image not found")
                        return None
                    for i in range(len(result)):
                        if result[i]['type'] == 'images_search':
                            images.append(result[i]['source_url'])
                    print(f"Found {len(images)} images")
                    return images
                else:
                    print("waiting for completion...")
                    await asyncio.sleep(5)

            except Exception as e:
                print(f"Error making API request: {e}")
                raise ValueError("Error making API request")

    except Exception as e:
        print(f"Error making API request: {e}")
        raise ValueError("Error making API request")

# get image url randomly from the array


def get_image_url(images):
    """
    Returns a random image URL from the given list of image URLs.

    Args:
        images (list): A list of image URLs.

    Returns:
        A random image URL from the list.
    """
    maxindex = len(images) - 1
    arrayindex = random.randint(0, maxindex)
    return images[arrayindex]
