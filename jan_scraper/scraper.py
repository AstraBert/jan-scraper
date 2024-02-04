import json
import pyautogui
import time
import subprocess
import platform
import os
import sys
import warnings
from jan_scraper import UnableToFindLocationError
from pyautogui import ImageNotFoundException
from jan_scraper import MayActivateOnlyOneModelWarning


def get_directory_info(path):
    """
    Get the last modified time of a folder.

    Parameters:
        path (str): Path to the folder.

    Returns:
        float: Last modified time of the folder.
    """
    # Use different methods based on the platform
    info = os.stat(path)
    last_modified_time = info.st_mtime
    print(f"Folder {path} was last modified at {last_modified_time}", file=sys.stderr)
    return last_modified_time


def define_assistant(
    json_file_path,
    new_instructions,
    model,
    name="Jan",
    description="A default assistant that can use all downloaded models",
):
    """
    Update the assistant's configuration in a JSON file.

    Parameters:
        json_file_path (str): Path to the JSON file containing the assistant's configuration.
        new_instructions (str): New instructions for the assistant.
        model (str): Model to be used by the assistant.
        name (str): Assistant's name.
        description (str): Assistant's description.
    """
    # Load the existing JSON data from the file
    with open(json_file_path, "r") as file:
        data = json.load(file)

    # Update the fields with the new instructions
    data["instructions"] = new_instructions
    data["model"] = model
    data["name"] = name
    data["description"] = description

    # Write the updated data back to the file
    with open(json_file_path, "w") as file:
        json.dump(data, file, indent=2)


def parse_jsonl_file(file_path):
    """
    Parse a JSON Lines file and return a list of JSON objects.

    Parameters:
        file_path (str): Path to the JSON Lines file.

    Returns:
        list: List of parsed JSON objects.
    """
    results = []
    with open(file_path, "r") as file:
        for line in file:
            # Parse each line as a JSON object
            try:
                json_object = json.loads(line.strip())
                results.append(json_object)
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON in line: {line.strip()}")
                print(f"Error details: {e}")

    return results


def get_package_location():
    """
    Get the location of the installed jan-scraper package.

    Returns:
        str: Location of the jan-scraper package.
    """
    if platform.system() == "Windows":
        command = subprocess.run(
            "python3 -m pip show jan-scraper > .\jan_scaper.txt", shell=True
        )
        if command.returncode == 0:
            f = open(".\jan_scaper.txt")
            for i in f.readlines():
                if i.startswith("Location: "):
                    text = i.replace("Location: ", "").replace("\n", "")
                    return os.path.join(text, "jan_scraper")
        else:
            raise Exception(
                "Unable to find the location of the package, can't proceed",
                UnableToFindLocationError,
            )
    else:
        command = subprocess.run(
            "python3 -m pip show jan-scraper > ./jan_scaper.txt", shell=True
        )
        if command.returncode == 0:
            f = open("./jan_scaper.txt")
            for i in f.readlines():
                if i.startswith("Location: "):
                    text = i.replace("Location: ", "").replace("\n", "")
                    return os.path.join(text, "jan_scraper")
        else:
            raise Exception(
                "Unable to find the location of the package, can't proceed",
                UnableToFindLocationError,
            )


def scrape_jan(
    text,
    app,
    jan_threads_path,
    model,
    new_instructions="You are a helpful assistant",
    name="Jan",
    description="A default assistant that can use all downloaded models",
    set_new_thread=True,
):
    """
    Scrape data using the jan-scraper package.

    Parameters:
        text (str): Text input for jan-scraper.
        app (str): Path to the jan-scraper desktop app.
        jan_threads_path (str): Path to the threads directory used by jan-scraper.
        model (str): Model to be used by jan-scraper.
        new_instructions (str): New instructions for the assistant.
        name (str): Assistant's name.
        description (str): Assistant's description.
        set_new_thread (bool): Whether to set a new thread or use the existing one.

    Returns:
        str: Resulting message from jan-scraper.
    """
    packdir = get_package_location()
    approx_start = time.time()
    try:
        define_assistant(
            os.path.join(jan_threads_path, "../assistants/jan/assistant.json"),
            new_instructions,
            model,
            name,
            description,
        )

        # Launch the desktop app
        print(f"Approx start time: {approx_start}")
        subprocess.Popen(app)

        # Give the app some time to open
        time.sleep(7)

        jan_is_open = False

        while not jan_is_open:
            try:
                new_thread = pyautogui.locateOnScreen(
                    os.path.join(packdir, "new.png"), confidence=0.9
                )
                x_thread, y_thread, width_thread, height_thread = new_thread
                enter_your_message = pyautogui.locateOnScreen(
                    os.path.join(packdir, "enter_your_message.png"), confidence=0.9
                )
                x_enter, y_enter, width_enter, height_enter = enter_your_message
                jan_is_open = True
            except Exception as e:
                print("Waiting for Jan to open...", file=sys.stderr)
                jan_is_open = False
                time.sleep(1)
        if set_new_thread:
            pyautogui.click(x_thread + 4, y_thread + 4)
            time.sleep(10)
        pyautogui.click(x_enter + 2, y_enter + 2)
        pyautogui.typewrite(text)
        sendlocation = pyautogui.locateOnScreen(os.path.join(packdir, "send.png"))
        x_send, y_send, width_send, height_send = sendlocation
        pyautogui.click(x_send + 5, y_send + 5)
        time.sleep(15)
        message_is_being_generated = True
        while message_is_being_generated:
            try:
                print("Waiting for message to be generated...", file=sys.stderr)
                wait_button = pyautogui.locateOnScreen(
                    os.path.join(packdir, "waitbutton.png")
                )
                message_is_being_generated = True
                time.sleep(2)
            except Exception as e:
                message_is_being_generated = False
        jan_has_finished = False
        while not jan_has_finished:
            try:
                finished_button = pyautogui.locateOnScreen(
                    os.path.join(packdir, "copy.png")
                )
                jan_has_finished = True
            except Exception as e:
                print("Waiting for Jan to finish...", file=sys.stderr)
                jan_has_finished = False
                time.sleep(1)
        time.sleep(2)
        killlocation = pyautogui.locateOnScreen(os.path.join(packdir, "kill.png"))
        x_kill, y_kill, width_kill, heigth_kill = killlocation
        pyautogui.click(x_kill + 5, y_kill + 5)
        folders = [
            os.path.join(f"{jan_threads_path}", f"{fol}")
            for fol in os.listdir(jan_threads_path)
            if os.path.isdir(os.path.join(f"{jan_threads_path}", f"{fol}"))
        ]
        print(folders, file=sys.stderr)
        if set_new_thread:
            fold = ""
            approx_end = time.time()
            print(f"Approx end time: {approx_end}")
            for i in folders:
                if (
                    float(approx_start)
                    <= float(get_directory_info(i))
                    <= float(approx_end)
                ):
                    fold = i
                    break
                else:
                    continue
            jsonl = os.path.join(fold, "messages.jsonl")
            parsed_data = parse_jsonl_file(jsonl)
            return parsed_data[1]["content"][0]["text"]["value"]
        else:
            fold = folders[len(folders) - 1]
            jsonl = os.path.join(fold, "messages.jsonl")
            parsed_data = parse_jsonl_file(jsonl)
            return parsed_data[len(parsed_data) - 1]["content"][0]["text"]["value"]
    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)


def activate_jan_api(app):
    """
    Activate the Jan application through GUI interactions.

    Parameters:
    - app (str): The application to be activated.

    Note: Requires the use of the pyautogui library for GUI interactions.
    """
    packdir = get_package_location()
    subprocess.Popen(app)
    time.sleep(7)
    jan_is_open = False
    while not jan_is_open:
        try:
            x_loc, y_loc, h_loc, wd_loc = pyautogui.locateOnScreen(
                os.path.join(packdir, "server.png")
            )
            jan_is_open = True
        except Exception:
            print("Waiting for Jan to open...", file=sys.stderr)
            jan_is_open = False
            time.sleep(2)
    pyautogui.click(x_loc + 2, y_loc + 2)
    time.sleep(2)


def convert_stream_to_jsonl(stream):
    """
    Convert a text stream containing JSON lines into a JSON Lines (.jsonl) file.

    Parameters:
    - stream (str): Path to the input text stream file.

    Returns:
    - str: Path to the created JSON Lines file.
    """
    s = open(stream, "r+")
    lines = s.readlines()
    s.close()
    jsonl_file = os.path.join(
        os.path.dirname(os.path.realpath(stream)), "response.jsonl"
    )
    jsonl_fileobj = open(jsonl_file, "w")
    for line in lines:
        if line.replace("\n", "") == "" or line.replace("data: [DONE]\n", "") == "":
            continue
        else:
            jsonl_fileobj.write(line.replace("data: ", ""))
    jsonl_fileobj.close()
    return jsonl_file


def mine_content_from_jsonl(jsonlfile):
    """
    Extract content from a JSON Lines (.jsonl) file containing GPT-3 API response.

    Parameters:
    - jsonlfile (str): Path to the input JSON Lines file.

    Returns:
    - str: Mined content from the Jan API response.
    """
    results = parse_jsonl_file(
        jsonlfile
    )  # Assuming 'parse_jsonl_file' is defined elsewhere
    response = []
    for jsonobj in results:
        response.append(jsonobj["choices"][0]["delta"]["content"])
    return "".join(response)


def scrape_jan_through_api(
    text,
    model,
    new_instructions="You are a helpful assistant",
    name="Jan",
    description="A default assistant that can use all downloaded models",
):
    """
    Scrape responses from the Jan application through an API.

    Parameters:
    - text (str): User input text.
    - model (str): The model to be used in the API request.
    - new_instructions (str): Additional instructions for the system content.
    - name (str): Name of the assistant.
    - description (str): Description of the assistant.

    Returns:
    - str: Response obtained from the API.

    Note: Requires the use of the pyautogui library for GUI interactions.
    """
    system_content = f"Your name is {name} You can be described as {description} You have to follow these instructions {new_instructions}"
    response_exists = os.path.isfile("response.json")
    if response_exists:
        f = open("response.stream", "r+")
        f.seek(0)
        f.truncate()
        f.close()
    elif not response_exists:
        f = open("response.stream", "w")
        f.close()

    command = (
        'curl http://localhost:1337/v1/chat/completions -H "Content-Type: application/json" -d "{\\"messages\\": [{\\"role\\": \\"system\\", \\"content\\": \\"'
        + system_content
        + '\\"}, {\\"role\\": \\"user\\", \\"content\\": \\"'
        + text
        + '\\"}],\\"model\\": \\"'
        + model
        + '\\",\\"stream\\": true}" > response.stream'
    )

    cmd = subprocess.run(command, shell=True)

    if cmd.returncode == 0:
        results = convert_stream_to_jsonl("response.stream")
        answer = mine_content_from_jsonl(results)
        return answer
    else:
        return "Something went wrong"
