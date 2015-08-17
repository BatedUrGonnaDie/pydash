#Setting Up
Clone the Repo, then follow OS specific instructions.
#####Windows
  1. `pip install -r requirements.txt`

#####Linux
Tested on the following platforms:
- Debian 8.1 w/ python 2.7.9
- Ubuntu 14.04 LTS w/ python 2.7.6
- Fedora 22.3 w/ python 2.7.9

1. Install binary for system as described: `https://wiki.qt.io/PySide_Binaries_Linux`
2. `sudo pip install -U requests`
3. If SSL warning/error is thrown: `sudo pip install requests[security]`
(requires python-dev, libffi-dev, and libssl-dev packages)
4. If you receive an xcb threading error, make sure pip is up to date then try step 2 again.

#####Mac
Using 10.10, Python >= 2.7.9 (thanks to rennsport for testing)  
  1. `brew install qt`
  2. `sudo pip install -r requirements.txt`

#OS Support
This program is not thoroughly tested outside of windows.  If something
doesn't work open an issue with the full error and steps to reproduce.
