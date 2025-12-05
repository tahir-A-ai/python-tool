Contact Book CLI (Python)

A simple Command-Line Contact Book built using modular Python, JSON storage, and CRUD operations.
Includes pytest tests for core functions.

Features

Add a new contact

List all contacts

Update a contact

Delete a contact

JSON file auto-created on first run

Minimal & beginner-friendly project structure

Project Structure
ContactBook/
│
├── contact_book/
│   ├── storage.py      # JSON read/write
│   ├── manager.py      # CRUD functions
│   └── cli.py          # menu-driven interface
│
├── data/
│   └── contacts.json
│
├── tests/
│   └── test_*.py       # pytest CRUD tests
│
└── main.py             # run CLI

Running the App
python main.py

Running Tests
pytest -v

Requirements

Libraries
pytest - run pip install pytest
Python standard library (json, os).

Purpose

This project is part of a learning roadmap to practice:

Python modules

JSON file handling

CRUD logic

Basic testing with pytest
