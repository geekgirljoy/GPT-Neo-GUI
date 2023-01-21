# Standard imports
import sys
import os
import json
import asyncio

# Qt imports - installed with "pip install PyQt5"
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

# The main window class
class GPTNEO_GUI(QMainWindow):
    
    # App Constructor
    def __init__(self):

        #display the splash screen while the app is loading
        splash_pix = QPixmap(os.path.dirname(os.path.realpath(__file__)) + "/" + 'gui/splash/Splash.png')
        splash = QSplashScreen(splash_pix, Qt.WindowStaysOnTopHint)
        splash.setMask(splash_pix.mask())
        splash.show()
        
       

        ############################
        # Initialize the main window
        ############################
        super(GPTNEO_GUI, self).__init__()
        self.setWindowTitle("GPT-Neo GUI")
        self.setFixedSize(640, 400) # set the size of the window
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        icon = QIcon()
        icon.addFile(os.path.dirname(os.path.realpath(__file__)) + "/" + 'gui/icons/GPTNEO_GUI_Icon_4x4.png', QSize(4,4))
        icon.addFile(os.path.dirname(os.path.realpath(__file__)) + "/" + 'gui/icons/GPTNEO_GUI_Icon_8x8.png', QSize(8,8))
        icon.addFile(os.path.dirname(os.path.realpath(__file__)) + "/" + 'gui/icons/GPTNEO_GUI_Icon_16x16.png', QSize(16,16))
        icon.addFile(os.path.dirname(os.path.realpath(__file__)) + "/" + 'gui/icons/GPTNEO_GUI_Icon_32x32.png', QSize(32,32))
        icon.addFile(os.path.dirname(os.path.realpath(__file__)) + "/" + 'gui/icons/GPTNEO_GUI_Icon_64x64.png', QSize(64,64))
        icon.addFile(os.path.dirname(os.path.realpath(__file__)) + "/" + 'gui/icons/GPTNEO_GUI_Icon_128x128.png',QSize(128,128))
        icon.addFile(os.path.dirname(os.path.realpath(__file__)) + "/" + 'gui/icons/GPTNEO_GUI_Icon_256x256.png', QSize(256,256))
        icon.addFile(os.path.dirname(os.path.realpath(__file__)) + "/" + 'gui/icons/GPTNEO_GUI_Icon_512x512.png', QSize(512,512))
        self.setWindowIcon(icon)
        
        #AppUserModelID for Windows 10 taskbar icon - yay windows just has to overcomplicate everything, 
        # not like the icon wasn't already set in the lines above!!!
        if sys.platform == "win32":
            import ctypes
            myappid = 'GPTNEO_GUI' # arbitrary string
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

        ############################
        # End Initialize the main window
        ############################


        ############################
        # Menu Bar
        ############################

        # Create a menu bar
        self.menu = self.menuBar()

        # Add File to the menu bar
        self.file_menu = self.menu.addMenu('&File')

        # Add Save to the File menu
        self.save_action = QAction('Save', self)
        self.save_action.setShortcut('Ctrl+S')
        self.save_action.setStatusTip('Save output to file')
        self.save_action.triggered.connect(self.Save)
        self.file_menu.addAction(self.save_action)

        # Create a separator
        self.file_menu.addSeparator()

        # Add Exit to the File menu
        self.exit_action = QAction('Exit', self)
        self.exit_action.setShortcut('Ctrl+Q')
        self.exit_action.setStatusTip('Exit application')
        self.exit_action.triggered.connect(self.close)
        self.file_menu.addAction(self.exit_action)

        # Add GPT Neo to the menu bar
        self.gptneo_menu = self.menu.addMenu('&GPT-Neo')

        # Add GPT Neo Model to the GPT Neo menu
        self.gptneo_model_menu = self.gptneo_menu.addMenu('Model')
        self.gptneo_model_menu.setStatusTip('Select GPT-Neo model')

        # Add GPT Neo Model 125M to the GPT Neo Model menu
        self.gptneo_model_125M_action = QAction('125M', self)
        self.gptneo_model_125M_action.setShortcut('Ctrl+1')
        self.gptneo_model_125M_action.setStatusTip('Set GPT-Neo model to 125M')
        self.gptneo_model_125M_action.triggered.connect(self.SetGPTNeoModel125M)
        self.gptneo_model_menu.addAction(self.gptneo_model_125M_action)

        # Add GPT Neo Model 1.3B to the GPT Neo Model menu
        self.gptneo_model_1_3B_action = QAction('1.3B', self)
        self.gptneo_model_1_3B_action.setShortcut('Ctrl+2')
        self.gptneo_model_1_3B_action.setStatusTip('Set GPT-Neo model to 1.3B')
        self.gptneo_model_1_3B_action.triggered.connect(self.SetGPTNeoModel1_3B)
        self.gptneo_model_menu.addAction(self.gptneo_model_1_3B_action)

        # Add GPT Neo Model 2.7B to the GPT Neo Model menu
        self.gptneo_model_2_7B_action = QAction('2.7B', self)
        self.gptneo_model_2_7B_action.setShortcut('Ctrl+3')
        self.gptneo_model_2_7B_action.setStatusTip('Set GPT-Neo model to 2.7B')
        self.gptneo_model_2_7B_action.triggered.connect(self.SetGPTNeoModel2_7B)
        self.gptneo_model_menu.addAction(self.gptneo_model_2_7B_action)

        # Add Set Max Length to the GPT Neo menu
        self.gptneo_set_max_length_action = QAction('Set Max Length', self)
        self.gptneo_set_max_length_action.setShortcut('Ctrl+M')
        self.gptneo_set_max_length_action.setStatusTip('Set GPT-Neo max output length')
        self.gptneo_set_max_length_action.triggered.connect(self.SetMaxLength)
        self.gptneo_menu.addAction(self.gptneo_set_max_length_action)

        # Add Set Temperature to the GPT Neo menu
        self.gptneo_set_temperature_action = QAction('Set Temperature', self)
        self.gptneo_set_temperature_action.setShortcut('Ctrl+T')
        self.gptneo_set_temperature_action.setStatusTip('Set GPT-Neo temperature')
        self.gptneo_set_temperature_action.triggered.connect(self.SetTemperature)
        self.gptneo_menu.addAction(self.gptneo_set_temperature_action)

        # Add Set Top P to the GPT Neo menu
        self.gptneo_set_top_p_action = QAction('Set Top P', self)
        self.gptneo_set_top_p_action.setShortcut('Ctrl+P')
        self.gptneo_set_top_p_action.setStatusTip('Set GPT-Neo top p')
        self.gptneo_set_top_p_action.triggered.connect(self.SetTopP)
        self.gptneo_menu.addAction(self.gptneo_set_top_p_action)

        # Add Change Input Exchange File to the GPT Neo menu
        self.gptneo_change_input_exchange_file_action = QAction('Change Input Exchange File', self)
        self.gptneo_change_input_exchange_file_action.setShortcut('Ctrl+I')
        self.gptneo_change_input_exchange_file_action.setStatusTip('Change GPT-Neo input exchange file')
        self.gptneo_change_input_exchange_file_action.triggered.connect(self.ChangeInputExchangeFile)
        self.gptneo_menu.addAction(self.gptneo_change_input_exchange_file_action)

        # Add Change Output Exchange File to the GPT Neo menu
        self.gptneo_change_output_exchange_file_action = QAction('Change Output Exchange File', self)
        self.gptneo_change_output_exchange_file_action.setShortcut('Ctrl+O')
        self.gptneo_change_output_exchange_file_action.setStatusTip('Change GPT-Neo output exchange file')
        self.gptneo_change_output_exchange_file_action.triggered.connect(self.ChangeOutputExchangeFile)
        self.gptneo_menu.addAction(self.gptneo_change_output_exchange_file_action)

        # Add Help to menu bar
        self.help_menu = self.menuBar().addMenu('&Help')
        self.help_menu.setStatusTip('Help Menu')

        # Add About to the Help menu
        self.about_action = QAction('About', self)
        self.about_action.setShortcut('F1')
        self.about_action.setStatusTip('About GPT-Neo GUI')
        self.about_action.triggered.connect(self.About)
        self.help_menu.addAction(self.about_action)


        ############################
        # End Menu Bar
        ############################


        ############################
        # GUI Elements
        ############################

        #create a label
        vertical_offset = 20
        self.label = QLabel(self)
        self.label.move(10, vertical_offset + 20)
        self.label.setText("GPT-Neo Input String")
        self.label.resize(self.label.sizeHint())

        #Create a QLineEdit widget for the input text
        self.textbox = QTextEdit(self)
        self.textbox.move(10, vertical_offset + 40)
        #resize to window size x - 10, height 50
        self.textbox.resize(self.width() - 130, vertical_offset + 50)
        #set the text
        self.textbox.setText("In a shocking finding, scientists discovered a herd of unicorns living in a remote, previously unexplored valley, in the Andes Mountains. Even more surprising to the researchers was the fact that the unicorns spoke perfect English.")

        #create a Generate Button
        self.button = QPushButton('Generate', self)
        self.button.move(self.width() - 110, vertical_offset + 40)
        self.button.resize(100, 50)
        self.button.clicked.connect(self.Generate)

        #create a label
        self.label = QLabel(self)
        self.label.move(10, vertical_offset + 120)
        self.label.setText("Generated Output")
        self.label.resize(self.label.sizeHint())

        #create a text box for the output
        self.output_textbox = QTextEdit(self)
        self.output_textbox.move(10, vertical_offset + 140)
        #resize to window size x - 10, height 50
        self.output_textbox.resize(self.width() - 20, 150)
        #set the text
        self.output_textbox.setText("Output will be appended here")
        #rich text
        self.output_textbox.setAcceptRichText(True)

        #create a label
        self.label = QLabel(self)
        self.label.move(10, vertical_offset + 300)
        self.label.setText("Output File Name")
        self.label.resize(self.label.sizeHint())

        # Create a QLineEdit widget for the output file name
        self.output_file_name = QLineEdit(self)
        self.output_file_name.move(10, vertical_offset + 320)
        #resize to window size x - 10, height 50
        self.output_file_name.resize(self.width() - 130, vertical_offset + 10)
        #set the text
        self.output_file_name.setText("generated_text.txt")

        #create a Save Button
        self.button = QPushButton('Save', self)
        self.button.move(self.width() - 110, vertical_offset + 320)
        self.button.resize(100, 50)
        self.button.clicked.connect(self.Save)

        ############################
        # End GUI Elements
        ############################
        self.show() # show the window

    # Generate method
    def Generate(self):
        print("Generating...")
        config = GPTNEO_GUI.CheckConfigFileJSON()
        
        #get the text from the text box
        text = self.textbox.toPlainText()
        path = os.path.dirname(os.path.realpath(__file__)) + "/"
        input_file_name = config["input_file"]

        #open the input file for writing
        input_file = open(path + input_file_name, "w+")
        input_file.write(text)
        input_file.close()

        # use a coroutine to check the output file (GPTNEO_output.txt) for text and if it has text, display it in the output text box
        async def check_output_file():
            while True:
                #check if the output file has text
                output_file_name = config["output_file"]
                output_file = open(path + output_file_name, "r")
                output_text = output_file.read()
                output_file.close()
                if len(output_text) > 0:
                    # Append the text to the output text box
                    self.output_textbox.append("\n" + output_text)
                    print("Generated")
                    # Clear the output file
                    output_file = open(path + config["output_file"], "w+")
                    output_file.write("")
                    output_file.close()
                    break
                await asyncio.sleep(10) # sleep for 10 seconds
        asyncio.run(check_output_file())


    # Save method
    def Save(self):
        print("Saveing...")
        #get the text from the text box
        text = self.output_textbox.toPlainText()
        path = os.path.dirname(os.path.realpath(__file__)) + "/generated_text/"
        output_file_name = self.output_file_name.text()

        if output_file_name == "":
            output_file_name = "generated_text.txt"

        #open the input file for writing and append the text
        output_file = open(path + output_file_name, "a+")
        output_file.write(text + "\n\n")
        output_file.close()
        print("Saved to " + path + output_file_name)


    # Check Config File method
    def CheckConfigFileJSON():
        # Open config.json
        config_file = open(os.path.dirname(os.path.realpath(__file__)) + "/" + "config.json", "r")
        # Read the file
        config = config_file.read()
        # Close the file
        config_file.close()
        # parse the json file into an object
        config = json.loads(config)
        # return the object
        return config

    # Write Config File method
    def WriteConfigFileJSON(json_object):
        # Open config.json
        config_file = open(os.path.dirname(os.path.realpath(__file__)) + "/" + "config.json", "w")
        # Convert the json object to a string
        json_object = json.dumps(json_object)
        # Write the json to the file
        config_file.write(json_object)
        # Close the file
        config_file.close()

    # Set GPT Neo Model to 125M
    def SetGPTNeoModel125M(self):
        print("Setting GPT Neo Model to 125M")
        # Get the config file
        config = GPTNEO_GUI.CheckConfigFileJSON()
        # Set the model to 125M
        config["model"] = config["models"]["125M"]
        # Write the config file
        GPTNEO_GUI.WriteConfigFileJSON(config)
    
    # Set GPT Neo Model to 1.3B
    def SetGPTNeoModel1_3B(self):
        print("Setting GPT Neo Model to 1.3B")
        # Get the config file
        config = GPTNEO_GUI.CheckConfigFileJSON()
        # Set the model to 1.3B
        config["model"] = config["models"]["1.3B"]
        # Write the config file
        GPTNEO_GUI.WriteConfigFileJSON(config)
    
    # Set GPT Neo Model to 2.7B
    def SetGPTNeoModel2_7B(self):
        print("Setting GPT Neo Model to 2.7B")
        # Get the config file
        config = GPTNEO_GUI.CheckConfigFileJSON()
        # Set the model to 2.7B
        config["model"] = config["models"]["2.7B"]
        # Write the config file
        GPTNEO_GUI.WriteConfigFileJSON(config)
    

    # Set Max Length method
    def SetMaxLength(self):
        print("Setting Max Length")
        # Get the config file
        config = GPTNEO_GUI.CheckConfigFileJSON()

        # Display a dialog box to get the max length, show the current max length as the default
        max_length, ok = QInputDialog.getInt(self, "Set Max Length", "Max Length:", config["max_length"], 1, 1000, 1)

        if ok:
            # Set the max length
            config["max_length"] = max_length
            # Write the config file
            GPTNEO_GUI.WriteConfigFileJSON(config)

    # Set Temperature method
    def SetTemperature(self):
        print("Setting Temperature")
        # Get the config file
        config = GPTNEO_GUI.CheckConfigFileJSON()

        # Display a dialog box to get the temperature, show the current temperature as the default
        temperature, ok = QInputDialog.getDouble(self, "Set Temperature", "Temperature:", config["temperature"], 0.0, 1.0, 2)

        if ok:
            # Set the temperature
            config["temperature"] = temperature
            # Write the config file
            GPTNEO_GUI.WriteConfigFileJSON(config)

    # Set Top P method
    def SetTopP(self):
        print("Setting Top P")
        # Get the config file
        config = GPTNEO_GUI.CheckConfigFileJSON()

        # Display a dialog box to get the top p, show the current top p as the default
        top_p, ok = QInputDialog.getDouble(self, "Set Top P", "Top P:", config["top_p"], 0.0, 1.0, 2)

        if ok:
            # Set the top p
            config["top_p"] = top_p
            # Write the config file
            GPTNEO_GUI.WriteConfigFileJSON(config)
    
    # Change Input Exchange File method
    def ChangeInputExchangeFile(self):
        print("Setting Input File Name")
        # Get the config file
        config = GPTNEO_GUI.CheckConfigFileJSON()

        # Display a dialog box to get the input file name, show the current input file name as the default
        input_file_name, ok = QInputDialog.getText(self, "Set Input File Name", "Input File Name:", QLineEdit.Normal, config["input_file"])

        if ok:
            # Set the input file name
            config["input_file"] = input_file_name
            # Write the config file
            GPTNEO_GUI.WriteConfigFileJSON(config)

    # Change Output Exchange File method
    def ChangeOutputExchangeFile(self):
        print("Setting Output File Name")
        # Get the config file
        config = GPTNEO_GUI.CheckConfigFileJSON()

        # Display a dialog box to get the output file name, show the current output file name as the default
        output_file_name, ok = QInputDialog.getText(self, "Set Output File Name", "Output File Name:", QLineEdit.Normal, config["output_file"])
        
        if ok:
            # Set the output file name
            config["output_file"] = output_file_name
            # Write the config file
            GPTNEO_GUI.WriteConfigFileJSON(config)
    
    def About(self):
        print("About")
        config = GPTNEO_GUI.CheckConfigFileJSON()
        # Display a message box with the about information
        QMessageBox.about(self, "About", "GPT Neo GUI\nVersion "+ config["version"] + "\n\nCreated by: \nGeekGirlJoy\n\nGPT Neo Created by:\nEleutherAI\n\nGitHub:\nhttps://github.com/geekgirljoy/GPT-Neo-GUI\n\nGitHub:\nhttps://github.com/EleutherAI/gpt-neo")
        
# End GPTNEO_GUI class
############################################
        

def main():
    app = QApplication(sys.argv)
    sys.window = GPTNEO_GUI()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()


