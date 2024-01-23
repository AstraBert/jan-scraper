# jan-scraper
jan-scraper: interact with Jan.ai by sending messages and retrieving the response

## Overview

**jan-scraper** is a Python package that provides a convenient interface to interact with Jan.ai. Jan.ai is an open-source desktop app designed to run large language models (LLMs) locally, ensuring an offline and privacy-focused environment. With **jan-scraper**, you can easily send messages to Jan.ai and retrieve responses, making it a versatile tool for leveraging Jan.ai's capabilities programmatically.

## Installation

- First and foremost, you need Jan.ai installed on your machine, and you need to download at least one of the models that the app suggests.

- Now, you can install **jan-scraper** using `pip`:

```bash
python3 -m pip install jan-scraper
```

## Requirements

- Python 3.10 or higher
- pyautogui (version 0.9.54)


## Functions

### `get_directory_info(path)`

Get the last modified time of a folder.

- **Parameters:**
  - `path (str)`: Path to the folder.
- **Returns:**
  - `float`: Last modified time of the folder.

### `define_assistant(json_file_path, new_instructions, model, name="Jan", description="A default assistant that can use all downloaded models")`

Update the assistant's configuration in a JSON file.

- **Parameters:**
  - `json_file_path (str)`: Path to the JSON file containing the assistant's configuration.
  - `new_instructions (str)`: New instructions for the assistant.
  - `model (str)`: Model to be used by the assistant.
  - `name (str)`: Assistant's name.
  - `description (str)`: Assistant's description.

### `parse_jsonl_file(file_path)`

Parse a JSON Lines file and return a list of JSON objects.

- **Parameters:**
  - `file_path (str)`: Path to the JSON Lines file.
- **Returns:**
  - `list`: List of parsed JSON objects.

### `get_package_location()`

Get the location of the installed jan-scraper package.

- **Returns:**
  - `str`: Location of the jan-scraper package.

### `scrape_jan(text, app, jan_threads_path, model, new_instructions="You are a helpful assistant", name="Jan", description="A default assistant that can use all downloaded models", set_new_thread=True)`

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

### Example

```python
import jan_scraper

# Define your messages, app path, and other necessary parameters
text = "Hi there, can you present yourself?"
app_path = "/path/to/jan-app"
threads_path = "/path/to/jan-threads"
model = "your-preferred-model"
instructions = "You are an Italian XVII century poet"
name = "Guglielmo Scuotipera"

# Scrape Jan.ai and retrieve the response
response = jan_scraper.scrape_jan(text = text, app = app_path, jan_threads = threads_path, model = model, new_instructions = instructions, name = name)

# Process the response as needed
print("Jan's Response:", response)
```

Find a more elaborate user case in [user_case.py](./user_case.py)

## License

This project is licensed under the AGPL-v3.0 License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [pyautogui](https://github.com/asweigart/pyautogui)
- [Jan.ai](https://jan.ai/)
