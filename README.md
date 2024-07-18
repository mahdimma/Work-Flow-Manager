# Work-Flow-Manager

Work-Flow-Manager is a Python application built using PyQt6 that manages workflows through a graphical user interface. It allows supervisor to manage and analyse employee works

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)
- [Files](#files)
- [Dependencies](#dependencies)
- [Contributing](#contributing)
- [License](#license)

## Installation

To install and run the Work-Flow-Manager, follow these steps:

1. **Clone the repository:**
   ```bash
   git clone https://github.com/mahdimma/Work-Flow-Manager.git
   cd Work-Flow-Manager
   ```

2. **Set up a virtual environment (optional but recommended):**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install the required dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
   And configure SQL Server according to [Configuration](#configuration).

4. **Run the application:**
   ```bash
   python main.py
   ```

## Usage

Upon running `main.py`, the Work-Flow-Manager application will launch, displaying a graphical interface.

**In the first run, a window containing the ID and password of the first user will be displayed.**

## Configuration

The application connects to an SQL Server database using the following configuration:

```python
server = 'localhost'
database = 'master'
username = 'SA'
password = 'YourStrong@Passw0rd'
```

Ensure that your SQL Server is running and accessible with the provided credentials. Adjust the server address, database name, username, and password as necessary for your environment.

## Files

- **main.py:** The main entry point of the application. It imports necessary modules and sets up the GUI.
- **custom.css:** Contains custom styles for the application, enhancing the visual appearance.

## Dependencies

- **PyQt6:** For creating the graphical user interface.
- **jdatetime, datetime, locale:** For handling date and time in different formats.
- **pyodbc:** For connecting to SQL Server.
- **qt_material:** For applying custom stylesheets to the PyQt6 application.

## Contributing

Contributions to Work-Flow-Manager are welcome! Please follow these steps:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Make your changes and commit them (`git commit -am 'Add some feature'`).
4. Push to the branch (`git push origin feature-branch`).
5. Create a new Pull Request.

## License

This project is Closed to any use.

---
