# Freecycle Monitor Bot

Welcome to the Freecycle Monitor GitHub repository! This repository contains an automation script that continually monitors listings on the Freecycle website and sends messages to listings that match user-specified keywords. Additionally, it notifies the user via Discord when an automated message has been sent out.

## Getting Started

To use this script, follow the instructions below:

1. **Clone the Repository**: Clone this repository to your local machine.

2. **Activate the Provided Virtual Environment**: Navigate to the cloned repository directory and activate the provided virtual environment:
   - On Windows:
     ```bash
     .\venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

3. **Create .env file**: Create a file named `.env` in the working directory of the script. Populate this file with your Freecycle username, password, and Discord bot token in the following format:
```bash
LOGIN=your_username
PASSWORD=your_password
TOKEN=your_discord_bot_token
```


4. **Update Keywords**: Update the list of keywords on line 24 of the script with your own keywords. This list will be used to filter listings.

5. **Update Discord Channel ID**: Update the Channel ID on line 39 with the ID of the Discord channel where you want to receive notifications.

6. **Download Chromedriver**: Download the correct version of chromedriver that corresponds to the version of Chrome installed on your system. Place the chromedriver file in the `Program Files (x86)` directory, or update line 43 of the script with the location of your chromedriver file.

## Usage

Once you have activated the provided virtual environment and completed the setup steps above, you can run the script using your preferred Python interpreter.

```bash
python Freecycle_Bot.py
```

The script will start monitoring Freecycle listings and sending messages to listings that match your keywords. You will receive notifications on Discord when automated messages are sent out.

## Contributing

Contributions to this project are welcome! If you encounter any issues or have suggestions for improvements, please open an issue or submit a pull request.

## License

This project is licensed under the MIT License.
