# jan-scraper 
jan-scraper: interact with Jan.ai by sending messages and retrieving the response

⚠️DISCLAIMER: This version is still a beta and it is built for small, end-user, customizable projects. The implementation of API scraping brings us closer to the result of optimized scaling for large LLM application in daily life, but we're still far from what we can reach... Stay tuned!

🎉**jan-scraper for conversation??**: Now jan-scraper is optimized also to use Jan as an interface to hold a conversation with several text-generation and text2text-generation HuggingFace models, in 89 different languages, with *your own* pdfs.

⚠️Being a new implementation, the conversator module may still be unstable, throw errors and have some bugs. Moreover, it only support one pdf at a time, so, if you have more, make sure to concatenate all of them in only one file.

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
- langdetect (version 1.0.9)
- deep_translator (version 1.11.4)
- transformers (version 4.30.2)
- langchain-community (version 0.0.13)
- langchain (version 0.1.1)
- torch (version 2.1.2)

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


### `conversator.generate_id()`

Generate a random 26-character alphanumeric ID.

**Returns**
- `str`: The generated ID.

**Description**
This function generates a random alphanumeric ID with a length of 26 characters. It includes a mix of digits and uppercase letters, making it suitable for unique identifiers.

---

### `conversator.create_a_persistent_db(pdfpath)`

Create a persistent database from a PDF file.

**Parameters**
- `pdfpath` (str): The path to the PDF file.

**Description**
This function initiates the creation of a persistent database from a PDF file. It involves loading the PDF, splitting documents into smaller chunks, using HuggingFace embeddings to transform text into numerical vectors, and storing the processed data in a Chroma vector store. The time taken for the operation is printed to the standard error output. 

A cache for the embeddings that will be used by your language model will be created in the same directory as your pdf, in a folder named documenttitle_cache (if you have a pdf whose path is "/Users/User/mydata/chat.pdf", the vector store will be: "/Users/User/mydata/chat_cache").

A local vectore store will be created in the same directory as the provided pdf, in a folder named documenttitle_localDB (if you have a pdf whose path is "/Users/User/mydata/chat.pdf", the vector store will be: "/Users/User/mydata/chat_localDB").




### `conversator.jan_chatting(jan_app_path, jan_data_folder, thread_id, hfmodel, model_task, persistent_db_dir, embeddings_cache, pdfpath)`

Implement a chat system using the Jan app, Hugging Face models, and a persistent database.

**Parameters**
- `jan_app_path` (str): Path to the Jan app executable.
- `jan_data_folder` (str): Folder containing Jan app data.
- `thread_id` (str): ID of the chat thread.
- `hfmodel` (str): Hugging Face model identifier (see `models_source.supported_causalLM_models()` to get to know about available "text-generation" models and `models_source.supported_seq2seqLM_models()` to get to know about available "text2text-generation" models)
- `model_task` (str): Task for the Hugging Face model.
- `persistent_db_dir` (str): Directory for the persistent database.
- `embeddings_cache` (str): Path to cache Hugging Face embeddings.
- `pdfpath` (str): Path to the PDF file.

**Raises**
- `KeyboardInterrupt`: Raised if the user interrupts the chat.

**Description**
This function facilitates interaction with the Jan app, utilizes Hugging Face models, and manages a persistent database. It launches Jan, reads and processes chat messages from a JSON file, queries a conversational retrieval chain, translates responses, and updates the chat thread. The function is designed to handle interruptions with a graceful exit.

### `models_source.longest_in_list(l)`

Find and return the longest element in a list.

**Parameters**
- `l` (list): List of elements.

**Returns**
- `Any`: The longest element in the list.

**Description**
This function takes a list of elements as input and identifies the longest element within it. The result is the element with the maximum length.


### `models_source.choose_right_model(model_name, model_task)`

Choose the right Hugging Face model based on the provided model name and task.

**Parameters**
- `model_name` (str): Name or identifier of the Hugging Face model.
- `model_task` (str): Task associated with the model.

**Returns**
- `str`: The chosen Hugging Face model.

**Raises**
- `Exception`: Raised if the model is not supported.

**Description**
This function selects the appropriate Hugging Face model by analyzing the model name and task. It supports two tasks: "text2text-generation" and "text-generation." Depending on the task, it matches keywords in the model name and returns the most suitable model. If multiple matches are found, it chooses the one with the longest keyword.


### `models_source.supported_causalLM_models()`

Print a list of supported causal language models.

**Description**
This function prints a list of supported causal language models.


### `models_source.supported_seq2seqLM_models()`

Print a list of supported sequence-to-sequence language models.

**Description**
This function prints a list of supported sequence-to-sequence language models.

### `anylang.supported_languages()`

Print a list of supported languages.

**Description**
This function prints a list of supported languages based on the keys in the `LANGNAMES` dictionary.


### `anylang.TranslateFunctions`

A class for translating text between languages using Google Translate.

#### **Attributes**
- `text` (str): The text to be translated.
- `destination` (str): The target language for translation.
- `original` (str): The detected or specified source language for translation.

#### **Methods**
- `__init__(text, destination)`: Initialize the TranslateFunctions object.
- `translatef()`: Translate the text to the target language.

#### **Raises**
- `Unrecognizable_Language_Warning`: Warns if the provided language is not supported for auto-detection.

#### **Description**
The `TranslateFunctions` class encapsulates functionality for translating text between languages using Google Translate. It initializes with a text and a destination language, and automatically detects the source language (or defaults to "auto"). The `translatef` method performs the translation, and the class raises a warning if the provided language is not recognized for auto-detection.

**Usage Example**
```python
translator = TranslateFunctions("Hello, world!", destination="es")
translation = translator.translatef()
```


#### `anylang.TranslateFunctions.__init__(text, destination)`

Initialize the TranslateFunctions object.

**Parameters**
- `text` (str): The text to be translated.
- `destination` (str): The target language for translation.

**Raises**
- `Unrecognizable_Language_Warning`: Warns if the provided language is not supported for auto-detection.

**Description**
This method initializes a `TranslateFunctions` object with a given text and destination language. It attempts to detect the source language; if unsuccessful, it defaults to "auto" and raises a warning.



#### `anylang.TranslateFunctions.translatef()`

Translate the text to the target language.

**Returns**
- `str`: The translated text.

**Description**
This method utilizes Google Translate to translate the stored text to the specified destination language. The translated text is returned as a string.

**Usage Example**
```python
translator = TranslateFunctions("Hello, world!", destination="es")
translation = translator.translatef()
print(translation)  # Output: ¡Hola Mundo!
```

## Example

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

# Do you want to use your own HF model with your own pdf? Do something like this!
create_a_persistent_db("mydata/chat.pdf") # Creates a local vectorestore database at mydata/chat_localDB and a local embeddings cache at mydata/chat_cache
jan_chatting(jan_app_path="Jan.exe",jan_data_folder="Users/User/jan",thread_id="jan_1706919400",hfmodel="google/flan-t5-base",model_task="text2text-generation",persistent_db_dir="mydata/chat_localDB",embeddings_cache="mydata/chat_cache",pdfpath="mydata/chat.pdf")
```

Find more elaborate user cases in [user_case_noAPI.py](https://github.com/AstraBert/jan-scraper/tree/main/user_case_noAPI.py) and in [user_case_API.py](https://github.com/AstraBert/jan-scraper/tree/main/user_case_API.py). Make sure also not to miss the [Discord bot application user cases](https://github.com/AstraBert/jan-scraper/tree/main/discord_bot)!🐍

## License

This project is licensed under the AGPL-v3.0 License - see the [LICENSE](https://github.com/AstraBert/jan-scraper/tree/main/LICENSE) file for details.

## Acknowledgments

- [pyautogui](https://github.com/asweigart/pyautogui)
- [Jan.ai](https://jan.ai/)
- [langdetect](https://github.com/Mimino666/langdetect)
- [deep_translator](https://github.com/nidhaloff/deep_translator)
- [transformers](https://github.com/huggingface/transformers)
- [langchain and langchain-community](https://github.com/langchain-ai/langchain)
- [torch](https://pytorch.org/)
