import easy_pysy as ez


def test_read_md_table():
    with open('table.md') as md_file:
        lines = ez.read_md_table(md_file)
        assert list(lines) == [
            {"Firstname": "John", "Lastname": "Doe", "Age": "18"},
            {"Firstname": "Jane", "Lastname": "Doe", "Age": ""},
        ]


def test_post_process_md_table():
    with open('table.md') as md_file:
        lines = ez.read_md_table(md_file, types={'Age': int})
        assert list(lines) == [
            {"Firstname": "John", "Lastname": "Doe", "Age": 18},
            {"Firstname": "Jane", "Lastname": "Doe", "Age": None},
        ]

