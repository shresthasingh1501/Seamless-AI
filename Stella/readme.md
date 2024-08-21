
# Stella


https://stella.vaizar.com


Stella is a conversational AI assistant that provides accurate and detailed answers to users' queries in various languages, including English, Hindi, Bengali, Tamil, Marathi, Gujarati, Punjabi, Urdu, Telugu, Kannada, and Malayalam. It leverages the power of multimodal AI to generate textual and visual responses based on the user's input.

## Features

- **Multilingual Support**: Stella understands and responds in multiple languages, allowing users to communicate in their preferred language or switch between languages seamlessly.

- **Multimodal AI**: Stella combines the capabilities of state-of-the-art language models and image generation models to provide responses in various formats, including text, images, or a combination of both.

- **Detailed and Context-Aware Responses**: Stella utilizes advanced natural language processing and understanding techniques to provide long, detailed, and context-aware responses to user queries, ensuring a more natural and engaging conversational experience.

- **Seamless Mode**: Stella offers a unique "Seamless Mode" that creates an immersive conversational environment by adjusting the output format (text or image) and language based on the user's input, providing a seamless and intuitive experience.

- **Audio Input and Output**: Stella supports audio input through voice recognition, allowing users to interact hands-free. Additionally, it can generate audio output (text-to-speech) for selected responses.

- **Responsive Web Interface**: Stella is accessible through a modern and responsive web interface, ensuring a consistent and user-friendly experience across various devices and screen sizes.

## Installation

1. Clone the repository:

```bash
git clone https://github.com/your-username/stella.git
```

2. Install the required dependencies:

```bash
cd stella
pip install -r requirements.txt
```

3. Configure the application by updating the `config.json` file with the appropriate settings, including API keys, model paths, and other configuration options.

## Usage

1. Run the application:

```bash
python run.py
```

2. Open your web browser and navigate to `http://localhost:5000` (or the configured port).

3. Start conversing with Stella by typing your queries, uploading images, or using the voice input feature.

4. Stella will respond with the appropriate output format (text, image, or a combination) based on your input and the selected mode (regular or Seamless Mode).

5. Explore the various features and settings, such as language selection, output mode, and Seamless Mode, to enhance your conversational experience.

## File Structure

```
.
├── client
│   ├── css
│   │   └── style.css            # CSS styles for the web interface
│   ├── html
│   │   ├── index.html           # Main HTML file for the web interface
│   │   └── temp.html            # Temporary HTML file (if any)
│   ├── img
│   │   ├── arrow-down-s-fill.png
│   │   ├── download.jfif
│   │   ├── gpt.png
│   │   ├── guy.jpg
│   │   ├── seamless-symbol.png  # Stella's logo/icon
│   │   ├── site.webmanifest     # Web app manifest file
│   │   └── user.png             # User avatar icon
│   └── js
│       ├── chat.js              # JavaScript file for handling chat functionality
│       ├── highlightjs-copy.min.js
│       ├── highlight.min.js     # Syntax highlighting library
│       └── icons.js             # JavaScript file for icons
├── config.json                  # Configuration file for the application
├── README.md                    # This file
├── requirements.txt             # Python dependencies required for the application
├── run.py                       # Entry point for running the application
└── server
    ├── __pycache__              # Cached Python bytecode files
    ├── app.py                   # Flask application setup
    ├── backend.py               # Backend logic for handling requests and responses
    ├── config.py                # Configuration module for the server
    └── website.py               # Website routing and rendering
```

## Contributing

Contributions to Stella are welcome! If you encounter any issues or have suggestions for improvements, please open an issue or submit a pull request.

When contributing, please follow these guidelines:

1. Fork the repository and create a new branch for your feature or bug fix.
2. Make your changes and ensure they follow the project's coding style and conventions.
3. Write tests for your changes, if applicable.
4. Update the documentation if necessary.
5. Commit your changes and push them to your forked repository.
6. Open a pull request against the main repository, describing your changes in detail.

## License

This project is licensed under the [MIT License](LICENSE).

## Acknowledgments

Stella utilizes various open-source libraries and frameworks, including:

- [Flask](https://flask.palletsprojects.com/) - Web framework for Python
- [Requests](https://requests.readthedocs.io/) - HTTP library for Python
- [Markdown-it](https://markdown-it.github.io/) - Markdown parser for JavaScript
- [Highlight.js](https://highlightjs.org/) - Syntax highlighting library
- [Tailwind CSS](https://tailwindcss.com/) - Utility-first CSS framework

Special thanks to the developers and contributors of these projects for their hard work and dedication.
```
This markdown code contains the entire content with proper formatting.
