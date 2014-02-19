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
* `sudo apt-get install python-mysqldb`
* python-dev
* `sudo apt-get install python-dev`


Setting up environment
---------------------

use virtual environment and pip
* sudo apt-get install python-virtualenv
* sudo apt-get install python-pip
* clone this repository
* `virtual-env dir`
* go inside the directory
* `pip install -r requirements`
* This will fail for bottle-flash. Fix: `pip install --no-install bottle-flash; touch build/bottle-flash/README.rst;pip install --no-download bottle-flash`
* alternative for bottle-flash: `git clone https://github.com/agrewal/bottle_plugins` then enter dir and `python setup.py install`
* `pip install wtforms`
* Create a new `config.py` file and adapt its contents (make a new mysql database)
* insert both `creation.sql` and `formula.sql`
* Finally `python run_sample.py`
