---
title: duniq Tool | Remove Duplicates from Subdomain Lists and Output Unique Domains
categories: writeup
tags: ['subdomain', 'golang', 'tool', 'duplicate-removal']
---


To create a Go tool that takes multiple text files, removes duplicates, and writes the unique subdomains to an output file, here's how you can approach it. I'll provide the code, installation instructions, and usage details.

## Go Tool: duniq

1. Code for ``duniq`` Tool:

```golang
package main

import (
	"flag"
	"fmt"
	"io/ioutil"
	"log"
	"os"
	"strings"
)

func main() {
	// Define flags for input files and output file
	var inputFiles string
	var outputFile string

	flag.StringVar(&inputFiles, "c", "", "Comma separated list of input text files")
	flag.StringVar(&outputFile, "o", "output.txt", "Output file name")
	flag.Parse()

	if inputFiles == "" {
		log.Fatal("No input files provided. Use -c flag to provide input files.")
	}

	// Split the input files by comma
	files := strings.Split(inputFiles, ",")
	subdomains := make(map[string]bool)

	// Read and process each file
	for _, file := range files {
		content, err := ioutil.ReadFile(file)
		if err != nil {
			log.Fatalf("Error reading file %s: %v", file, err)
		}

		// Split file content into lines and add to map
		lines := strings.Split(string(content), "\n")
		for _, line := range lines {
			if line != "" {
				subdomains[line] = true
			}
		}
	}

	// Open output file for writing
	output, err := os.Create(outputFile)
	if err != nil {
		log.Fatalf("Error creating output file: %v", err)
	}
	defer output.Close()

	// Write unique subdomains to output file
	for subdomain := range subdomains {
		output.WriteString(subdomain + "\n")
	}

	fmt.Printf("Unique subdomains have been written to %s\n", outputFile)
}
```


## Explanation of the Code:
- Input Files: The program takes a comma-separated list of text files containing subdomains.
- Duplicate Removal: It reads the contents of all files, adds each subdomain to a map (subdomains), ensuring that duplicates are automatically removed.
- Output: After processing, it writes the unique subdomains to the specified output file (default is output.txt).

## 2. Installation and Usage:
### Step 1: Install Go

If you don't have Go installed, you can install it by following the instructions from Go's official website.

### Step 2: Save the Code to a File
Save the code into a file, for example, duniq.go.

### Step 3: Build the Tool
Navigate to the directory where you saved duniq.go and run the following command to build the executable:

```bash
go build duniq.go
```
This will generate an executable named `duniq` in the current directory.

### Step 4: Usage
Once the tool is built, you can use it in the terminal. Here’s how:
```bash
./duniq -c file1.txt,file2.txt -o output.txt
```

- ``-c`` flag: Provide a comma-separated list of the input files (e.g.,`` file1.txt,file2.txt``).
- ``-o`` flag: Specify the output file name (default is ``output.txt`` if not specified).


## Example:
Let's say you have two files:

``file1.txt``
```bash
example1.com
example2.com
example3.com
```

``file2.txt``
```bash
example2.com
example4.com
example5.com
```

Running the following command:
```bash
./duniq -c file1.txt,file2.txt -o output.txt
```

Will result in an ``output.txt`` with:

```bash
example1.com
example2.com
example3.com
example4.com
example5.com
```