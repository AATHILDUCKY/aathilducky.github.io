---
title: "install vim-plug"
categories: Vim install-vim
tags: ['neovim','vim']
---
# vim-plug: How to Install (Vim and Neovim)

## What is vim-plug?

vim-plug is a lightweight plugin manager for Vim and Neovim. It simplifies adding, updating, and removing plugins in your editor without manual downloads or complicated setups.

---

## Installation Process

### **Step 1: Install Neovim (if not already installed)**

```bash
sudo apt update
sudo apt install neovim -y
```

### **Step 2: Install `curl` (if not installed)**

```bash
sudo apt install curl -y
```

### **Step 3: Download and Install vim-plug**

```bash
curl -fLo ~/.local/share/nvim/site/autoload/plug.vim --create-dirs \
https://raw.githubusercontent.com/junegunn/vim-plug/master/plug.vim
```

- vim-plug will be stored in `~/.local/share/nvim/site/autoload/plug.vim`.

### **Step 4: Configure vim-plug**

1. Create or edit the Neovim configuration file:

   ```bash
   mkdir -p ~/.config/nvim
   nano ~/.config/nvim/init.vim
   ```
2. Add the following lines to initialize vim-plug:

```vim
call plug#begin('~/.local/share/nvim/plugged')

" Example plugin
Plug 'preservim/nerdtree'

call plug#end()
```

- `call plug#begin()` initializes vim-plug and specifies the plugin installation directory.
- `Plug '<plugin-repo>'` specifies a plugin from its GitHub repository.
- `call plug#end()` ends the plugin section.

### **Step 5: Install Plugins**

1. Open Neovim:
   ```bash
   nvim
   ```
2. Run the following command to install the plugins listed in `init.vim`:
   ```vim
   :PlugInstall
   ```

---

## How vim-plug Works

### **Plugin Management**

- vim-plug uses Git to fetch plugins from their repositories.
- Installed plugins are stored in `~/.local/share/nvim/plugged/`.

### **Commands**

| Command          | Description                                            |
| ---------------- | ------------------------------------------------------ |
| `:PlugInstall` | Installs all plugins listed in the configuration file. |
| `:PlugUpdate`  | Updates all installed plugins.                         |
| `:PlugClean`   | Removes plugins not listed in your configuration file. |
| `:PlugStatus`  | Displays the current status of plugins.                |
| `:PlugDiff`    | Shows Git changes in installed plugins.                |

### **On-demand Loading**

Plugins can be lazily loaded to improve startup time. Example:

```vim
Plug 'junegunn/fzf', { 'on': 'Files' }
```

This loads the plugin only when the `:Files` command is run.

---

## Example Workflow

### **1. Add a Plugin**

1. Update your `init.vim`:
   ```vim
   call plug#begin('~/.local/share/nvim/plugged')

   Plug 'tpope/vim-surround'  " Adds surround text editing functionality

   call plug#end()
   ```
2. Save the file and run:
   ```vim
   :PlugInstall
   ```

### **2. Update Plugins**

Run the following command to update plugins:

```vim
:PlugUpdate
```

### **3. Remove a Plugin**

1. Delete the plugin line from `init.vim`.
2. Run:
   ```vim
   :PlugClean
   ```

---

## Why Use vim-plug?

### **Ease of Use**

Simplifies managing plugins with intuitive commands.

### **Performance**

Supports parallel installation for faster downloads.

### **Flexibility**

Allows on-demand loading for improved startup times.
