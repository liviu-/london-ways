The London Ways
================

## What is it?

It's a Flask application meant to hold your hand while you cross London.

![browser-screenshot](/screenshot.png?raw=true)

The bus data itself is not to be found in this repository, as it's the property of London Transport - insititute which does not directly endorse or know about my project or myself.

The project is designed to use Redis as a data storage for pairing up station ID with station name, so the project is bundeled with a bonus Python script to store CSV data in a Redis instance.

## How do I run it locally?

Requirements: 
* You'll have to go to [London Transport](https://www.tfl.gov.uk/info-for/open-data-users/) and sign-up to download the CSV file containing the bus stations information.
* Redis instance running
* virtualenv

```
$ git clone https://github.com/liviu-/london-ways
$ cd london-ways
$ virtualenv env
$ source env/bin/activate
(env) $ pip install -r requirements.txt
(env) $ cd london-ways
(env) $ mv /path/to/london-bus.csv .
(env) $ ./preprocess.py london-bus.csv
(env) $ python london-ways.py
```

To test it run `(env) $ python london_ways/tests/tests.py`
