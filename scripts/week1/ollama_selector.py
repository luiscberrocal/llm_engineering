import time

from scripts.week1.dockerhub_images import get_versions
from scripts.week1.settings import IMAGE_LIST, API_KEY
from openai import OpenAI


def build_user_prompt(versions: list[str], image: str, distro: str) -> str:
    images = "\n".join(versions)
    user_prompt = f"""You are looking for the best Docker hub image for {image} to use for a project. 
    You want to use the latest version of the image, but you want to stay one minor version behind the latest.
    Select the images that are the best to use for {image} and {distro}. The images to select from are: {images}
    Please provide a list Python list of strings with the best images to use only include the latest version behind."""
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
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": build_user_prompt(versions, image, distro)},
    ]
    open_ai = OpenAI(api_key=API_KEY)
    response = open_ai.chat.completions.create(model="gpt-4o-mini", messages=messages)

    print(response.choices[0].message.content)


if __name__ == "__main__":
    start = time.time()
    main()
    end = time.time()
    print(f"Execution time: {end - start:.2f} seconds")
