# Cori+

A simple social network, inspired by the now dead Google-Plus.

To run the app, do "flask run" in the package's parent directory.

Based on Tweepee example of [peewee](https://github.com/coleifer/peewee/).

This is the server. For the client, see [coriplusapp](https://github.com/sakuragasaki46/coriplusapp/).

## Features

* Create text statuses, optionally with image
* Follow users
* Timeline feed
* Add info to your profile
* In-site notifications
* Public API
* SQLite (or PostgreSQL)-based app

## Requirements

* **Python 3.10+** with **pip**.
* **Flask** web framework.
* **Peewee** ORM.
* A \*nix-based OS.

## Installation

* Install dependencies: `pip install .`
* Set the `DATABASE_URL` (must be SQLite or PostgreSQL)
* Run the migrations: `sh ./genmig.sh @`
* i forgor

