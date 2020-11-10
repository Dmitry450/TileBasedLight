from chunk import Chunk

from constants import *

from light_solver import LightSolver


def genworld():
    grid = [[0 for i in range(GRID_WIDTH)] for j in range(GRID_HEIGHT)]

    for y, line in enumerate(grid):
        for x, el in enumerate(grid[y]):
            if y >= x*2-20:
                grid[y][x] = 1
    
    return grid


class World:
    CHUNK_WIDTH = 10
    CHUNK_HEIGHT = 7

    instance = None
    
    @classmethod
    def get(cls):
        return cls.instance
    
    @classmethod
    def new(cls):
        cls.instance = World()
        return cls.instance

    def __init__(self):
        self.blocks = genworld()
        
        self.light_solver = LightSolver(self)
        
        self.blocks_data = {}

        chunks_x = GRID_WIDTH // self.CHUNK_WIDTH
        chunks_y = GRID_HEIGHT // self.CHUNK_HEIGHT

        self.chunks = [[Chunk(
            self,
            (x*self.CHUNK_WIDTH, y*self.CHUNK_HEIGHT),
            (self.CHUNK_WIDTH*CELL_WIDTH, self.CHUNK_HEIGHT*CELL_HEIGHT)) for x in range(chunks_x)] for y in range(chunks_y)]

    def update_chunks(self):
        for line in self.chunks:
            for chunk in line:
                chunk.init_light()
                
                chunk.update()

    def add_block(self, blockid,
                  light_dropoff=0.6,
                  color=None,
                  light_source=0):
        self.blocks_data[blockid] = {
            'light_dropoff': light_dropoff,
            'color': color,
            'light_source': light_source,
        }

    def within_bounds(self, x, y):
        return (0 <= x < GRID_WIDTH and 0 <= y < GRID_HEIGHT)
    
    def get_color(self, blockid):
        return self.blocks_data.get(blockid, {}).get('color')
    
    def get_light_source(self, blockid):
        return self.blocks_data.get(blockid, {}).get('light_source')
    
    def get_blockdef(self, blockid):
        return self.blocks_data.get(blockid)

    def get_chunk_position(self, x, y):
        """Chunk position in chunks matrix"""
        return (x // self.CHUNK_WIDTH, y // self.CHUNK_HEIGHT)
    
    def localize_position(self, x, y):
        """Converts global world's position to chunk's local"""
        c_pos = self.get_chunk_position(x, y)
        c_pos = c_pos[0] * self.CHUNK_WIDTH, c_pos[1] * self.CHUNK_HEIGHT

        return x - c_pos[0], y - c_pos[1]

    def get_chunk(self, x, y):
        """Gets chunk at given block position. Returns None if out of bounds"""
        if not self.within_bounds(x, y):
            return

        x //= self.CHUNK_WIDTH
        y //= self.CHUNK_HEIGHT

        return self.chunks[y][x]

    def get_light(self, x, y):
        """Gets light at given position. Returns None if out of bounds"""
        pos = self.localize_position(x, y)  # Local chunk's position
        chunk = self.get_chunk(x, y)  # Chunk or None

        if chunk is not None:
            return chunk.get_light(*pos)

    def set_light(self, x, y, value):
        """Sets light at given position. Does nothing if out of bounds"""
        pos = self.localize_position(x, y)  # Local chunk's position
        chunk = self.get_chunk(x, y)  # Chunk or None

        if chunk is not None:
            chunk.set_light(*pos, value)

    def setblock(self, x, y, block):
        chunk = self.get_chunk(x, y)

        if chunk is not None:
            self.blocks[y][x] = block
            
            light_source = self.get_light_source(self.blocks[y][x])
            
            if light_source != 0:
                self.light(x, y, intensity=light_source)
            else:
                self.unlight(x, y)
            
            chunk.update()
    
    def light(self, x, y, intensity):
        if (self.within_bounds(x, y) and
            intensity >= self.get_light(x, y)):
            self.light_solver.add_light_source(x, y, intensity)

    def unlight(self, x, y):
        if (self.within_bounds(x, y) and
            self.get_light_source(self.get_block(x, y)) == 0):
            self.light_solver.remove_light_source(x, y)

    def get_block(self, x, y):
        if self.within_bounds(x, y):
            return self.blocks[y][x]

    def draw(self, screen):
        for line in self.chunks:
            for chunk in line:
                chunk.draw(screen)
