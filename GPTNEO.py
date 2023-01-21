# Imports
from transformers import AutoTokenizer, AutoModelForCausalLM
import time
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

def CheckInputFile():
    # open the input file for reading and writing
    input_file = open(path + input_file_name, "r+")
    input_text = input_file.read()
    #clear the input file
    input_file.truncate(0)
    input_file.close()
    if input_text != "":
        return input_text
    else:
        return None


json_config = CheckConfigFileJSON() # Get the config file

input_file_name = json_config["input_file"] # Get the input file name from the config file
output_file_name = json_config["output_file"] # Get the output file name from the config file

# Notify the user that the script is starting and that it will take a while to download and or load the model
print("I this is the first time you are running this script, it will take a while to download the model.")
print("Especially if you didn't run DownloadModels.py first.")
print("The largest model is like 10 GB in size... so be patient for it to load or download.")
print("If/After the model is downloaded, the script will run much faster but... expect it to take like 5-10 minutes to load the model.")
print("Generating text will very depending on the length of the input text but expect it to take like 2-10 minutes per input prompt.")
print("If you want to stop the script, press Command + C on Mac or Control + C on Windows or Linux.\n\n")
print("GPT-Neo Model "+json_config["model"]+" Loading...")

# Load the EleutherAI/gpt-neo-size model
tokenizer = AutoTokenizer.from_pretrained(json_config["model"])  # Load/Download the tokenizer
model = AutoModelForCausalLM.from_pretrained(json_config["model"])  # Load/Download the model

# Announce the model has been loaded, yay we made it! :D
print("Model Loaded!")

while json_config["runGPTLoop"] == 'true':

    print("Checking for Input...")
    input_text = CheckInputFile()

    if input_text != None:
        print("Input Text: " + input_text)
        # Tokenize the input text
        inputs = tokenizer(input_text, return_tensors="pt")
        input_ids = inputs["input_ids"]

        # Generate some text
        output = model.generate(
            input_ids,
            attention_mask=inputs["attention_mask"],
            do_sample=True, 
            max_length=json_config["max_length"],
            temperature=json_config["temperature"],
            use_cache=True,
            top_p=json_config["top_p"]
        )
        # Decode the generated tokens to text
        output_text = tokenizer.decode(output[0])
        print("Output Text: " + output_text)
        output_file = open(path + output_file_name, "w")
        output_file.write(output_text)
        output_file.close()
        print("Output File Written!")

    time.sleep(5) # sleep for 5 seconds
    json_config = CheckConfigFileJSON() # check the config file again
