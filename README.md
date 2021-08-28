# ImageToAsciiGui
A Python Application with a nice looking user interface which converts any image into ascii characters which is usable anywhere!


## Compatibility
#### Operating Systems
This application works on both Linux and Windows. But it has not been tested on Mac yet. And I have detected some issues while running it on Linux but don't worry, I'm working on it. Overall, it works very well on Windows 10.
#### Python Versions
This application can run using python versions: 3.6.x, 3.7.x, 3.8.x and 3.9.x;
Avoid python versions older than 3.6.x

## Installation

#### Step-1: Create Virtual Environment
First install any compatible version of python mentioned above from http://python.org ; Python 3.9.x is recommended. Then open terminal (on Linux) or Cmd (on Windows) and install virtualenv package by typing this command:\
`python -m pip install virtualenv`\
And then create a virtual environment by entering this command:\
`python -m venv /path/to/your/virtual/environment` (for example: `python -m venv C://users/user/desktop/ImageToAscii`)\
And then, a virtual environment will be created.

#### Step-2: Activate the virtual environment
Next, we have to activate the virtual environment. To do so, do the following thing:

if you are running Linux, type this command in terminal and hit enter:\
`source /path/to/your/virtual/environment/bin/activate` (for example: `source ~/home/user/Desktop/ImageToAscii/bin/activate`)

or, if you are running windows, do following:\
`/path/to/your/virtual/environment/bin/activate.bat` (for example: `source C://users/user/desktop/ImageToAscii/bin/activate.bat`)

And your virtual environemnt will be activated!

#### Step-3: Download the File
Download the file from this Github repository by Clicking `Code` and then `Download ZIP` button and when it's downloaded, extract it. You will find a folder named ImageToAsciiApp inside the extracted folder. Go to that folder and you will find a file called `App.py`. This is the file you have to run.

#### Step-4: Run the App!
Now it's time to run the app. But you should note that, everytime you boot into your OS or reopen the terminal/cmd, you have to manually activate the virtual environment to run the application. Follow Step-2 to activate it.

Now, in order to run it, type this in the terminal: (this step is same for both Windows and Linux)\
`cd /path/to/your/ImageToAsciiGui/ImageToAsciiApp` (for example: `cd C://users/user/desktop/ImageToAsciiGui/ImageToAsciiApp`)

And then simply type this command on the terminal and hit enter:\
`python App.py`

If everything went well, then Congratualtions! You have successfully started the application!

#### Step-5: How to use it
First choose image by clicking `Choose Image` button. Then set an output path where the output file wil be stored, by clicking `Select Output File`. (this is optional). Then click `Convert To Ascii`. Done! You will see an ascii version of the choosed image on the right side of the window. But that view might look a bit messy! That's why to get a good view, click `Open In Text Editor` button. For Windows, it will show the output in notepad and for linux, it will be shown in terminal. BUT YOU MUST SELECT AN OUTPUT FILE TO CLICK THAT BUTTON. There are options to scale the image and set an width of that image. This is how you can use it.

#### step-6: Conclusion
I know, it's a very lengthy and annoying process of installation of any software That's why, I will add a Graphical Installer which will do the installation thing by itself in the next version. And there will be an app launcher by which you can launch this application with just a click! No need to open the cmd or terminal to install or launch the application. These features will be available very soon. And there will be plenty of customizing options too. Till then, be creative and be open-source!\
Enjoy using!
