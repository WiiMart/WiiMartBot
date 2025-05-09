# WiiMart Discord Bot

<img src="https://wiimart.github.io/media/branding-bag-no-bg.png" width="100" height="100" align="right" />

This is a Discord bot built using the `discord.py` library that provides functionalities for managing and querying error codes related to a specific service. The bot can respond to commands, check the status of a service, and manage error codes stored in a SQLite database.

## Features

- Query error messages based on error codes.
- Set and unset the bot's status.
- Check the status of a service.
- Uses SQLite for storing error codes and messages.
- Uses MySQL for managing friend codes.

## Requirements

- Python 3.8 or higher
- `discord.py` library
- `python-dotenv` for environment variable management
- `requests` for making HTTP requests
- SQLite for database management (for error codes)
- MySQL connector for managing friend codes

## Installation

1. **Clone the repository**:
   `git clone https://github.com/WiiMart/WiiMartBot.git`
   `cd WiiMartBot`

2. **Install the required packages**:
   `pip install discord.py python-dotenv requests mysql-connector-python`

3. **Create a `.env` file** in the root directory of your project with the following format:
```
token=your token here 
status="Not Set" 
mqlu=mysqluser 
mqlp=mysqlpassword 
mqld=mysqldb 
mqur=mysqlurl 
mqpo=mysqlport
```

## Usage

1. **Run the bot**:
`python bot.py`

2. **Commands**:
- `/status`: Check the current status of the service.
- `/setstatus <status>`: Set the current status of the bot (requires Admin role).
- `/unsetstatus`: Unset the current status of the bot (requires Admin role).
- `/error <error_code>`: Get the error message linked with the specified error code.
- `/addfc <fc>`: Adds your friend code to the lists of friendcodes.
- `/forceaddfc <user> <fc>`: Adds the users friendcode to the lists of friendcodes (requires Admin role).
- `/getfc <user>`: Gets the friend code of the specified user.

## Database Management

The bot uses a SQLite database to store error codes and their corresponding messages. The database is created and populated automatically when the bot starts. 

The MySQL database is to store friend codes from users. It is not automatically populated, a table with usersfc is needed, with 2 collums, one for the userid as varchar of 20 and one for their friend code as fc as a varcahr of 16.

### Error Codes Format

The error codes are defined in the script and can include:
- Standalone codes (e.g., `204013`)
- Ranges (e.g., `204019-204041`), which will be expanded into individual codes.
- Wildcard codes (e.g., `2056XX`), which can match multiple codes.

*WiiMart is not affiliated with Nintendo or any related parties.*

*To contact, please send an email to support@wiimart.org*
