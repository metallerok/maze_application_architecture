from typing import Dict, Optional
from abc import ABC, abstractmethod
from enum import Enum
from copy import deepcopy


class Direction(Enum):
    North: 1
    South: 2
    East: 3
    West: 4


class MapSite(ABC):

    @abstractmethod
    def enter(self) -> None:
        pass


class Room(MapSite):

    _room_number = None
    _sides: Dict[MapSite]

    def __init__(self, room_no: int):
        self._room_number = room_no

    def get_side(self, drn: Direction) -> MapSite:
        pass

    def set_side(self, drn: Direction, mps: MapSite) -> None:
        pass

    def enter(self) -> None:
        pass

    def clone(self):
        return deepcopy(self)

    def initialize(self, n):
        self._room_number = n


class EnchantedRoom(Room):
    def __init__(self, room_no: int, locked: bool):
        self._locked = locked
        super().__init__(room_no)


class RoomWithBomb(Room):
    have_bomb = False
    is_destroyed = False


class Wall(MapSite):
    
    def enter(self) -> None:
        pass

    def clone(self):
        return deepcopy(self)


class BombedWall(Wall):
    is_destroyed: bool = False


class Door(MapSite):

    is_open: bool = False

    def __init__(self, r1: Room, r2: Room):
        self._room1 = r1
        self._room2 = r2

    def other_side_from(self, r: Room) -> Room:
        pass

    def enter(self) -> None:
        pass

    def clone(self):
        return deepcopy(self)

    def initialize(self, r1, r2):
        self._room1 = r1
        self._room2 = r2


class Maze:
    
    def add_room(self, r: Room):
        pass

    def room_no(self, no: int) -> Room:
        """
        Get room by number
        """
        pass

    def clone(self):
        return deepcopy(self)


class MazeFactory:

    @classmethod
    def make_maze(cls) -> Maze:
        return Maze()

    @classmethod
    def make_wall(cls) -> Wall:
        return Wall()

    @classmethod
    def make_room(cls, n: int) -> Room:
        return Room(n)

    @classmethod
    def make_door(cls, r1: Room, r2: Room) -> Door:
        return Door(r1, r2)


class EnchantedMazeFactory(MazeFactory):

    @classmethod
    def make_room(cls, n: int) -> Room:
        return EnchantedRoom(n, cls._cast_spell())

    @classmethod
    def _cast_spell(cls) -> bool:
        pass


class BombedMazeFactory(MazeFactory):

    @classmethod 
    def make_wall(cls) -> Wall:
        return BombedWall()

    @classmethod
    def make_room(cls, n: int) -> Room:
        return RoomWithBomb(n)


class MazePrototypeFactory(MazeFactory):
    def __init__(self, m: Maze, w: Wall, r: Room, d: Door):
        self._prototype_maze = m
        self._prototype_wall = w
        self._prototype_room = r
        self._prototype_door = d

    def make_maze(self):
        self._prototype_maze.clone()

    def make_room(self, n):
        room = self._prototype_room.clone()
        room.initialize(n)
        return room

    def make_door(self, r1, r2):
        door = self._prototype_door.clone()
        door.initialize(r1, r2)
        return door

    def make_wall(self):
        return self._prototype_wall.clone()


class MazeBuilder:
    def build_maze(self):
        pass

    def build_room(self, n: int):
        pass

    def build_door(self, room_from: int, room_to: int):
        pass

    def get_maze(self) -> Maze:
        pass


class StdMazeBuilder(MazeBuilder):
    def __init__(self):
        self._current_maze: Optional[Maze] = None

    def _common_wall(self, r1, r2) -> Direction:
        pass

    def build_maze(self):
        self._current_maze = Maze()

    def get_maze(self) -> Maze:
        return self._current_maze

    def build_room(self, n: int):
        if self._current_maze.room_no(n) is None:
            room: Room = Room(n)

            self._current_maze.add_room(room)

            room.set_side(Direction.North, Wall())
            room.set_side(Direction.East, Wall())
            room.set_side(Direction.South, Wall())
            room.set_side(Direction.West, Wall())

    def build_door(self, room_from: int, room_to: int):
        r1 = self._current_maze.room_no(room_from)
        r2 = self._current_maze.room_no(room_to)

        door: Door = Door(r1, r2)

        r1.set_side(self._common_wall(r1, r2), door)
        r2.set_side(self._common_wall(r2, r2), door)


class MazeGame:

    @staticmethod
    def make_maze() -> Maze:
        return Maze()

    @staticmethod
    def make_room(n: int) -> Room:
        return Room(n)

    @staticmethod
    def make_wall() -> Wall:
        return Wall()

    @staticmethod
    def make_door(r1: Room, r2: Room) -> Door:
        return Door(r1, r2)

    @staticmethod
    def create_maze_by_abstract_factory(factory: MazeFactory) -> Maze:
        maze: Maze = factory.make_maze()
        r1: Room = factory.make_room(1)
        r2: Room = factory.make_room(2)
        door: Door = factory.make_door(r1, r2)

        maze.add_room(r1)
        maze.add_room(r2)

        r1.set_side(Direction.North, factory.make_wall())
        r1.set_side(Direction.East, door)
        r1.set_side(Direction.South, factory.make_wall())
        r1.set_side(Direction.West, factory.make_wall())

        r1.set_side(Direction.North, factory.make_wall())
        r1.set_side(Direction.East, factory.make_wall())
        r1.set_side(Direction.South, factory.make_wall())
        r1.set_side(Direction.West, door)

        return maze

    @staticmethod
    def create_maze_from_builder(builder: MazeBuilder):
        builder.build_maze()

        builder.build_room(1)
        builder.build_room(2)
        builder.build_door(1, 2)

        return builder.get_maze()

    def create_maze_by_fabric_method(self) -> Maze:
        maze = self.make_maze()

        r1 = self.make_room(1)
        r2 = self.make_room(2)

        door = self.make_door(r1, r2)

        maze.add_room(r1)
        maze.add_room(r2)

        r1.set_side(Direction.North, self.make_wall())
        r1.set_side(Direction.East, door)
        r1.set_side(Direction.South, self.make_wall())
        r1.set_side(Direction.West, self.make_wall())

        r1.set_side(Direction.North, self.make_wall())
        r1.set_side(Direction.East, self.make_wall())
        r1.set_side(Direction.South, self.make_wall())
        r1.set_side(Direction.West, door)

        return maze
