![logo](etc/logo.jpg)
# Maryland Degerrymanderer (MD)
These programs rely on 2010 Maryland census data to generate divided maps of Maryland. Maps can either be generated from the command-line or within the GUI. The current stable release allows the user to generate two divided maps of Maryland:
  1. Map of Zip Code Tabulation Areas (ZCTAs) each rendered a different color
  2. Unbiased map divided into eight districts of approximately equal population all rendered in a different color
### Requirements
These programs are intended to be run on ***Linux*** based operating systems. For a full list of supported operating systems, [click here](https://github.com/taaustin/Group2/blob/final/README.md#supported-operating-systems). Furthermore, ensure ***Python 3.5 or newer*** and a compatible version of ***pip*** is installed. To check which versions you have installed, run the following commands:
```
$ python3 --version
$ pip3 --version
```
- To intall Python 3, visit (https://www.python.org/downloads/)
- To install pip, visit (https://pip.pypa.io/en/stable/installing/)
### Getting Started
1. Clone this git respository for the latest stable release
2. Run ***linux_setup.py*** to ensure all required python libraries are installed:
    ```
    $ python3 linux_setup.py
    ```
3. Start the GUI:
    ```
    $ python3 md_dgm.py
    ```
###### Command-Line Interface
***THESE FEATURE NEED TO BE ADDED***
- Generate map of ZCTAs:
    ```
    $ python3 ziprender.py [filename]
    ```
- Generate map of districts:
    ```
    $ python3 zipdistrict.py [filename]
    ```
### Supported Operating Systems
###### Kali GNU/Linux Rolling (2020.1)
- Full functionality
###### Ubuntu 18.04.3 LTS (Bionic Beaver)
- Spinner appears but does not spin
- Unable to open 2 map windows at the same time
###### Ubuntu 20.04 LTS (Focal Fossa)
- Open windows do not unminimize within GUI, must unminimize from navigation bar
