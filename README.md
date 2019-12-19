[![License](http://img.shields.io/:license-mit-blue.svg?style=flat-square)](http://badges.mit-license.org)
[![Build Status](https://travis-ci.org/agrija9/Software-Development-Project.svg?branch=master)](https://travis-ci.org/agrija9/Software-Development-Project)

# Post-mortem Analysis of ROS Bag File

This tool plots the topics of a RosBag file as a timeline. The timeline graph runs as an interactive web application that allows to select topics at ease and shows their corresponding messages and timestamps.

## Prerequisites

Software needed to run this repository:

- [Ubuntu 16.04](https://ubuntu.com/download/desktop)
- Python 2.7 / 3.6
- [ROS Kinetic](http://wiki.ros.org/kinetic/Installation/Ubuntu)

## Installation

### Clone

Clone this repository in you local machine

```
git clone https://github.com/agrija9/Software-Development-Project.git
```

### Setup

Install packages in home directory (no need of root privileges)

```
pip2 install --user -r requirements.txt
```

## Run

```
Open a terminal
Activate ROS environment
cd Software-Development-Project/
cd Interactive_graph/
python3 app.py
```

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
