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

## Usage
1. Clone or download this repository to your local machine.
2. Ensure the following files are placed together in the `Chat_with_Screen` folder:
   - `Chat_with_Screen.py` (the main Python script)
   - `chat_history.txt` (file for storing chat history)
   - `test.png` (image file used for the floating window icon)
3. Open a terminal or command prompt.
4. Navigate to the `Chat_with_Screen` directory that contains the program files.
5. Run the program with the command `python Chat_with_Screen.py`.

Note: It's important to keep all three files in the same directory (`Chat_with_Screen`) to ensure the program runs correctly.


## Operating Guide
- **Accessing Chat**: Double-click the round floating window to open the chat interface.
- **Sending Messages and Screenshots**: Type your message in the input box at the bottom of the chat window. To send your message along with a screenshot of the current screen, click the "Screenshot+Send" button. When you do this, the chat window will temporarily disappear to avoid capturing the chat window in the screenshot, ensuring that only the relevant screen content is captured.
- **Viewing Chat History**: The left side of the chat window displays GPT's responses, while the right side shows user messages. Both sections are equipped with scrollbars for navigating through the history.
- **Closing the Program**: Right-click on the floating window and select "QUIT" to close the program.


## Additional Information
The chat history is saved in a local text file named chat_history.txt. Ensure this file is present in the project directory for history logging.
Customize the floating window icon by replacing the local image file used in create_round_window function.

## Contributing
Contributions to the project are welcome. You can contribute by submitting bug reports, feature requests, or pull requests.

## License
This project is licensed under the MIT License. See the LICENSE file for more details.
