from math import trunc

class ALU:
    def __init__(self, x=0, y=0, z=0, w=0, buffer=None, fname='input.txt'):
        self.x = x
        self.y = y
        self.z = z
        self.w = w
        self.buffer = buffer
        self.bufferloc = 0
        self.fname = fname

        self.cmd_dict = {'inp': self.inp,
                         'add': self.add,
                         'mul': self.mul,
                         'div': self.div,
                         'mod': self.mod,
                         'eql': self.eql}

    def __str__(self):
        return f"ALU(x={self.x}, y={self.y}, z={self.z}, w={self.w})"

    def monad(self, buffer=None, fname=None, verbose=False):
        if buffer is not None:
            self.buffer = str(buffer)
            self.bufferloc = 0
            self.x = self.y = self.z = self.w = 0
        if fname is None:
            fname = self.fname

        with open(fname) as f:
            for line in f:
                self.parse_command(line)
        print(f"{self.z = }")


    def command(self, cmd, *args):
        return self.cmd_dict[cmd](*args)

    def parse_command(self, cmdstr):
        condition_args = lambda x: x if x in ('x', 'y', 'z', 'w') else int(x)
        cmdlist = cmdstr.strip().split()
        cmd = cmdlist[0]
        args = cmdlist[1:]
        args = list(map(condition_args, args))
        self.command(cmd, *args)

    def inp(self, *args, verbose=False):
        setattr(self, args[0], int(self.buffer[self.bufferloc]))
        self.bufferloc += 1
        return True

    def _binop(self, cmd, *args):
        a, b = args
        if b in ('x', 'y', 'z', 'w'):
            b = getattr(self, b)
        aval = getattr(self, a)
        if cmd == 'add':
            newval = aval + b
        elif cmd == 'mul':
            newval = int(aval*b)
        elif cmd == 'div':
            newval = trunc(aval/b)
        elif cmd == 'mod':
            newval = aval % b
        elif cmd == 'eql':
            newval = 1 if (aval == b) else 0
        setattr(self, a, newval)
        return True        

    def add(self, *args):
        return self._binop('add', *args)

    def mul(self, *args):
        return self._binop('mul', *args)

    def div(self, *args):
        return self._binop('div', *args)

    def mod(self, *args):
        return self._binop('mod', *args)

    def eql(self, *args):
        return self._binop('eql', *args)


def test():
    alu = ALU()
    alu.buffer = '1234567890'

    cmds = ['inp x',
            'inp y',
            'inp z',
            'inp w',
            'add x 8', 
            "mul x 0",
            'add z w',
            'mul z -1',
            'div z 2',
            'add x 5',
            'mod z x',
            'eql z x',
            'eql z z'
            ]

    print(alu)
    for cmd in cmds:
        print(cmd)
        alu.parse_command(cmd)
        print(alu)



alu = ALU()

id_max = 99999795919456
alu.monad(id_max)
print(f"id = {id_max}: PASS" if alu.z == 0 else "FAIL")

id_min = 45311191516111
alu.monad(id_min)
print(f"id = {id_min}: PASS" if alu.z == 0 else "FAIL")
