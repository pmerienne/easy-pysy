import os

import easy_pysy as ez

markdown_filename = os.path.join(os.path.dirname(__file__), 'table.md')


def test_read_md_table():
    with open(markdown_filename) as md_file:
        lines = ez.read_md_table(md_file)
        assert list(lines) == [
            {"Firstname": "John", "Lastname": "Doe", "Age": "18", "Jobs": "Dev,Teacher", "Rooms": "1,2"},
            {"Firstname": "Jane", "Lastname": "Doe", "Age": "", "Jobs": "Cooker", "Rooms": "1"},
        ]


def test_post_process_md_table():
    with open(markdown_filename) as md_file:
        lines = ez.read_md_table(md_file, types={
            'Age': int,
            'Jobs': lambda raw: raw.split(','),
            "Rooms": lambda raw: [int(room) for room in raw.split(',')]
        })
        assert list(lines) == [
            {"Firstname": "John", "Lastname": "Doe", "Age": 18, "Jobs": ["Dev", "Teacher"], "Rooms": [1, 2]},
            {"Firstname": "Jane", "Lastname": "Doe", "Age": None, "Jobs": ["Cooker"], "Rooms": [1]},
        ]

