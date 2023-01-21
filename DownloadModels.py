# Imports
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
import sys
import os
import json

#path = the path where this script is located
path = os.path.dirname(os.path.realpath(__file__)) + "/"

def CheckConfigFileJSON():
    # Open config.json
    config_file = open(path + "config.json", "r")
    # Read the file
    config = config_file.read()
    # Close the file
    config_file.close()
    # parse the json file into an object
    config = json.loads(config)
    # return the object
    return config

def WriteConfigFileJSON(json_object):
    # Open config.json
    config_file = open(path + "config.json", "w")
    # Convert the json object to a string
    json_object = json.dumps(json_object)
    # Write the json to the file
    config_file.write(json_object)
    # Close the file
    config_file.close()

json_config = CheckConfigFileJSON() # Get the config file


# Notify the user that the script is starting and that it will take a while to download all the models
print("It will take a while to download all the models.")
print("The largest model is like 10 GB in size... so be patient, you only have to do this once.")
print("If you want to stop the script, press Command + C on Mac or Control + C on Windows or Linux.\n\n")

# on Windows these files are stored: C:\Users\%username%\.cache\huggingface\transformers
# on Mac (I THINK) these files are stored: /Users/$USER/.cache/huggingface/transformers
# on Linux (I THINK) these files are stored: /home/$USER/.cache/huggingface/transformers
# but...
# they might be stored somewhere else depending on your operating system and your settings
# so...
# chew carefully, nom noms

# for all the models in json_config["models"]
for model in json_config["models"]:
    print("Downloading model "+model+"...")
    # Load the EleutherAI/gpt-neo-size model and tokenizer
    tokenizer = AutoTokenizer.from_pretrained(json_config["model"])  # Load/Download the tokenizer
    model = AutoModelForCausalLM.from_pretrained(json_config["model"])  # Load/Download the model
    print("Model "+model+" downloaded.")

print("All models downloaded.")
