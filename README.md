[![License](http://img.shields.io/:license-mit-blue.svg?style=flat-square)](http://badges.mit-license.org)
[![Build Status](https://travis-ci.org/agrija9/Software-Development-Project.svg?branch=master)](https://travis-ci.org/agrija9/Software-Development-Project)

# Post-mortem Analysis of a ROS Bag File

This tool plots the topics of a RosBag file as a timeline. The timeline graph runs as an interactive web application that allows to select topics at ease and shows their corresponding messages and timestamps.

## Prerequisites

Software needed to run this repository:

- [Ubuntu 16.04](https://ubuntu.com/download/desktop)
- Python 2.7 / 3.6

## Installation

### ROS

Install [ROS Kinetic](http://wiki.ros.org/kinetic/Installation/Ubuntu)

### Python Virtual Environment

Open terminal to install pip and virtual environment

```
python3 -m pip install --user --upgrade pip
python3 -m pip install --user virtualenv
```

### Clone repository

Clone this repository in your computer

```
git clone https://github.com/agrija9/Software-Development-Project.git
```

### Create and activate python environment

In main repo folder do

```
python3 -m venv env
```

This will create a folder called ```env``` where all the packages required to run this software will be stored.

Activate python environment

```
source env/bin/activate
```

### Install requirements

Install packages in environment

```
pip install -r requirements.txt
```

## Run

Open a terminal and do

```
ros
roscore
cd Software-Development-Project/
cd Interactive_graph/
python3 app.py
```

In another terminal do

```
cd Software-Development-Project/
source env/bin/activate
cd Interactive_graph/
python3 app.py
```

After this a local host will be created at ```http://127.0.0.1:5000/```. Go to that page and start using the application in your browser.


## Test

For unit testing run

```
python3 test_app.py
```

## Built With

* [Flask](https://www.palletsprojects.com/p/flask/) - Web framework
* [visjs](https://visjs.org/) - Interactive timeline in browser

##  Authors 

- [Alan Preciado Grijalva](https://github.com/agrija9)
- [Ragith Ayyappan Kutty](https://github.com/rkutty1)
- [Devaiah Ulliyada Arun](https://github.com/divindevaiah)
- [Shravanthi Arvind Patil](https://github.com/ShravanthiPatil)

## License

- **[MIT license](http://opensource.org/licenses/mit-license.php)**

## Contributions

- PEP 8

## TODO

- Travis build
- GIF in description
- Add use example (images)
