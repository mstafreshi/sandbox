## hotwired/turbo in flask applications

This is a flask application that uses [Turbo-Flask](https://github.com/miguelgrinberg/turbo-flask) and also 
uses Turbo directly.

You can find examples in the source code of turbo-drive, turbo-frame, turbo-stream, threading, database models, forms
 and a few other things.

## Installation

First download it:

```bash
git clone https://github.com/mstafreshi/sandbox
```

Then you need to install a virtual environment in the root of the application source code folder:

```bash
cd sandbox/flask/turbo-flask
python -m venv venv
```

Then activate this virtual environment with:

```bash
source venv/bin/activate
```

Then install application requirements with pip:

```bash
pip install -r requirements.txt
```

That was all. Start the application:

```bash
/usr/bin/env python app.py
```

And in browser go to: ```http://127.0.0.1:5000```
