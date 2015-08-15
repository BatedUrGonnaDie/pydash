#Setting Up
Clone the Repo, then follow OS specific instructions.
#####Windows
  1. `pip install -r requirements.txt`

#####Ubuntu
Tested using Ubuntu 14.03 LTS on python 2.7.6  
  1. `sudo apt-get install python-pyside`
  2. `sudo pip install -r requirements.txt`
  3. If threading/SSL error: `sudo pip install requests[security]`

#####Mac
Not tested, might not be this easy.  
  1. `brew install qt`
  2. `sudo pip install -r requirements.txt`

#OS Support
This program is not thoroughly tested outside of windows.  If something
doesn't work open an issue with the full error and steps to reproduce.
