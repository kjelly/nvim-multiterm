let s:plugin = fnamemodify(resolve(expand('<sfile>:p')), ':h') . '/multiterm.py'
execute "pyfile" fnamemodify(resolve(expand('<sfile>:p')), ':h') . '/multiterm.py'
autocmd TermOpen *sh* :py multiterm.on_termopen()
autocmd BufWinEnter *sh* :py multiterm.on_buffer_win_enter()
autocmd BufEnter *sh* :py multiterm.on_buffer_enter()

command! -nargs=* C py multiterm.command('<args>', '')
