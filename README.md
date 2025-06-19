# physio_keylogger

The following code starts recording immediately upon launch and stops when Ctrl + C is pressed. It only works when run as a superuser and relies on the keyboard library.

Additional line of information text about what the project does.

## Prerequisites

Before you begin, ensure you have met the following requirements:

## Installing physio_keylogger

To install physio_keylogger, follow these steps:

```bash
poetry install
```

## Using physio_keylogger

To use physio_keylogger, follow these steps:

```bash
poetry run dummy_project
sudo -E poetry run convert_key_to_csv --output ./logs
```
ou

sudo ./dist/keylogger/keylogger-gui

## License

This project is licensed under Apache 2.0, a permissive open source license that
allows you to freely use, modify, distribute, and sell your own
products that include this software. The full text of the license can be
obtained from the [Apache website](https://www.apache.org/licenses/LICENSE-2.0).
