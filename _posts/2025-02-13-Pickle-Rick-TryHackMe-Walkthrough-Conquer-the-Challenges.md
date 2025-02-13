---
title: Pickle Rick TryHackMe Walkthrough Conquer the Challenges!
categories: tryhackme
tags: ['tryhackme']
---
##  Pickle Rick TryHackMe Walkthrough: Conquer the Challenges!


<iframe width="560" height="315" src="https://www.youtube.com/embed/cqvqQF6m0vw?si=vgkidSB2KODZSt9Y" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>

Tryhackme-pickle-rick is a must in CTF. This is one of the easiest and most interesting rooms on Tryhackme. Three flags should be found in this. Okay, let's go face the CTF challenge.


<img src="https://raw.githubusercontent.com/AATHILDUCKY/my-assets/refs/heads/main/Pickle%20Rick%20-%20TryHackMe%20Walkthrough%20-%20CTF%20Challenge.png" alt="Reflected XSS" style="max-width: 100%; height: auto; display: block; margin: auto;">


## Step 1: Check connectivity.

After clicking Start Machine in Tryhackme, connectivity is available after a few minutes. You can use the ping command to check it.

<img src="https://raw.githubusercontent.com/AATHILDUCKY/my-assets/refs/heads/main/pickle%20rick%20tryhackme%20walkthrough%20-%20check%20connectivity.png" alt="Reflected XSS" style="max-width: 100%; height: auto; display: block; margin: auto;">


## Step 2: Information Gathering and Enumeration

What ports are open? You can use the simple Nmap scan command below to find out what services are running on it.

### nmap scanning

```
nmap -vv <host_IP>
```

**`-v`** is verbose mode, **`-vv`** double verbose mode can increase speed.


And deep scanning of those ports can be done. By doing this deep scanning, any sensitive and usable data can be found.

Only ports 22 and 80 will be open. So only these two ports can be scanned using Nmap scripts.

```
nmap -vv -sV -sC -A -p22,80 <host_IP>
```


<img src="https://raw.githubusercontent.com/AATHILDUCKY/my-assets/refs/heads/main/pickle%20rick%20tryhackme%20walkthrough%20-%20nikto%20scanning.png" alt="Reflected XSS" style="max-width: 100%; height: auto; display: block; margin: auto;">


`-sV` service version

`-sC` default nmap scripts

`-A`  aggressive mode


### nikto scanning

Gathering information by scanning using the Nikto tool , when I go to the CTF challenge, after gathering information using various tools, I go to the next step.

```
nikto -h <host_ip>
```

<img src="https://raw.githubusercontent.com/AATHILDUCKY/my-assets/refs/heads/main/pickle%20rick%20tryhackme%20walkthrough%20-%20nikto%20scanning%20(1).png" alt="Reflected XSS" style="max-width: 100%; height: auto; display: block; margin: auto;">



### Gobuster enumeration

Next, let's move on to directory enumeration. The Gobuster tool can be used for directory discovery. And you can use Seclist for wordlists.

```
gobuster dir -w http://10.10.66.10/ -w Seclist/Discovery/Web-Content/common.txt
```


<img src="https://raw.githubusercontent.com/AATHILDUCKY/my-assets/refs/heads/main/pickle%20rick%20tryhackme%20gobuster%20directory%20enumeration.png" alt="Reflected XSS" style="max-width: 100%; height: auto; display: block; margin: auto;">

Just search the Pickle Rick IP address in the browser, and a web home page will open.

<img src="https://raw.githubusercontent.com/AATHILDUCKY/my-assets/refs/heads/main/pickle%20rick%20tryhackme%20visit%20website.png" alt="Reflected XSS" style="max-width: 100%; height: auto; display: block; margin: auto;">


By checking the source code, we will get the user name in the HTML command.

<img src="https://raw.githubusercontent.com/AATHILDUCKY/my-assets/refs/heads/main/pickle%20rick%20view%20page%20source%20code%20-%20get%20user%20name.png" alt="Reflected XSS" style="max-width: 100%; height: auto; display: block; margin: auto;">

Generally, every website has robots.txt, which is used to show the search engine crawler what can be accessed and what cannot be accessed. It may contain sensitive information.

<img src="https://raw.githubusercontent.com/AATHILDUCKY/my-assets/refs/heads/main/pickle%20rick%20tryhackme%20robots_txt%20.png" alt="Reflected XSS" style="max-width: 100%; height: auto; display: block; margin: auto;">


The login page is available when gobuster enumeration is done, in which the username available in the home page source and the password available in robots.txt are used as the login page.

**user name : `R1ckRu13s`**

**password: `Wubbalubbadubdub`**


<img src="https://raw.githubusercontent.com/AATHILDUCKY/my-assets/refs/heads/main/pickle%20rick%20tryhackme%20portal%20login%20page%20-%20pickle%20rick%20username%20and%20password.png" alt="Reflected XSS" style="max-width: 100%; height: auto; display: block; margin: auto;">

After getting login access, a command panel is available. It contains a general set of files and directories to execute the ls command.

<img src="https://raw.githubusercontent.com/AATHILDUCKY/my-assets/refs/heads/main/pickle%20rick%20tryhackme%20portal%20command%20panel%20list%20.png" alt="Reflected XSS" style="max-width: 100%; height: auto; display: block; margin: auto;">

But when using the **`cat`** and **`head`** commands to read that file, this command was blocked.

<img src="https://raw.githubusercontent.com/AATHILDUCKY/my-assets/refs/heads/main/cat%20command%20disabled%20in%20pickle%20rick%20tyhackme.png" alt="Reflected XSS" style="max-width: 100%; height: auto; display: block; margin: auto;">


## Step 4: Get reverse shell

Now several commands to get reverse shell

`nc --help`

`ncat --help`

`netcat --help`

`python --version`

`python3 --version`

By executing a few commands like this, I learned how to get a reverse shell.

<img src="https://raw.githubusercontent.com/AATHILDUCKY/my-assets/refs/heads/main/pickle%20rick%20reverse%20shell%20-%20using%20python.png" alt="Reflected XSS" style="max-width: 100%; height: auto; display: block; margin: auto;">

It turns out that Python3 can also be used. Ok, next, I got reverse shell scripts from the Pentest Monkey website. 

<img src="https://raw.githubusercontent.com/AATHILDUCKY/my-assets/refs/heads/main/pickle%20rick%20reverse%20shell%20command.png" alt="Reflected XSS" style="max-width: 100%; height: auto; display: block; margin: auto;">


After changing the IP address and port number in this Python script, you can execute it in the command panel.

But before executing the command, start the netcat listener.

<img src="https://raw.githubusercontent.com/AATHILDUCKY/my-assets/refs/heads/main/listen%20for%20reverse%20shell%20-%20pickle%20rick%20tryhackme.png" alt="Reflected XSS" style="max-width: 100%; height: auto; display: block; margin: auto;">

after executing the python script , i got reverse shell

<img src="https://raw.githubusercontent.com/AATHILDUCKY/my-assets/refs/heads/main/i%20got%20reverse%20shell%20-%20pickle%20rick%20tryhackme.png" alt="Reflected XSS" style="max-width: 100%; height: auto; display: block; margin: auto;">



## Step 5 : Privilege Escalation

Use `sudo -l` for privilege escalation

`(ALL) NOPASSWD  : ALL`

its so easy

`sudo /bin/bash` Use this command to gain root access.

<img src="https://raw.githubusercontent.com/AATHILDUCKY/my-assets/refs/heads/main/privilege%20escalation%20-%20pickle%20rick%20tryhackme.png" alt="Reflected XSS" style="max-width: 100%; height: auto; display: block; margin: auto;">


i got root ☺️

To get a more interactive shell

```
python3 -c 'import pty;pty.spawn("/bin/bash")'
```


## Answer of Pickle Rick THM

### 1. What is the first ingredient that rick needs?

<img src="https://raw.githubusercontent.com/AATHILDUCKY/my-assets/refs/heads/main/What%20is%20the%20first%20ingredient%20that%20rick%20needs.png" alt="Reflected XSS" style="max-width: 100%; height: auto; display: block; margin: auto;">


### 2. What is the secoond ingredient in Rick's potion?

<img src="https://raw.githubusercontent.com/AATHILDUCKY/my-assets/refs/heads/main/What%20is%20the%20secoond%20ingredient%20in%20Rick's%20potion.png" alt="Reflected XSS" style="max-width: 100%; height: auto; display: block; margin: auto;">


### 3. What is the last and final ingredient?

<img src="https://raw.githubusercontent.com/AATHILDUCKY/my-assets/refs/heads/main/What%20is%20the%20last%20and%20final%20ingredient.png" alt="Reflected XSS" style="max-width: 100%; height: auto; display: block; margin: auto;">
