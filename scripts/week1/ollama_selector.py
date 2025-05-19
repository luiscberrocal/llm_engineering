import time
from pathlib import Path

import requests

from scripts.week1.dockerhub_images import get_versions
from scripts.week1.settings import IMAGE_LIST, API_KEY, MODEL, OLLAMA_API, HEADERS
from openai import OpenAI



def build_user_prompt(versions: list[str], image: str, distro: str) -> str:
    images = "\n".join(versions)
    user_prompt = f"""You are looking for the best Docker hub image for {image} to use for a project. 
    You want to use the latest version of the image, but you want to stay one minor version behind the latest.
    Select the images that are the best to use for {image} and {distro}. The images to select from are: {images}
    Please provide a list Python list of strings with the best images to use only include the latest version behind.
    The image list might not be ordered by version so please scan the whole list and select the best one."""
    return user_prompt


def main():
    system_prompt = """As a Senior Reliability Engineer, you are responsible for recommending the
    best Docker hub image for is being used. You always prefer to stay one minor version behind the latest,
    but always the version behind to be in it's latest minor and patch version. For example, if the latest version is 3.13.3
    we want to the latest for version 3.12.x. You know that `alpine` is Linux distro but it is not based on Debian. 
    """
    image_data = IMAGE_LIST[0]
    versions = get_versions(image_data["name"], image_filter=image_data["image_filter"])
    image = image_data["name"]
    distro = "Debian"
    print(f"Fetching '{image.upper()}' versions from Docker Hub...")
    user_prompt = build_user_prompt(versions, image, distro)
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ]
    open_ai = OpenAI(api_key=API_KEY)
    model = "gpt-4o-mini"
    response = open_ai.chat.completions.create(model=model, messages=messages)

    print(response.choices[0].message.content)
    user_prompt_file = Path(__file__).parent / f"{model}_user_prompt_{image}_{distro.lower()}.txt"
    with open(user_prompt_file, "w") as f:
        f.write(user_prompt)


def classify_using_ollama():
    system_prompt = """As a Senior Reliability Engineer, you are responsible for recommending the
    best Docker hub image for is being used. You always prefer to stay one minor version behind the latest,
    but always the version behind to be in it's latest minor and patch version. For example, if the latest version is 3.13.3
    we want to the latest for version 3.12.x. You know that `alpine` is Linux distro but it is not based on Debian. 
    """
    image_data = IMAGE_LIST[0]
    versions = get_versions(image_data["name"], image_filter=image_data["image_filter"])
    image = image_data["name"]
    distro = "Debian"
    print(f"Fetching '{image.upper()}' versions from Docker Hub...")
    user_prompt = build_user_prompt(versions, image, distro)
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ]
    payload = {"model": MODEL, "messages": messages, "stream": False}
    response = requests.post(OLLAMA_API, json=payload, headers=HEADERS)
    print(response.json()['message']['content'])
    user_prompt_file = Path(__file__).parent / f"{MODEL}_user_prompt_{image}_{distro.lower()}.txt"
    with open(user_prompt_file, "w") as f:
        f.write(user_prompt)


if __name__ == "__main__":
    start = time.time()
    # main()
    classify_using_ollama()
    end = time.time()
    print(f"Execution time: {end - start:.2f} seconds")
