# jan-scraper 
jan-scraper: interact with Jan.ai by sending messages and retrieving the response

⚠️DISCLAIMER: This version is still a beta and it is built for small, end-user, customizable projects. The implementation of API scraping brings us closer to the result of optimized scaling for large LLM application in daily life, but we're still far from what we can reach... Stay tuned!


## Overview

**jan-scraper** is a Python package that provides a convenient interface to interact with Jan.ai. Jan.ai is an open-source desktop app designed to run large language models (LLMs) locally, ensuring an offline and privacy-focused environment. With **jan-scraper**, you can easily send messages to Jan and retrieve responses, making it a versatile tool for leveraging Jan's capabilities programmatically.

## Installation

- First and foremost, you need Jan.ai installed on your machine, and you need to download at least one of the models that the app suggests.

- Now, you can install **jan-scraper** using `pip`:

```bash
python3 -m pip install jan-scraper
```
- Now open your python idle and do the following:
```bash
python3
Python 3.10.11 (tags/v3.10.11:7d4cc5a, Apr  5 2023, 00:38:17) [MSC v.1929 64 bit (AMD64)] on win32
Type "help", "copyright", "credits" or "license" for more information.
>>> from jan_scraper.scraper import get_package_location
>>> get_package_location()
'path\\to\\jan_scraper'
```
- Go to the [GitHub image directory](https://github.com/AstraBert/jan-scraper/tree/main/imgs) and download the images: now, move them to `'path\\to\\jan_scraper'` as obtained before. Everything should be then set to run!


## Requirements

- Python 3.10 or higher
- pyautogui (version 0.9.54)


## Functions

### `scraper.get_directory_info(path)`

Get the last modified time of a folder.

- **Parameters:**
  - `path (str)`: Path to the folder.
- **Returns:**
  - `float`: Last modified time of the folder.

### `scraper.define_assistant(json_file_path, new_instructions, model, name="Jan", description="A default assistant that can use all downloaded models")`

Update the assistant's configuration in a JSON file.

- **Parameters:**
  - `json_file_path (str)`: Path to the JSON file containing the assistant's configuration.
  - `new_instructions (str)`: New instructions for the assistant.
  - `model (str)`: Model to be used by the assistant.
  - `name (str)`: Assistant's name.
  - `description (str)`: Assistant's description.

### `scraper.parse_jsonl_file(file_path)`

Parse a JSON Lines file and return a list of JSON objects.

- **Parameters:**
  - `file_path (str)`: Path to the JSON Lines file.
- **Returns:**
  - `list`: List of parsed JSON objects.

### `scraper.get_package_location()`

Get the location of the installed jan-scraper package.

- **Returns:**
  - `str`: Location of the jan-scraper package.

### `scraper.scrape_jan(text, app, jan_threads_path, model, new_instructions="You are a helpful assistant", name="Jan", description="A default assistant that can use all downloaded models", set_new_thread=True)`

Scrape data using the jan-scraper package.

- **Parameters:**
  - `text (str)`: Text input for jan-scraper.
  - `app (str)`: Path to the jan-scraper desktop app.
  - `jan_threads_path (str)`: Path to the threads directory used by jan-scraper.
  - `model (str)`: Model to be used by jan-scraper.
  - `new_instructions (str)`: New instructions for the assistant.
  - `name (str)`: Assistant's name.
  - `description (str)`: Assistant's description.
  - `set_new_thread (bool)`: Whether to set a new thread or use the existing one.
- **Returns:**
  - `str`: Resulting message from jan-scraper.

### `scraper.activate_jan_api`

This function automates the activation of Jan application through a series of GUI interactions using the `pyautogui` library. Here's a step-by-step explanation:

- **Parameters**:
  - `app`: The application to be activated.

- **Function Flow**:
  1. Obtain the directory of the package using `get_package_location()`.
  2. If the application is not already active:
     - Start the application using `subprocess.Popen(app)`.
     - Continuously check for the presence of an image (server.png) on the screen, indicating that the application has opened.
     - Click on the located image to proceed.


### `scraper.convert_stream_to_jsonl(stream)`

Convert a text stream from Jan API containing JSON lines into a JSON Lines (.jsonl) file.

- **Parameters:**
  - `stream` (str): Path to the input text stream file obtained from the Jan API.

- **Returns:**
  - `str`: Path to the created JSON Lines file.

This function reads the provided text stream file, removes unnecessary lines, and writes the cleaned content into a new JSON Lines file. The resulting file can be used for further processing and analysis of Jan API responses.


### `scraper.mine_content_from_jsonl(jsonlfile)`

Extract relevant content from a JSON Lines (.jsonl) file obtained from Jan API responses.

- **Parameters:**
  - `jsonlfile` (str): Path to the input JSON Lines file.

- **Returns:**
  - `str`: Mined content from the Jan API response.

This function parses the JSON Lines file, extracts the desired content from the API response, and returns it as a string. The extracted content is typically relevant information obtained from scraping the Jan API, which can be further processed or displayed as needed.

### `scraper.scrape_jan_through_api`:

This function uses the previously defined `activate_jan_api` function and interacts with the API related to the Jan application, to obtain responses to user inputs. 

You can initialize the model you want to exploit and activate Jan API in your app doing the following:

1. `Settings > Models > Your-favourite-model > ... > Start Model`
2. `Local API server > Choose model to start > Your-favourite-model > Start server`

From version 0.0.4b0, we decided to deprecate the `auto` parameter. You can, nevertheless, call a function named `scraper.activate_jan_api` to speed up the process of API activation.

- **Parameters**:
  - `text`: User input text.
  - `model`: The model to be used in the API request.
  - `new_instructions`: Additional instructions for the system content.
  - `name`: Name of the assistant.
  - `description`: Description of the assistant.

- **Function Flow**:
  1. Create system content based on provided parameters.
  2. Check if a file named "response.json" exists and truncate it if it does.
  3. If the file doesn't exist, create it.
  4. Construct a command to make a `curl` request to an API endpoint.
  5. Execute the command using `subprocess.run`.
  6. If the command is successful, parse the JSON response from "response.stream", convert it to "response.jsonl" and return the content of the first choice message. If not, return an error message.

### `formatter.convert_code_to_curl_json`

Convert a Python code string to a format suitable for inclusion in a JSON string within a curl command.

**Parameters**
- `code` (str): Python code string.

**Returns**
- `str`: JSON-formatted string suitable for inclusion in a curl command.

**Description**
This function takes a Python code string as input and escapes backslashes and double quotes within the code to prepare it for inclusion in a JSON string within a curl command. It also replaces newline characters with '\\n' to ensure proper formatting in the JSON representation.


### Example

```python
import jan_scraper.scraper

# Define your messages, app path, and other necessary parameters
text = "Hi there, can you present yourself?"
app_path = "/path/to/jan-app"
threads_path = "/path/to/jan-threads"
model = "your-preferred-model"
instructions = "You are an Italian XVII century poet"
name = "Guglielmo Scuotipera"

# Scrape Jan.ai and retrieve the response
response = jan_scraper.scraper.scrape_jan(text = text, app = app_path, jan_threads_path = threads_path, model = model, new_instructions = instructions, name = name)

# Process the response as needed
print("Jan's Response:", response)


# Wanna speed up Jan opening and API activation? Try the following code!
jan_scraper.scraper.activate_jan_api(app_path)

# 1. Open Jan
# 1. Settings > Models > Your-favourite-model > ... > Start Model
# 2. Local API server > Choose model to start > Your-favourite-model > Start server
# 4. Scrape Jan API with the following function 
response = jan_scraper.scraper.scrape_jan_through_api(model="tinyllama-1.1b", text="How is it to be ruling on such a big Empire?", name="Carolus Magnus", new_instructions="You are an emperor from the Middle Ages")

print("Jan's Response:", response)
```

Find more elaborate user cases in [user_case_noAPI.py](https://github.com/AstraBert/jan-scraper/tree/main/user_case_noAPI.py) and in [user_case_API.py](https://github.com/AstraBert/jan-scraper/tree/main/user_case_API.py). Make sure also not to miss the [Discord bot application user cases](https://github.com/AstraBert/jan-scraper/tree/main/discord_bot)!🐍

## License

This project is licensed under the AGPL-v3.0 License - see the [LICENSE](https://github.com/AstraBert/jan-scraper/tree/main/LICENSE) file for details.

## Acknowledgments

- [pyautogui](https://github.com/asweigart/pyautogui)
- [Jan.ai](https://jan.ai/)
