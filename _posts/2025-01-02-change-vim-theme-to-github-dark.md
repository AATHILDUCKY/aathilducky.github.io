---
title: "Add GitHub Dark Colorscheme in to Neovim"
categories: Vim change-vim-theme
tags: ['neovim','vim','vim-theme']
---
Add **GitHub Dark** Colorscheme in to Neovim
========================================

### Steps to Add **GitHub Dark** Colorscheme in Neovim

### **Install GitHub Theme Plugin**:

Use a plugin manager like `vim-plug`, `packer.nvim`, or `catppuccin-nvim`.

```vim
call plug#begin('~/.local/share/nvim/plugged')

" Add GitHub theme
Plug 'projekt0n/github-nvim-theme'

call plug#end()
```

### Install the Plugin:

After adding the plugin, run:

```
:PlugInstall

```

or for `packer.nvim`:

```
:PackerSync
```

### **Configure the Colorscheme** :

Set the colorscheme in your configuration:

```
colorscheme github_dark

```
