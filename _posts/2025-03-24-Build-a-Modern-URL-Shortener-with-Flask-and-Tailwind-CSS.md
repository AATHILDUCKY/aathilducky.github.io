---
title: "Build a Modern URL Shortener with Flask and Tailwind CSS"
categories: Web-Development Flask 
tags: ['flask', 'python', 'url-shortener', 'web-development', 'tailwindcss']
---

# Build a URL Shortener with Python, Flask & MySQL, Tailwindcss

i start my career in cyber security and now i started to learn python developement,automation these stuffs these are make more curious. and these i love problem solving, and practicing with small projects.

i decited to do some project but i dont have idea,  while i watch youtube videos, one youtuber,  he had posted video about url shortener. so i choose that as my first project

this is my project

![Alt Text](https://raw.githubusercontent.com/AATHILDUCKY/my-assets/refs/heads/main/urlshortner.png)


lets start

first we need to create a virtual envirement

```bash
python3 -m venv venv
```

then activate that virtual envirement
```bash
source venv/bin/activate
```

then install  some depentancies 
```bash
sudo apt install python3-pip
pip3 install flask flask-mysqldb
```

lets go to coding part


```python
from flask import Flask, request, redirect, render_template
from flask_mysqldb import MySQL
import random
import string

app = Flask(__name__)

```

- `flask`  this is core class for creating flask webapplication and 
- `request` this is handling the HTTP requeest
- `redirect` this is help to url redirection
- `render_templates` this is help to rendering html files

- `flask_mysqldb` this MQSQL extension for flask, this is make easiar to connect with mysql database

```python
app = Flask(__name__)
```
- app is the object that represents your Flask web application


## MYSQL configuration

```python
# MySQL Configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'cyber123/A'
app.config['MYSQL_DB'] = 'url_shortener'
```

- `app.config['MYSQL_HOST'] = 'localhost'`  its defining where sql database is running
- `app.config['MYSQL_USER'] = 'root'` its defining mysql user name
- `app.config['MYSQL_PASSWORD'] = 'cyber123/A'` its defining mysql database password
- `app.config['MYSQL_DB'] = 'url_shortener'` its defining database name 

## lets write  random 6 digit code for generate short code 

```python 
def generate_short_code(length=6):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

```

`random.choices()` generate a random lists, and `string.ascii_letters` this its randomly generate ascii charecters small and capital, `string.digits` this is generate random digit , and `random.choices(string.ascii_letters + string.digits, k=length)` this both compined generate ascii and digit makes 6 digit short code

```python
app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        long_url = request.form['long_url']
        cur = mysql.connection.cursor()
        short_code = generate_short_code()
        
        # Insert into database
        cur.execute("INSERT INTO urls (long_url, short_code) VALUES (%s, %s)", (long_url, short_code))
        mysql.connection.commit()
        cur.close()
        
        short_url = request.host_url + short_code
        return render_template('index.html', short_url=short_url)
    return render_template('index.html')
```

in this code `/` its define this endpoint its use both `GET` , `POST` method

- `POST` method is used to submitting in a from, and generating short url.
- `GET` method is helpfull  to display the form where users can enter their long url.


```python
long_url = request.form['long_url']
```

this `long_url` access the value of input filed 

```python
cur = mysql.connection.cursor()
```
its help to create a connection to MYSQL, its help to execute SQL queries in MYSQL

```python
short_code = generate_short_code()
```

its help to generate random shortcode urls

```python
cur.execute("INSERT INTO urls (long_url, short_code) VALUES (%s, %s)", (long_url, short_code))
```

this this code is used to intert shortcode and url into database

```python
mysql.connection.commit()
```

this is help to commit the transection, and save the changes in databse

```python
cur.close()
```
Closes the database cursor after the operation is complete.


## redirect and route url shortener 

```python
@app.route('/<short_code>')
def redirect_url(short_code):
    cur = mysql.connection.cursor()
    cur.execute("SELECT long_url FROM urls WHERE short_code = %s", (short_code,))
    result = cur.fetchone()
    cur.close()
    
    if result:
        return redirect(result[0])
    else:
        return "URL not found", 404
```

`@app.route('/<short_code>')` this is getting long url from the database, this route take dynamic `short code` , its part of url

```python
cur = mysql.connection.cursor()
cur.execute("SELECT long_url FROM urls WHERE short_code = %s", (short_code,))
```

in this code `cur` create a connect to mysql and `cur.execute("SELECT long_url FROM urls WHERE short_code = %s", (short_code,))` this get the suitable long url for short_urls

`result = cur.fetchone()` fetch the long url for short code

`cur.close()`  close the cursor


```python
if result:
        return redirect(result[0])
    else:
        return "URL not found", 404
```

in this code if result in database that redirect to the url, otherwize its show `URL not found` 

thats it next we need to write code for index.html
create a folder name ``/templates`` then create file inside this directory 

``index.html``

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>URL Shortener</title>
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-gray-100 font-sans antialiased">

    <div class="flex items-center justify-center min-h-screen py-12 px-6">
        <div class="max-w-md w-full bg-white rounded-lg shadow-xl p-8">
            <h1 class="text-3xl font-semibold text-center text-indigo-600 mb-6">URL Shortener</h1>
            
            <!-- Form -->
            <form method="POST" class="space-y-4">
                <div class="flex flex-col">
                    <label for="long_url" class="text-lg font-medium text-gray-700">Enter URL</label>
                    <input type="url" name="long_url" class="px-4 py-2 border rounded-lg text-gray-800 focus:ring-2 focus:ring-indigo-400 focus:outline-none" required placeholder="Paste your long URL here">
                </div>
                
                <button type="submit" class="w-full py-2 bg-indigo-600 text-white font-semibold rounded-lg hover:bg-indigo-700 focus:ring-2 focus:ring-indigo-400">Shorten URL</button>
            </form>

            {% if short_url %}
                <div class="mt-6 text-center">
                    <p class="text-lg text-gray-800">Shortened URL:</p>
                    <a href="{{ short_url }}" target="_blank" class="text-indigo-600 font-semibold hover:underline">{{ short_url }}</a>
                </div>
            {% endif %}
        </div>
    </div>

</body>
</html>

```

i use tailwind css for styling , tailwind is very easy to build mordern application quicly, i this case i used Tailwind CDN 

![Alt Text](https://raw.githubusercontent.com/AATHILDUCKY/my-assets/refs/heads/main/urlsshortner.gif)


and this is stores links in database 

```
mysql> select * from urls;
+----+--------------------------------------------------------------------------------------+------------+
| id | long_url                                                                             | short_code |
+----+--------------------------------------------------------------------------------------+------------+
|  1 | https://aathilducky.com/posts/Interactive-Snake-Game-Using-OpenCV-&-Hand-Tracking/   | AWXoIO     |
|  2 | https://aathilducky.com/posts/Unlocking-the-Secrets-Information-picoCTF-Walkthrough/ | t36O06     |
|  3 | https://aathilducky.com/posts/Unlocking-the-Secrets-Information-picoCTF-Walkthrough/ | 0NhECT     |
|  4 | https://www.interngate.com/2025/03/software-engineering-intern-metana-sri.html       | U4gyxQ     |
+----+--------------------------------------------------------------------------------------+------------+
```