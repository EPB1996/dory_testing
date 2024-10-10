import requests
import tkinter as tk
from tkinter import ttk, messagebox

# Load model directly
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
import json
import os

print("Loading Model")
tokenizer = AutoTokenizer.from_pretrained("meta-llama/Llama-3.2-1B-Instruct")
model = AutoModelForCausalLM.from_pretrained("meta-llama/Llama-3.2-1B-Instruct")
print("Model loaded")


def calling_api(config: dict):
    api = config.get("api")
    endpoint = config.get("endpoint")
    payload = config.get("payload")
    function = config.get("function")

    print(api, endpoint, payload)

    # Simulate an API call
    if function == "GET":
        response = requests.get(f"{api}/{endpoint}", params=payload)
    elif function == "POST":
        response = requests.post(f"{api}/{endpoint}", json=payload)
    elif function == "PUT":
        response = requests.put(f"{api}/{endpoint}", json=payload)

    result = response.json()

    print(f"Calling function {function} on  {api}{endpoint} with payload {payload}")
    print(f"Result: {result}")
    return result


def create_api_call():
    query = query_entry.get("1.0", tk.END)

    # Option 1: Direct api object creation
    object_form_example = {
        "api": "http://example.com",
        "endpoint": "message",
        "function": "POST",
        "payload": {"More positive!"},
    }

    # Option 2: Create a description while giving options on what kind of endpoints and apis to call
    """   possible_apis = ["calendar", "email", "notion"]
    object_form_example = {"api": "", "function": "", "payload": {}} """

    # Load the OpenAPI schema from the json file
    json_path = os.path.join(os.path.dirname(__file__), "open_api.json")
    with open(json_path, "r") as file:
        json_api = json.load(file)

    # Option 1: Context which takes the whole json api - does not work wo well on big json files. Want to have another mechanism or another way to get the correct functions
    context = (
        "You are a language model that generates structured suggestions from meeting transcripts.\n"
        "Your task is to create json objects with the following keys:\n\n"
        f"{object_form_example.keys()}\n\n"
        f"You should consider the following apis: {json_api} \n"
        'If no suitable API function call is available, you should generate return "No suitable function found" \n\n'
        "Instructions:\n"
        "1. Extract relevant information from the meeting transcript.\n"
        "2. Identify the additional information and context and create a dict to be added to the payload key. \n"
        "3. Populate the object with the extracted information.\n\n"
    )

    # Option 2: Descriptive and API needs to be handled after from this object. Depending on the api the model would select the payload should
    # take the form of the possible options. This would have to be pretrained
    """    context = (
        "You are a language model that generates structured suggestions from meeting transcripts.\n"
        "Your task is to create json objects with the following keys:\n\n"
        f"{object_form_example.keys()}\n\n"
        f"You should consider the following apis: {possible_apis} \n"
        "Instructions:\n"
        "1. Extract relevant information from the meeting transcript.\n"
        "2. Identify the additional information and context and create a dict to be added to the payload key. \n"
        "3. Populate the object with the extracted information.\n\n"

    ) """

    print(context)
    messages = [
        {
            "role": "system",
            "content": context,
        },
        {
            "role": "user",
            "content": f"Transcript: {query}",
        },
    ]

    model_inputs = tokenizer.apply_chat_template(
        messages, add_generation_prompt=False, return_tensors="pt"
    )

    input_length = model_inputs.shape[1]
    generated_ids = model.generate(
        model_inputs,
        do_sample=True,
        max_new_tokens=128,
    )
    print(
        tokenizer.batch_decode(
            generated_ids[:, input_length:], skip_special_tokens=True
        )[0]
    )


root = tk.Tk()
root.title("API Caller")

ttk.Label(root, text="Query for local model").grid(column=0, row=0, padx=10, pady=5)
query_entry = tk.Text(root, height=10, width=60)
query_entry.grid(column=0, row=1, columnspan=2, padx=10, pady=5)

api_button = ttk.Button(root, text="Create API Object", command=create_api_call)
api_button.grid(column=0, row=2, columnspan=2, pady=10)


""" def call_api_from_gui():
    api = api_entry.get()
    endpoint = endpoint_entry.get()
    function = function_var.get()
    payload = payload_entry.get()

    try:
        payload_dict = eval(payload)
        if not isinstance(payload_dict, dict):
            raise ValueError
    except:
        messagebox.showerror("Invalid Payload", "Payload must be a valid dictionary.")
        return

    config = {
        "api": api,
        "endpoint": endpoint,
        "function": function,
        "payload": payload_dict,
    }

    result = calling_api(config)
    result_text.delete(1.0, tk.END)
    result_text.insert(tk.END, str(result)) """


""" def insert_example_get():
    api_entry.delete(0, tk.END)
    api_entry.insert(0, "http://127.0.0.1:8000")
    endpoint_entry.delete(0, tk.END)
    endpoint_entry.insert(0, "")
    function_combobox.set("GET")
    payload_entry.delete(0, tk.END)
    payload_entry.insert(0, "{}")


def insert_example_post():
    api_entry.delete(0, tk.END)
    api_entry.insert(0, "http://127.0.0.1:8000")
    endpoint_entry.delete(0, tk.END)
    endpoint_entry.insert(0, "")
    function_combobox.set("POST")
    payload_entry.delete(0, tk.END)
    payload_entry.insert(0, '{"message": "Hello, New World!"}') """

""" ttk.Label(root, text="API URL:").grid(column=0, row=3, padx=10, pady=5)
api_entry = ttk.Entry(root, width=50)
api_entry.grid(column=1, row=3, padx=10, pady=5)

ttk.Label(root, text="Endpoint:").grid(column=0, row=4, padx=10, pady=5)
endpoint_entry = ttk.Entry(root, width=50)
endpoint_entry.grid(column=1, row=4, padx=10, pady=5)

ttk.Label(root, text="Function:").grid(column=0, row=5, padx=10, pady=5)
function_var = tk.StringVar()
function_combobox = ttk.Combobox(
    root, textvariable=function_var, values=["GET", "POST", "PUT"]
)
function_combobox.grid(column=1, row=5, padx=10, pady=5)
function_combobox.current(0)

ttk.Label(root, text="Payload:").grid(column=0, row=6, padx=10, pady=5)
payload_entry = ttk.Entry(root, width=50)
payload_entry.grid(column=1, row=6, padx=10, pady=5)

ttk.Label(root, text="Result:").grid(column=0, row=7, padx=10, pady=5)
result_text = tk.Text(root, height=10, width=60)
result_text.grid(column=0, row=8, columnspan=2, padx=10, pady=5)

example_get_button = ttk.Button(root, text="Example GET", command=insert_example_get)
example_get_button.grid(column=0, row=9, padx=10, pady=5)

example_post_button = ttk.Button(root, text="Example POST", command=insert_example_post)
example_post_button.grid(column=1, row=9, padx=10, pady=5)

call_button = ttk.Button(root, text="Call API", command=call_api_from_gui)
call_button.grid(column=0, row=10, columnspan=2, pady=10) """
root.mainloop()
