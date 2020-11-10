class DynamicLight:
    """
    Light which can be connected to something
    """
    
    def __init__(self, world, getposf, update_time=0.1):
        self.world = world
        
        self.getposf = getposf
        
        self.pos = None

        self.update_time = update_time
        self.timer = 0

    def update(self, dtime):
        self.timer += dtime

        if self.timer > self.update_time:
            self.timer = 0

            newpos = self.getposf()

            if newpos != self.pos:

                if self.pos is not None:
                    self.world.unlight(*self.pos)
                
                self.world.light(*newpos, 180)

                self.pos = newpos

    def clear(self):
        self.world.unlight(*self.pos)
