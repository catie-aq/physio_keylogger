# Physio Keylogger

This project provides both a command-line interface (CLI) and a graphical user interface (GUI) for recording keyboard events and exporting them to CSV files. It only works when run as a superuser and relies on the `keyboard` library.

## Features

- Record keyboard events and save them as CSV files.
- Command-line interface for quick usage.
- Graphical user interface for interactive usage.

## Installation

To install the project and its dependencies, you need to have [Poetry](https://python-poetry.org/) installed. Once you have Poetry set up, you can install the project by running:

```shell
poetry install
```

## Usage

### Keylogger CLI

To start recording keyboard events and save them as a CSV file:

```shell
sudo -E poetry run convert_key_to_csv --output /path/to/output_directory
```
Example :
```shell
sudo -E poetry run convert_key_to_csv --output ./logs
```

- The keylogger will start immediately and save logs in the specified directory.
- Press `Ctrl+C` to stop recording while the terminal is focused.

### Keylogger GUI

To use the graphical interface:

```shell
sudo poetry run python -m keylogger.gui
```

- Select the output directory and use the Start/Stop buttons to control logging.

> **Note:**
> The `keyboard` library requires root privileges on Linux. Always use `sudo` when running the CLI or GUI.

## Bundling as a Standalone Executable

You can bundle both the CLI and GUI as standalone executables for Linux or Windows using [PyInstaller](https://pyinstaller.org/).

First, install the development dependencies:

```shell
poetry install --with dev
```

Then, to build both executables:

**On Linux:**
```shell
poetry run pyinstaller keylogger_cli.spec
```

**On Windows:**
```powershell
poetry run pyinstaller keylogger_cli.spec
```

The standalone executables will be created in the `dist//keylogger/` directory:
- `keylogger.exe` (CLI)
- `keylogger-gui.exe` (GUI)

> **Note:**
> - You must run PyInstaller on the target OS (build on Linux for Linux, on Windows for Windows).
> - For advanced options, see the [PyInstaller documentation](https://pyinstaller.org/en/stable/).

## License

This project is licensed under the Apache-2.0 License. See the LICENSE file for more details.
