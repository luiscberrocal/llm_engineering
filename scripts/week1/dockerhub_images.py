import re
from functools import lru_cache

import requests
import json
import logging


logger = logging.getLogger(__name__)


@lru_cache(maxsize=5)
def get_versions_dockerhub(image_name: str, page_size: int = 100):
    """
    Fetches a list of available Python versions (tags) from Docker Hub.

    Args:
        page_size (int): The number of results to request per page from the API.
                         Defaults to 100.

    Returns:
        list: A list of strings, where each string is a Python version tag.
              Returns an empty list if an error occurs or no tags are found.
    """
    # Base URL for the official Python image tags on Docker Hub V2 API
    base_url = f"https://hub.docker.com/v2/repositories/library/{image_name}/tags/"
    all_tags = []
    next_page = base_url  # Start with the first page

    while next_page:
        try:
            # Make the GET request to the API endpoint
            # Include page_size and sort by last_updated in descending order (most recent first)
            params = {"page_size": page_size, "ordering": "last_updated"}
            response = requests.get(next_page, params=params)

            # Check if the request was successful (status code 200)
            response.raise_for_status()

            # Parse the JSON response
            data = response.json()

            # Extract tag names from the 'results' list
            for result in data.get("results", []):
                tag_name = result.get("name")
                if tag_name:
                    all_tags.append(tag_name)

            # Get the URL for the next page
            next_page = data.get("next")

        except requests.exceptions.RequestException as e:
            print(f"Error fetching data from Docker Hub API: {e}")
            return []  # Return empty list in case of error
        except json.JSONDecodeError:
            print("Error decoding JSON response from Docker Hub API.")
            return []  # Return empty list if JSON is invalid

    return all_tags


def get_versions(image_name: str, image_filter: str, page_size: int = 100):
    """
    Fetches a list of available Python versions (tags) from Docker Hub.

    Args:
        image_name (str): The name of the Docker image to fetch versions for.
        image_filter (str): A regex pattern to filter the tags.
        page_size (int): The number of results to request per page from the API.
                         Defaults to 100.

    Returns:
        list: A list of strings, where each string is a Python version tag.
              Returns an empty list if an error occurs or no tags are found.
    """
    all_tags = get_versions_dockerhub(image_name, page_size)
    if image_filter:
        filtered_tags = [tag for tag in all_tags if re.match(image_filter, tag)]
    else:
        filtered_tags = all_tags
    logger.debug("TAGS: %s", len((filtered_tags)))
    return sorted(filtered_tags, reverse=True)


if __name__ == "__main__":
    # Example usage:
    data = {
        "name": "python",
        "image_filter": r"3\.1\d+\.\d+-([a-zA-Z]+)(-[a-zA-Z0-9]+)?",
    }
    data = {
        "name": "postgres",
        "image_filter": r"1[679]\.\d+-([a-zA-Z]+)(-[a-zA-Z0-9]+)?",
    }
    logger.debug("Testing Docker Hub API")
    print(f"Fetching {data['name']} versions from Docker Hub...")
    image_versions = get_versions(
        data["name"], image_filter=data["image_filter"]
    )  # Fetch 50 tags per page

    if image_versions:
        print(f"Found {len(image_versions)} Python versions:")
        # Print the first 20 versions as an example
        for version in image_versions:
            print(version)
    else:
        print("Could not retrieve Python versions.")
