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

`C s1 ls`

Run the last command:
`C !`

Run the command with current line:
`C !l`

Run the command with current word:
`C !w`

Run the command stored in vim register:
`C @a @b`