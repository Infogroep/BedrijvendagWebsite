BedrijvendagWebsite
===================

Webplatform for Bedrijvendag
An event hosted by Infogroep

Purpose
------

The creation of a webplatform where administrators can get an overal look of the current standing of the event.

Requirements Linux
------------------
* python-mysqldb
* python-dev


Setting up environment
---------------------

use virtual environment and pip
sudo apt-get install python-virtualenv
sudo apt-get install python-pip

* clone this repository
* virtual-env the directory
* go inside the directory
* pip install -r requirements
* This will fail for bottle-flash. Fix: pip install --no-install bottle-flash; touch build/bottle-flash/README.rst;pip install --no-download bottle-flash

