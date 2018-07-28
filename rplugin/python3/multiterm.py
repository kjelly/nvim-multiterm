import re
import neovim
import enum
try:
    import psutil
except ImportError:
    psutil = None


def isNumber(x):
    return x in '1234567890'


class Result(enum.Enum):
    BY_PASS = 1
    HANDLED = 2
    UNHANDLED = 3


@neovim.plugin
class MultiTerm(object):

    def __init__(self, nvim):
        self.nvim = nvim
        self.data = {}
        self.command_map = {}
        self.name_map = {}
        self.last_term_job_id = None
        self.last_command = ''
        self.name_list = ['one', 'two', 'three', 'four', 'five', 'six',
                          'seven', 'eight', 'nine', 'ten']
        self.name_index = 0
        self.browser = self.nvim.eval("expand('$BROWSER')")
        if self.browser == '$BROWSER':
            self.browser = 'w3m'

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

    def subcommand_a(self, arg0, args, range):
        cmd = ' '.join(args[1:]) + '\n'
        self.run_in_all_terminal(cmd)
        return Result.HANDLED

    def subcommand_s(self, arg0, args, range):
        if len(arg0) == 2 and arg0[0] == 's' and isNumber(arg0[1]):
            cmd = ' '.join(args[1:]) + '\n'
            self.command_map[arg0[1]] = cmd
            return Result.HANDLED
        return Result.UNHANDLED

    def subcommand_r(self, arg0, args, range):
        if arg0[0] == 'r' and len(arg0) == 1:
            self.echo(arg0)
            cmd = self.command_map.get(arg0[1], '')
            self.run(self.last_term_job_id, cmd)
            return Result.HANDLED
        elif arg0[0] == 'r' and len(arg0) == 2 and isNumber(arg0[1]):
            # C g1 : run command 1 stored in command map.
            self.echo(arg0)
            cmd = self.command_map.get(arg0[1], '')
            self.run(self.last_term_job_id, cmd)
            return Result.HANDLED
        return Result.UNHANDLED

    def subcommand_n(self, arg0, args, range):
        if arg0 in ['n', 'N'] and len(args) > 1:
            if len(args) == 2:
                try:
                    filename = self.nvim.eval("expand('%:p')").split(',')[0]
                    job_id = self.nvim.eval('expand(b:terminal_job_id)')
                    self.name_map[job_id] = args[1]
                    self.nvim.command("keepalt file %s,%s" % (filename, args[1]))
                except:
                    self.name_map[self.last_term_job_id] = args[1]
                return Result.HANDLED
            elif len(args) > 2:
                self.name_map[args[2]] = args[1]
                return Result.HANDLED
        return Result.UNHANDLED

    def subcommand_g(self, arg0, args, range):
        name_or_id = args[1]
        inv_name_map = {v: k for k, v in self.name_map.items()}
        inv_data_map = {v: k for k, v in self.data.items()}
        r = inv_name_map.get(name_or_id, None)
        if r is None:
            r = name_or_id
        r = inv_data_map.get(r, None)
        if r is None:
            return Result.BY_PASS
        self.nvim.command("buffer %s" % r)
        return Result.HANDLED

    def subcommand_w(self, arg0, args, range):
        if psutil is None:
            return Result.BY_PASS
        inv_name_map = {v: k for k, v in self.name_map.items()}
        if inv_name_map.get('w3m', None) is None:
            self.nvim.command("terminal")
            self.nvim.command("C n w3m")

        url = ' '.join(args[1:]) + '\n'
        self.kill_and_run('w3m', '%s %s' % (self.browser, url))
        self.nvim.command("normal! i")
        return Result.HANDLED

    def subcommand_k(self, arg0, args, range):
        if psutil is None:
            return Result.BY_PASS
        name_list = args[1].split(',')
        if len(name_list) < 2:
            return
        cmd = ' '.join(args[2:]) + '\n'
        for i in name_list:
            if i == '':
                continue
            self.kill_and_run(i, cmd)
            self.nvim.command("normal! G")
        return Result.HANDLED

    def kill_and_run(self, name, command):
        inv_name_map = {v: k for k, v in self.name_map.items()}
        inv_data_map = {v: k for k, v in self.data.items()}
        job_id = inv_name_map.get(name, None)
        if job_id is None:
            return
        file_name = inv_data_map[job_id]
        self.nvim.command("buffer %s" % file_name)
        pid = file_name.split('/')[-1].split(':')[0]
        p = psutil.Process(pid=int(pid, 10))
        childrens = p.children()
        for i in childrens:
            i.kill()
        self.run(job_id, command)
        return Result.HANDLED

    def subcommand_l(self, arg0, args, range):
        # C l : list all terminal.
        if len(arg0) > 1:
            return Result.UNHANDLED
        text = ''
        for i in self.data:
            job_id = self.data[i]
            text += '%s => %s, %s\n' % (job_id, i,
                                        self.name_map.get(job_id, ''))
        try:
            job_id = self.nvim.eval('expand(b:terminal_job_id)')
        except:
            pass
        text += 'current job_id=%s, name=%s' % (job_id, self.name_map[job_id])
        self.echo(text)
        return Result.HANDLED

    def subcommand_empty(self, arg0, args, range):
        return Result.UNHANDLED

    @neovim.command("C", range='', nargs='*', sync=True)
    def command(self, args, range):
        if len(args) < 1:
            return

        if self.last_term_job_id is None:
            self.nvim.command("split")
            self.nvim.command("wincmd j")
            self.nvim.command("terminal")

        self.replace_args(args)

        function_map = {
            'a': self.subcommand_a,
            'g': self.subcommand_g,
            'l': self.subcommand_l,
            'n': self.subcommand_n,
            'r': self.subcommand_r,
            's': self.subcommand_s,
            'w': self.subcommand_w,
            'k': self.subcommand_k,
        }

        arg0 = args[0]

        result = function_map.get(arg0[0],
                                  self.subcommand_empty)(arg0, args, range)

        if result == Result.BY_PASS or result == Result.HANDLED:
            return

        if re.match(r'(\d+,)*\d+', arg0):
            # C 1, 3 ls : run ls in terminal 1, terminal 3.
            cmd = ' '.join(args[1:]) + '\n'
            for i in arg0.split(','):
                self.run(i, cmd)
        elif re.match(r'(\w+,)+', arg0):
            cmd = ' '.join(args[1:]) + '\n'
            name_list = arg0.split(',')
            inv_name_map = {v: k for k, v in self.name_map.items()}
            ever_run = False
            for name in name_list:
                job_id = inv_name_map.get(name, None)
                if job_id is None:
                    continue
                self.run(job_id, cmd)
                ever_run = True
            if ever_run is False:
                self.run(self.last_term_job_id, cmd)
        else:
            cmd = ' '.join(args[:]) + '\n'
            self.run(self.last_term_job_id, cmd)

    @neovim.autocmd('TermOpen', eval='expand("<afile>")', sync=True,
                    pattern='*fish*')
    def on_termopen(self, filename):
        job_id = self.nvim.eval('expand(b:terminal_job_id)')
        self.data[filename] = job_id
        self.last_term_job_id = job_id
        if self.name_index < 10:
            name = self.name_list[self.name_index]
            self.name_map[job_id] = name
            self.nvim.command("keepalt file %s,%s" % (filename, name))
            self.name_index += 1

    @neovim.autocmd('BufWinEnter', eval='expand("%:p")', sync=True,
                    pattern='*fish*')
    def on_buffer_win_enter(self, filename):
        try:
            job_id = self.nvim.eval('expand(b:terminal_job_id)')
            if self.name_map.get(job_id, '') != 'w3m':
                self.last_term_job_id = job_id
        except:
            pass

    @neovim.autocmd('BufEnter', eval='expand("%:p")', sync=True,
                    pattern='*fish*')
    def on_buffer_enter(self, filename):
        if psutil is None:
            return
        try:
            pid = filename.split('/')[-1].split(':')[0]
            p = psutil.Process(pid=int(pid, 10))
            childrens = p.children()
            if len(childrens) > 0 and childrens[0].name() == 'w3m':
                self.nvim.command("normal! g")
                self.nvim.command("normal! i")
        except:
            pass
