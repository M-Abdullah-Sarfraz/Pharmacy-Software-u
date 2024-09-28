# Pharmacy Management Software README

## Introduction

This project is a **Pharmacy Management Software** developed in **Python** that manages a range of pharmacy-related tasks such as inventory management, billing, and customer handling. The software uses a **Graphical User Interface (GUI)** built with **Tkinter** and implements several **design patterns** to ensure modularity and maintainability. A **SQLite3** database is used for storing all relevant data, and various Python libraries enhance the functionality of the software.

## Prerequisites

Ensure that you have **Python** installed on your system. Additionally, the following libraries need to be installed before running the program:

- **tkinter**: Used for GUI development.
- **sqlite3**: A lightweight, embedded database engine used to store the pharmacy data.
- **PIL (Pillow)**: For image processing and handling background images.
- **win32api** and **win32print**: Used for printing functionalities (works only on Windows).
- **random, tempfile, and time**: Standard Python libraries used for various functionalities such as generating random numbers and managing temporary files.

## Installation Steps

1. Open a terminal or command prompt.
2. Navigate to the project directory.
3. Run the following command to install all required libraries:
       pip install -r libraries.txt
   

## Running the Program

1. After installing the libraries, navigate to the project directory in your terminal.
2. Ensure the image file `image.jpg` is correctly placed according to the path specified in the code, or choose a background image of your preference and update the path in the code accordingly.
3. Execute the following command to run the software:
       python Chemist.py
   

4. Once the program runs, use the following login credentials to access the software:
   - **Username**: admin
   - **Password**: admin



## Technologies Used

### Tkinter
**Tkinter** is Python’s standard GUI library. It is used in this project to create windows, buttons, labels, and input fields that make the software user-friendly and interactive.

### SQLite3
**SQLite3** is a simple, self-contained, and serverless database engine. It is lightweight and is used here to store and manage all the pharmacy’s data, such as customer details, inventory, and billing records.

### Python Imaging Library (PIL)
**PIL** (via the **Pillow** fork) is used for handling image files, specifically to manage the background image for the GUI. You can customize the look and feel of the interface by choosing your own background image.

### Design Patterns
Design patterns such as **Model-View-Controller (MVC)** and **Singleton** have been applied in the code to improve maintainability, scalability, and clarity in code structure.

### Win32 Libraries
For Windows users, the **win32api** and **win32print** libraries allow integration with the Windows operating system for tasks like printing receipts directly from the application.



By following these instructions, you can successfully run and use the pharmacy management software.


