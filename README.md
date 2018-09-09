multiterm
=========

multiterm let you send your command to multi terminal.
The plugin only support neovim.


## Installation

For Plug

`Plug 'kjelly/vim-multiterm'`

For NeoBundle

`NeoBundle 'kjelly/vim-multiterm'`

Note: The plugin is remote-plugin.
It's needed that run `UpdateRemotePlugins` again.


## Use Case

Sample config:

```vim
let mapleader = ","
let maplocalleader = "_"
silent! call plug#begin('~/.config/nvim/plugged')
Plug 'kjelly/nvim-multiterm', { 'do': ':UpdateRemotePlugins'}
call plug#end()

nnoremap <leader>lg :C w 'https://www.google.com/search?q=<c-r>=&filetype<cr> '<left>
nnoremap <leader>lh :C k how2, how2 -l <c-r>=&filetype<cr><space>

```

You also need w3m, [psutils](https://pypi.org/project/psutil/), [how2](https://www.npmjs.com/package/how2)

Step:

```
:terminal
:C n how2
,lh
```


Search in the google in the vim terminal.
![w3m](https://raw.githubusercontent.com/kjelly/nvim-multiterm/master/docs/w3m.gif)


Search in the stackoverflow in the vim terminal.
![how-2](https://raw.githubusercontent.com/kjelly/nvim-multiterm/master/docs/how-2.gif)

## Usage

- Run `ls -al` in the last terminal:

  `C ls -al`

- Run `ls -al` in all terminals:

  `C a ls -al`

- Show all the job id of terminal:

  `C l`

- Run `ls -al` in these terminal whose job id is 1 or 3:

  `C 1,3 ls -al`

- Store command `ls` in command map 1:

  `C s1 ls`

- Run command which is stored in command map 1:

  `C r1`

- Run the last command:

  `C !`

- Run the command with current line:

  `C !l`

- Run the command with current word:

  `C !w`

- Run the command stored in vim register:

  `C @a @b`

- Name the current terminal to w3m:

  `C n w3m`

- Run the command, 'ls', in the terminal with the name w3m:

  `C w3m, ls`

- Use w3m to open google in the terminal whose name is w3m:

  Note: The feature require w3m program and psutil python package

  `C w google.com`

- Run the command, 'ls', in the terminal with the name w3m:

  It will kill any process before running the new command.

  `C k w3m, ls -al`
