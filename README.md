multiterm
=========

multiterm let you send your command to multi terminal.
The plugin only support neovim.


##Installation

For Plug

`Plug 'kjelly/vim-multiterm'`

For NeoBundle

`NeoBundle 'kjelly/vim-multiterm'`

Note: The plugin is remote-plugin.
It's needed that run `UpdateRemotePlugins` again.


## Use Case

Search in the google in the vim terminal.
[w3m](https://raw.githubusercontent.com/kjelly/nvim-multiterm/master/docs/w3m.gif)

Search in the stackoverflow in the vim terminal.
[how2](https://raw.githubusercontent.com/kjelly/nvim-multiterm/master/docs/how2.gif)

##Usage

Run `ls -al` in the last terminal:

`C ls -al`

Run `ls -al` in all terminals:

`C a ls -al`

Show all the job id of terminal:

`C l`

Run `ls -al` in these terminal whose job id is 1 or 3:

`C 1,3 ls -al`

Store command `ls` in command map 1:

`C s1 ls`

Run command which is stored in command map 1:

`C r1`

Run the last command:

`C !`

Run the command with current line:

`C !l`

Run the command with current word:

`C !w`

Run the command stored in vim register:

`C @a @b`

Name the current terminal to w3m:

`C n w3m`

Name the terminal with job id 5 to w3m:

`C n w3m 5`

Run the command, 'ls', in the terminal with the name w3m:

`C w3m, ls`

Use w3m to open google in the terminal whose name is w3m:

Note: The feature require w3m program and psutil python package

`C w google.com`
