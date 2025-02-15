---
title: picoCTf verify 2024
categories: picoctf
tags: ['picoctf']
---
# PicoCTF Verify 2024 (Forensics)

In this challenge, we need to find the correct encrypted file and decrypt it to get the flag. Here’s how I solved it:

## Step 1: Check the Given Files

Running `ls` shows three items:
- `checksum.txt` – contains a SHA-256 hash
- `decrypt.sh` – a script to decrypt files
- `files/` – a directory with multiple files


## Step 2: Find the Matching File

The hash inside `cat checksum.txt` is:


```bash
ctf-player@pico-chall$ cat checksum.txt
3ad37ed6c5ab81d31e4c94ae611e0adf2e9e3e6bee55804ebc7f386283e366a4
```

the `decrypt.sh` insite

```
ctf-player@pico-chall$ cat decrypt.sh

#!/bin/bash

        # Check if the user provided a file name as an argument
        if [ $# -eq 0 ]; thenctf-player@pico-chall$ cat decrypt.sh
            echo "Expected usage: decrypt.sh <filename>"
            exit 1
        fi

        # Store the provided filename in a variable
        file_name="$1"

        # Check if the provided argument is a file and not a folder
        if [ ! -f "/home/ctf-player/drop-in/$file_name" ]; then
            echo "Error: '$file_name' is not a valid file. Look inside the 'files' folder with 'ls -R'!"
            exit 1
        fi

        # If there's an error reading the file, print an error message
        if ! openssl enc -d -aes-256-cbc -pbkdf2 -iter 100000 -salt -in "/home/ctf-player/drop-in/$file_name" -k picoCTF; then
            echo "Error: Failed to decrypt '$file_name'. This flag is fake! Keep looking!"
        fi

```

To find which file matches this hash, I ran:

```
ctf-player@pico-chall$ sha256sum files/* | grep 3ad37ed6c5ab81d31e4c94ae611e0adf2e9e3e6bee55804ebc7f386283e366a4

3ad37ed6c5ab81d31e4c94ae611e0adf2e9e3e6bee55804ebc7f386283e366a4  files/e018b574
```

This revealed that `files/e018b574` has the matching hash.

## Step 3: Decrypt the File

The `decrypt.sh` script uses OpenSSL to decrypt files. Running:

```
./decrypt.sh files/e018b574
```

```
ctf-player@pico-chall$ ./decrypt.sh files/e018b574
picoCTF{trust_but_verify_e018b574}
```