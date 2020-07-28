import json
from consts import GenType, TILE_SIZE, TileType
from tile import Tile

with open('src/data/data.json', 'r') as file:
    data = json.load(file)
map = []
genType = GenType.SQUAREGRID

def gen_grid(levelNo=0):
    if genType == GenType.SQUAREGRID:
        if levelNo == 0:
            for y, column in enumerate(data['staticLevel']):
                map.append([])
                for x, value in enumerate(column):
                    if value == '.':
                        map[y].append(Tile(x, y, x * TILE_SIZE, y * TILE_SIZE, TileType.TILE_BLANK))
                    elif value == '0':
                        map[y].append(Tile(x, y, x * TILE_SIZE, y * TILE_SIZE, TileType.TILE_DBL_WALL))
                    elif value == '1':
                        map[y].append(Tile(x, y, x * TILE_SIZE, y * TILE_SIZE, TileType.TILE_WALL))
                    elif value == '2':
                        map[y].append(Tile(x, y, x * TILE_SIZE, y * TILE_SIZE, TileType.TILE_CORNER))
                    elif value == '-':
                        map[y].append(Tile(x, y, x * TILE_SIZE, y * TILE_SIZE, TileType.TILE_FRUIT))
                    elif value == '*':
                        map[y].append(Tile(x, y, x * TILE_SIZE, y * TILE_SIZE, TileType.TILE_ENERGIZER))

def correct_walls():



gen_grid()
print(*map, sep='\n')
