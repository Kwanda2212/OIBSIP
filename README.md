# 🐍 Oasis Infobyte Python Programming Internship Projects

[![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Oasis Infobyte](https://img.shields.io/badge/Internship-Oasis%20Infobyte-orange.svg)](https://oasisinfobyte.com/)

## 📋 Overview

This repository contains the completed projects for the **Oasis Infobyte Python Programming Internship**. The intensive 4-week internship program focuses on becoming proficient in Python programming, covering essential skills and practical applications in software development.

## 🚀 Projects Included

### 1. 🔐 Password Generator
**Files:** `password_generator.py`,

A comprehensive password generation tool with both beginner and advanced versions:

#### Beginner Version Features:
- **Interactive Command-Line Interface**: Step-by-step user guidance
- **Customizable Length**: Password length from 4-50 characters
- **Character Type Selection**: Choose from lowercase, uppercase, numbers, and symbols
- **Password Strength Analysis**: Real-time feedback on password security
- **Input Validation**: Robust error handling and user-friendly prompts


**Key Learning Concepts:**
- Randomization using `secrets` and `random` modules
- User input validation and error handling
- Character set manipulation
- GUI development with Tkinter
- File I/O operations
- Regular expressions for pattern detection

### 2. 🧮 BMI Calculator
**Files:** `main.py` `database.db`

A Body Mass Index calculator with health assessment capabilities:

#### Advanced Version Features:
- **Interactive GUI**: Professional interface with real-time calculations
- **Data Visualization**: BMI charts and health range indicators
- **Historical Tracking**: Save and view BMI history over time
- **Health Recommendations**: Personalized advice based on BMI category
- **Export Functionality**: Save results to CSV files
- **Age and Gender Considerations**: Enhanced accuracy for different demographics

**Key Learning Concepts:**
- Mathematical calculations and formula implementation
- Unit conversion algorithms
- Data validation and sanitization
- GUI design principles
- Data persistence and file handling
- Chart generation and visualization
- Exception handling for edge cases

### 3. 💬 Chat Application
**Files:**  `chat_application.py`

A real-time chat application with both server-client architecture and GUI interface:

#### Core Features:
- **Multi-Client Support**: Server handles multiple simultaneous connections
- **Real-Time Messaging**: Instant message delivery between clients
- **User Authentication**: Username-based identification system
- **Message Broadcasting**: Messages sent to all connected clients
- **Connection Management**: Graceful handling of client connections/disconnections
- **Thread-Safe Operations**: Concurrent message handling using threading

#### GUI Version Features:
- **Modern Chat Interface**: User-friendly graphical interface
- **Message History**: Scrollable chat history with timestamps
- **Emoji Support**: Enhanced messaging with emoji integration
- **File Sharing**: Send and receive files between clients
- **Private Messaging**: Direct messages between specific users
- **Customizable Themes**: Different color schemes and layouts

**Key Learning Concepts:**
- Socket programming for network communication
- Multi-threading for concurrent operations
- Client-server architecture design
- Protocol design and message formatting
- GUI event handling and user interaction
- File transfer protocols
- Error handling for network operations
- Asynchronous programming concepts

## 🛠️ Installation & Setup

### Prerequisites
- Python 3.7 or higher
- Required packages (install via pip):

```bash
# For Password Generator (Advanced)
pip install pyperclip

# For BMI Calculator (Advanced)
pip install matplotlib pandas numpy

# For Chat Application
pip install tkinter  # Usually comes with Python
```

### Installation Steps

1. **Clone the repository:**
```bash
git clone https://github.com/yourusername/oasis-infobyte-python-projects.git
cd oasis-infobyte-python-projects
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Run individual projects:**

```bash
# Password Generator (Beginner)
python password_generator_beginner.py

# Password Generator (Advanced)
python password_generator_advanced.py

# BMI Calculator (Basic)
python bmi_calculator_basic.py

# BMI Calculator (Advanced)
python bmi_calculator_advanced.py

# Chat Application (Start server first)
python chat_server.py
# Then run client(s) in separate terminals
python chat_client.py
```

## 📁 Project Structure

```
oasis-infobyte-python-projects/
│
├── 🔐 Password Generator/
│   ├── password_generator_beginner.py      # Command-line version for beginners
│
├── 🧮 BMI Calculator/
│   ├── main.py         # Advanced with GUI and tracking
│   ├── database.db         # database for bmi calculator
│
├── 💬 Chat Application/
│   ├── chat_application.py            # GUI client interface
│

├── 🖼️ Screenshots/
│   ├── password_generator_demo.png
│   ├── bmi_calculator_demo.png
│   └── chat_application_demo.png
│
└── README.md                              # This file
```

## 🎯 Learning Outcomes

Through these projects, the following Python programming concepts and skills were developed:

### Core Programming Concepts
- **Variables and Data Types**: String manipulation, numeric operations
- **Control Structures**: Loops, conditional statements, exception handling
- **Functions**: Modular programming, parameter passing, return values
- **Object-Oriented Programming**: Classes, methods, inheritance
- **File Handling**: Reading, writing, and manipulating files

### Advanced Concepts
- **GUI Development**: Tkinter widgets, event handling, layout management
- **Network Programming**: Sockets, client-server architecture, protocols
- **Concurrency**: Threading, asynchronous programming
- **Data Structures**: Lists, dictionaries, sets for efficient data management
- **Regular Expressions**: Pattern matching and text processing

### Software Development Practices
- **Error Handling**: Robust exception management and user feedback
- **Input Validation**: Data sanitization and security considerations
- **Code Organization**: Modular design, documentation, and maintainability
- **User Experience**: Intuitive interfaces and clear user guidance
- **Testing**: Input validation, edge case handling, and debugging

## 🌟 Features Showcase

### Password Generator Highlights
- ✅ Cryptographically secure random generation
- ✅ Customizable character sets and exclusions
- ✅ Real-time strength analysis with visual feedback
- ✅ Batch password generation (1-100 passwords)
- ✅ Clipboard integration for easy copying
- ✅ Password history and file export

### BMI Calculator Highlights
- ✅ Support for both metric and imperial units
- ✅ Health category classification with recommendations
- ✅ Data visualization with charts and graphs
- ✅ Historical tracking and progress monitoring
- ✅ Export functionality for health records
- ✅ Age and gender-specific considerations

### Chat Application Highlights
- ✅ Multi-client real-time messaging
- ✅ Thread-safe server implementation
- ✅ Modern GUI with message history
- ✅ File sharing capabilities
- ✅ Private messaging between users
- ✅ Customizable themes and appearance

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

### Contribution Guidelines
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

.

## 🙏 Acknowledgments

- **Oasis Infobyte** for providing the internship opportunity and project guidelines
- **Python Community** for excellent documentation and resources
- **Open Source Contributors** for the libraries and tools used in these projects

## 📞 Contact

**Internship Program:** [Oasis Infobyte](https://oasisinfobyte.com/)  
**LinkedIn:** [Oasis Infobyte LinkedIn](https://www.linkedin.com/company/oasis-infobyte)

---

*This repository represents the practical application of Python programming skills developed during the Oasis Infobyte internship program. Each project demonstrates different aspects of software development, from basic scripting to advanced GUI applications and network programming.*

**Happy Coding! 🚀**
