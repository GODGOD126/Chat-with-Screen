# Chat with Screen

## Introduction
This project enables quick interaction with your computer screen through the GPT API. For instance, when you encounter a tricky issue, this program allows you to swiftly get helpful suggestions from GPT without the need to describe the problem in cumbersome detail.

## Features
- Modern and intuitive interface.
- Text and screenshot messaging capabilities.
- Real-time interaction with the GPT-4 model.
- Chat history is saved locally in a text file.
- Customizable round floating window for chat access.

## Installation
To run this program, you need a Python environment. Make sure the following dependencies are installed:
- Python 3.6 or higher
- PIL (Python Imaging Library)
- Requests

Install the necessary libraries using:
```bash
pip install Pillow requests
```
## Setup
Before using, ensure you set the correct OpenAI API key in the code:
```python
api_key = "YOUR_OPENAI_API_KEY"
```

Also, place a local image file in the project directory to use as the floating window icon. This image should be in a format supported by PIL, like PNG or JPG.

## Usage
- Clone or download this repository to your local machine.
- Open a terminal or command prompt.
- Navigate to the directory containing the program.
- Run the program with python your_program.py (replace your_program.py with the actual filename).

## Operating Guide
- Accessing Chat: Double-click the round floating window to open the chat interface.
- Sending Text Messages: Type your message in the input box at the bottom of the chat window and press Enter or click the "Screenshot+Send" button.
- Sending Screenshots: Click the "Screenshot+Send" button to capture the current screen and send it for processing.
- Viewing Chat History: The left side of the chat window shows GPT's responses, while the right side shows user messages. Both sections have scrollbars for navigating through the history.
- Closing the Program: Right-click on the floating window and select "QUIT" to close the program.

## Additional Information
The chat history is saved in a local text file named chat_history.txt. Ensure this file is present in the project directory for history logging.
Customize the floating window icon by replacing the local image file used in create_round_window function.

## Contributing
Contributions to the project are welcome. You can contribute by submitting bug reports, feature requests, or pull requests.

## License
This project is licensed under the MIT License. See the LICENSE file for more details.
