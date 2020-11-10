class Command:
    commands = {}

    @classmethod
    def add_command(cls, command):
        cls.commands[command.name] = command
    
    @classmethod
    def exec_command(cls, name, *args):
        if cls.commands.get(name) is None:
            print(f'No such command: {name}')
            return
        else:
            cls.commands[name].execute(*args)

    def __init__(self, name, argcounts, help=""):
        self.name = name  # Name of command
        self.func = None  #  function(*args)
        self.argcounts = argcounts  # Variations of argument count
        self.helpstr = help

    def execute(self, *args):
        if len(args) not in self.argcounts:
            print(
                f'Command {self.name} takes '
                f'{",".join(str(c) for c in self.argcounts)} arguments,'
                f' but {len(args)} given')
            return
        else:
            try:
                self.func(*args)
            except Exception as e:
                print(f'Exception occured while executing command: {e}')
                print('Wrong syntax?')
    
    def help(self):
        print(f'Help on command {self.name}:\n{self.helpstr}')
    
    def __call__(self, func):
        self.func = func
        self.add_command(self)
