[![License](http://img.shields.io/:license-mit-blue.svg?style=flat-square)](http://badges.mit-license.org)
[![Build Status](https://travis-ci.org/agrija9/Software-Development-Project.svg?branch=master)](https://travis-ci.org/agrija9/Software-Development-Project)



# Post-mortem Analysis of ROS Bag File

This tool visualizes the topics and corresponding messages of a RosBag file in the form of a timeline. The timeline is an interactive graph that allows to zoom in/out and select specific topics.

## Prerequisites

Software needed to run this repository:

- [Ubuntu 16.04](https://ubuntu.com/download/desktop)
- Python 3.6
- [ROS Kinetic](http://wiki.ros.org/kinetic/Installation/Ubuntu)

## Installation

### Clone

Clone this repository in you local machine

```
git clone https://github.com/agrija9/Software-Development-Project.git
```

### Setup

```
pip install -r requirements.txt
```

## Run

Open a terminal. 

Activate ROS environment. 

```
cd Software-Development-Project/
cd Interactive_graph/
python3 app.py
```

TODO: Add images step by step of usage...

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
