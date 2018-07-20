import re
import neovim


def isNumber(x):
    return x in '1234567890'


@neovim.plugin
class MultiTerm(object):

    def __init__(self, nvim):
        self.nvim = nvim
        self.data = {}
        self.command_map = {}
        self.last_term_job_id = None
        self.last_command = ''

    def write_text(self, job_id, data):
        self.nvim.call('jobsend', int(job_id), data)

    def run(self, job_id, cmd):
        self.last_command = cmd.strip()
        self.write_text(job_id, cmd)

    def run_in_all_terminal(self, cmd):
        for i in self.data:
            self.run(int(self.data[i]), cmd)

    def echo(self, data):
        self.nvim.command('echo "%s"' % data)

    def replace_args(self, args):
        for i in range(len(args)):
            val = args[i]
            if val == '!':
                args[i] = self.last_command
            elif val == '!l':
                args[i] = self.nvim.current.line.strip()
            elif val == '!w':
                self.nvim.command('normal! viw"*y')
                args[i] = self.nvim.eval('@*')
            elif len(val) == 2 and val[0] == '@':
                args[i] = self.nvim.eval('@' + val[1])

    @neovim.command("C", range='', nargs='*')
    def command(self, args, range):
        if len(args) < 1:
            return

        if self.last_term_job_id is None:
            self.nvim.command("split")
            self.nvim.command("wincmd j")
            self.nvim.command("terminal")

        self.replace_args(args)

        arg0 = args[0]
        if arg0 in ['a', 'A']:
            # C a ls : Run ls in all terminal
            cmd = ' '.join(args[1:]) + '\n'
            self.run_in_all_terminal(cmd)
        elif len(arg0) == 2 and arg0[0] == 's' and isNumber(arg0[1]):
            # C s1 ls : store command `ls` in command map 1.
            cmd = ' '.join(args[1:]) + '\n'
            self.command_map[arg0[1]] = cmd
        elif arg0[0] == 'g' and len(arg0) == 1:
            # C g : show all commmand stored in command map.
            text = ''
            for i in self.command_map:
                text += '%s => %s' % (i, self.command_map[i])
            self.echo(text)
        elif arg0[0] == 'g' and len(arg0) == 2 and isNumber(arg0[1]):
            # C g1 : run command 1 stored in command map.
            self.echo(arg0)
            cmd = self.command_map.get(arg0[1], '')
            self.run(self.last_term_job_id, cmd)

        elif arg0 in ['l', 'L']:
            # C l : list all terminal.
            text = ''
            for i in self.data:
                text += '%s => %s\n' % (self.data[i], i)
            self.echo(text)
        elif re.match(r'(\d+,)*\d+', arg0):
            # C 1, 3 ls : run ls in terminal 1, terminal 3.
            cmd = ' '.join(args[1:]) + '\n'
            for i in arg0.split(','):
                self.run(i, cmd)
        else:
            cmd = ' '.join(args[:]) + '\n'
            self.run(self.last_term_job_id, cmd)

    @neovim.autocmd('TermOpen', eval='expand("<afile>")', sync=True,
                    pattern='*fish*')
    def on_termopen(self, filename):
        job_id = self.nvim.eval('expand(b:terminal_job_id)')
        self.data[filename] = job_id
        self.last_term_job_id = job_id
