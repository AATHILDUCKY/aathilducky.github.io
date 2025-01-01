---
title: "Set Up nvim-tree in vim plug"
categories: Vim Set-Up-nvim-tree
tags: ['nvim-tree','vim','vim-plugin']
---
# Steps to Set Up nvim-tree with Vim-Plug

## Install nvim-tree Plugin

Add the `nvim-tree` plugin to your `init.vim` or `init.lua` using Vim-Plug:

```vim
call plug#begin('~/.local/share/nvim/plugged')

" Add nvim-tree plugin
Plug 'kyazdani42/nvim-tree.lua'

call plug#end()
```

## Install the Plugin

open neovim and run

```vim
:PlugInstall

```

## Configure nvim-tree

Add the following configuration in your ``init.vim`` or ``init.lua``

```vim
" Basic nvim-tree setup
lua << EOF
require'nvim-tree'.setup {}
EOF
```

## Open nvim-tree

In Neovim, open the tree view using:

```
:NvimTreeToggle
```
