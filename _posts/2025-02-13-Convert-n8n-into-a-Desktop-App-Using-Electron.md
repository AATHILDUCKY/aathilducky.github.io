---
title: "Convert n8n into a Desktop App Using Electron"
categories: n8n
tags: ['n8n']
---
# Convert n8n into a Desktop App Using Electron

### **Step 1: Install Electron**

First, install Electron globally:

```
npm install -g electron
```

### **Step 2: Create an Electron Project**

Create a new folder and navigate into it:

```
mkdir n8n-desktop && cd n8n-desktop
```

Initialize a new Node.js project:

```
npm init -y
```

Install Electron as a dependency:

```
npm install electron
```

### **Step 3: Create `main.js` (Electron Main Process)**

Inside `n8n-desktop`, create a file named `main.js` and add the following code:

```javascript
const { app, BrowserWindow } = require('electron');
const { exec } = require('child_process');

let mainWindow;

app.on('ready', () => {
    // Start n8n process
    const n8nProcess = exec('n8n', (error, stdout, stderr) => {
        if (error) {
            console.error(`Error starting n8n: ${error}`);
        }
        console.log(stdout);
    });

    // Create a new window
    mainWindow = new BrowserWindow({
        width: 1200,
        height: 800,
        webPreferences: {
            nodeIntegration: false
        }
    });

    // Load n8n UI
    mainWindow.loadURL('http://localhost:5678');

    mainWindow.on('closed', () => {
        mainWindow = null;
        n8nProcess.kill(); // Stop n8n when the app is closed
    });
});

```

### **Step 4: Modify `package.json`**

Open `package.json` and add the following:

```json
"main": "main.js",
"scripts": {
  "start": "electron ."
}
```

### **Step 5: Run Your Desktop App**

Now, start the Electron app:

```json
npm start
```

### **Step 6: Package as a Desktop App**

You can package it into an executable using  **Electron Packager** :

```bash
npm install -g electron-packager
electron-packager . n8n-desktop --platform=win32 --arch=x64 --out=dist
```

For  **Mac** :

```bash
electron-packager . n8n-desktop --platform=darwin --arch=x64 --out=dist
```

For  **Linux** :

```bash
electron-packager . n8n-desktop --platform=linux --arch=x64 --out=dist
```

its generate executable file in `dist/`  folder , execue that

<img src="https://raw.githubusercontent.com/AATHILDUCKY/my-assets/refs/heads/main/n8n.png" alt="Reflected XSS" style="max-width: 100%; height: auto; display: block; margin: auto;">
