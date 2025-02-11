---
title: "How to find reflected xss"
categories: xss
tags: ['xss']
---
## What is XSS (Cross-Site Scripting)?

* Xss is a security vulnerability and its allow to injects malicious script into websites.

```shell
-XSS
  |--reflected xss
  |--stored xss
  |--DOM based xss
```

in this blog post i going to explain about reflected xss

## How it's work?

when give malicious script into entry points like search input section , Search forms, login forms, feedback forms ..etc that script reflect immediatly to user

and that is reflect  your URL or response

``URL parameter``

```
http://aathilducky.com/search?q=hello
```

``Payload``

```
http://aathilducky.com/search?q=<script>alert('XSS')</script>

```

and another enntry points are `**HTTP Headers:** User-Agent, Referer, Cookies.`

## Possibilities of Reflected Xss? (impacts)

```
|--Session Hijacking: Steal session cookies.
|--Phishing: Redirect users to malicious sites.
|--Defacement: Change how the website looks for the victim.
|--Keylogging: Capture keystrokes.
```

## Tools for finding reflected xss

* Burp Suite: Use the *Intruder* tool for fuzzing inputs.
* OWASP ZAP: Automated XSS scanner.
* XSSer: Automated framework for detecting XSS vulnerabilities.
* Browser Developer Tools: Check response reflections in real-time.
* ...etc

```php
<?php
    $search = $_GET['q'];
    echo "You searched for: " . $search;
?>
```

Exploit:

```
http://aathilducky.com/search.php?q=<script>alert('XSS')</script>
```

## Secured Code (Sanitizing Input)

```php
<?php
    $search = htmlspecialchars($_GET['q'], ENT_QUOTES, 'UTF-8');
    echo "You searched for: " . $search;
?>
```

it will filtering the input its show the script like plain text without execution

lot of vulnerable apps available for paracticing xss

* bWAPP
* DVWA
* Hackthbox, tryhackme ...etc

just i install  DVWA for practcing XSS

## Steps for install DVWA

* [ ] Download WAMPP server or XAMPP server

  [WAMPP link](https://sourceforge.net/projects/wampserver/)
* [ ] Download and Setup DVWA ,then extracted dvwa folder , move to `/www/`

```
C:\wamp64\www\
```

* [ ] Configure MySQL Database

```
http://localhost/phpmyadmin/
```

click database tab and create new database name `dvwa`

* [ ] Configure DVWA Settings

```
C:\wamp64\www\dvwa\config\config.inc.php
```

if this config file name `config.inc.php.dist` look like this change this like `config.inc.php`

navigate this file and open this in any text editors update some database related credentials

```php
$_DVWA[ 'db_server' ]   = getenv('DB_SERVER') ?: '127.0.0.1';
$_DVWA[ 'db_database' ] = getenv('DB_DATABASE') ?: 'dvwa';
$_DVWA[ 'db_user' ]     = getenv('DB_USER') ?: 'root';
$_DVWA[ 'db_password' ] = getenv('DB_PASSWORD') ?: '';
$_DVWA[ 'db_port']      = getenv('DB_PORT') ?: '3306';
```

* [ ] Install DVWA

go to this link

```
http://localhost/dvwa/setup.php
```

and click `Create/Reset Database ` after setup successfully use this default credencials to login DVWA

```
Username: admin
Password: password
```



## DVWA - low level

when i give simply give input `aathil` its its reflect in URL and in the page also show  `aathil`

```
http://localhost/dvwa/vulnerabilities/xss_r/?name=aathil#
```

<img src="https://raw.githubusercontent.com/AATHILDUCKY/my-assets/main/reflectedxss1.png" alt="Reflected XSS" style="max-width: 100%; height: auto; display: block; margin: auto;">


when enter this `<h1>ducky</h1> `  h1 tags reflected in page


<img src="https://raw.githubusercontent.com/AATHILDUCKY/my-assets/refs/heads/main/xssreflected2.png" alt="Reflected XSS" style="max-width: 100%; height: auto; display: block; margin: auto;">


when i enter `<script>alert(1)</script> `    

<img src="https://raw.githubusercontent.com/AATHILDUCKY/my-assets/refs/heads/main/reflectedxss2.png" alt="Reflected XSS" style="max-width: 100%; height: auto; display: block; margin: auto;">


`<script>alert(document.cookie)<script>`

<img src="https://raw.githubusercontent.com/AATHILDUCKY/my-assets/refs/heads/main/reflectedxss3.png" alt="Reflected XSS" style="max-width: 100%; height: auto; display: block; margin: auto;">


## DVWA - Medium level

in medium level its filtering tags like  `<script>`  it's convert like text format


<img src="https://raw.githubusercontent.com/AATHILDUCKY/my-assets/refs/heads/main/refxssmed1.png" alt="Reflected XSS" style="max-width: 100%; height: auto; display: block; margin: auto;">

so i itry to executre other tags like `<h1>, <h2> , <img>, <Script> , <SCRIPT> ,<SCRIpt>, <scriPT> , <scRIPT>`

<img src="https://raw.githubusercontent.com/AATHILDUCKY/my-assets/refs/heads/main/xssreflected2.png" alt="Reflected XSS" style="max-width: 100%; height: auto; display: block; margin: auto;">

when try this tags that executed in page, so i try this paylod `<img src="#" onerror="onclick(alert(1))/>`

<img src="https://raw.githubusercontent.com/AATHILDUCKY/my-assets/refs/heads/main/Screenshot%202025-02-11%20221149.png" alt="Reflected XSS" style="max-width: 100%; height: auto; display: block; margin: auto;">

## DVWA - High level

in high level its fully filtering and `<script> `  tag but its not filtering the `<h1>, <img> , <p>` i was try this types of tags , that tags was executed

`<h1 onclick='alert(1)'> hello1 </h1>`

when i submit this payload in into input section , that was reflected in the page, when i click that was shows `alert()` pop

<img src="https://raw.githubusercontent.com/AATHILDUCKY/my-assets/refs/heads/main/alertpop.png" alt="Reflected XSS" style="max-width: 100%; height: auto; display: block; margin: auto;">
