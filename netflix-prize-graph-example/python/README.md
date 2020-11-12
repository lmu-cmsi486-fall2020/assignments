# A Python DAL Using [Official Neo4j Python Driver](https://neo4j.com/developer/python/)

## Installation and Setup
First and foremost, you’ll need Python 3—Neo4j’s driver does not support Python 2 anymore. For clarity, the commands given here will have `3` as a suffix (`python3`, `pip3`), but if your machine only has Python 3 installed, then that suffix can be dropped (and indeed might not work).

Python has a module called `venv` (short for “virtual environment”) which allows developers to create a local Python environment where third-party libraries can exist without having to modify the system-level Python installation. This is similar to how having a _node_modules_ folder in a JavaScript code base allows libraries and packages to be installed there without modifying the overall system.

To initialize a local Python environment, run this [while `cd`’ed to this folder](.):

    cd python # Within this repository
    python3 -m venv env

This will initialize the environment and create a folder called _env_. This folder is specific to the development machine and should _not_ be committed to the repository (thus it should be listed in _.gitignore_).

To begin working within this environment, run this before starting to work (also while at the top of the code base):

    source env/bin/activate

This “activates” the environment so that you can now install libraries in the local setup without having the change the global one. You can tell when `virtualenv` is active by checking if `(env)` precedes your command line prompt. When `(env)` is on, you can now install the libraries needed by our DAL:

    pip3 install neo4j

It is important that you run `pip3 install` strictly _after_ you have set up and activated the virtual environment, because otherwise, Python will attempt to install the package _globally_ and this is generally no longer viewed as a recommended practice.

Once installed, there is no need to install again for that code base. Only `source env/bin/activate` needs to be invoked per work session. To “disconnect” from the environment, type:

    deactivate

You will notice how, when the environment is inactive, you can’t run or use the DAL code because you’re “outside” the environment at that point—the Neo4j library won’t be visible.

## Running the Examples
The reusable DAL code itself is in _netflix_dal.py_. The general pattern for invoking the accompanying programs is:

    DB_URL=<database URL> DB_PASSWORD=<Neo4j user password> python3 <program name> <arguments>

So, running _ratings_by_viewer.py_ for a database server on your local machine would look like this:

    DB_URL=neo4j://localhost DB_PASSWORD=omgwhyamitypingthis python3 ratings_by_viewer.py 83

As noted in the overall [README](../README.md), if supplying the password on the command line like this is unnerving, you can set the `DB_PASSWORD` environment variable through other common mechanisms.

The programs all include some rudimentary error checking and handling—the patterns for implementing these should be pretty well-ingrained by now, but if anything needs further exposition please don’t hesitate to ask.
