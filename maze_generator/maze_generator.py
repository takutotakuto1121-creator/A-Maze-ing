#!/usr/bin/env python3

from abc import ABC, abstractmethod
from pydantic import BaseModel, Field, field_validator, model_validator
import sys
import numpy as np


class Config(BaseModel):
    """
    config.txtを格納するクラス

    各KEYに対するVALUEにそれぞれ条件をつけてvalidationを行う
    """
    WIDTH: int = Field(ge=3)
    HEIGHT: int = Field(ge=3)
    ENTRY: tuple[int, int]
    EXIT: tuple[int, int]
    OUTPUT_FILE: str
    PERFECT: bool = Field(default=False)

    @field_validator("ENTRY", "EXIT", mode="before")
    @classmethod
    def parse_pos(cls, v):
        """
        ENTRY, EXITをタプルに変換

        変換できない形式ならそのまま返す
        """
        if isinstance(v, str):
            x, y = v.split(",")
            return (int(x), int(y))
        return v

    @model_validator(mode='after')
    def check_entry_and_exit(self):
        """
        Entry, Exitの妥当性の検証

        以下のいずれかに該当すればエラーを投げる
        ・Entry, Exitが同じ場所にある
        ・Entry, Exitが迷路の範囲外に存在する
        """
        entry_x, entry_y = self.ENTRY
        exit_x, exit_y = self.EXIT

        if self.ENTRY == self.EXIT:
            raise ValueError("Entry and exit should be different")
        if not (0 <= entry_x < self.WIDTH and 0 <= entry_y < self.HEIGHT):
            raise ValueError("Entry should be inside the maze bounds")
        if not (0 <= exit_x < self.WIDTH and 0 <= exit_y <self.HEIGHT):
            raise ValueError("Exit should be inside the maze bounds")
        return self

class Cell(BaseModel):
    value: int = Field(ge=0, le=15)
    visited: bool = Field(default=False)

class MazeGeneratorBasic(ABC):
    def __init__(self) -> None:
        """
        初期化関数

        ・self._configにconfig.txtを格納
        ・self._posに座標データを入れる。15で初期化(全方面に壁が存在)。
        ・self._rngにrngを代(selfで持っておくことにより再現性が保たれる)
        """
        self._config = self.parse_config()
        self._pos = [
            [Cell(value = 15, visited = False) for _ in range(self._config.HEIGHT)]
            for _ in range(self._config.WIDTH)
        ]
        self._rng = np.random.default_rng(42)
        self._parent = {}

    def parse_config(self) -> Config:
        """
        config.txtのパース

        config.txtを読み取り、Configにして返す
        """
        if len(sys.argv) < 2:
            raise Exception("Usage: python a-maze-ing.py config.txt")
        with open(sys.argv[1]) as f:
            content = f.read()
            pairs_str = content.split("\n")
            pairs_dict = dict(item.split("=", 1) for item in pairs_str if "=" in item)
            config = Config(**pairs_dict)
        return config

    def maze_show(self) -> None:
        """
        迷路の可視化
distance_x = abc(x - nx)
        distance_y = abc(y - ny)
        if distance_x > 1 or distance_y > 1:
            return False
        標準出力に16進数で迷路を表示させる
        """
        for y in range(self._config.HEIGHT):
            for x in range(self._config.WIDTH):
                print(f"{self._pos[x][y].value:x}", end="")
            print()

    def break_wall(self, position: tuple[int, int], cardinal: str) -> None:
        """
        壁を破壊する

        座標,方角を引数に取る
        方角の壁を破壊する
        """
        x, y = position
        if cardinal == "N":
            self._pos[x][y].value -= 8
            self._pos[x][y - 1].value -= 2
        elif cardinal == "E":
            self._pos[x][y].value -= 4
            self._pos[x + 1][y].value -= 1
        elif cardinal == "S":
            self._pos[x][y].value -= 2
            self._pos[x][y + 1].value -= 8
        elif cardinal == "W":
            self._pos[x][y].value -= 1
            self._pos[x - 1][y].value -= 4
        else:
            raise ValueError("break_wall(): cardinal should be N, E, S or W")

    def is_road(self, pos: tuple[int, int], n_pos: tuple[int, int]) -> bool:
        distance = (x - nx)**2 + (y - ny)**2
        if distance != 1:
            return False
        if ny < y and self._pos[x][y] >= 8 and self._pos[nx][ny] in (2, 3, 6, 7, 10, 11, 14, 15):
            return True
        if nx > x and self._pos[x][y] in (4,5,6,712,13,14,15) and self._pos[nx][ny] % 2 == 1:
            return True
        if ny > y and self._pos[x][y] in (2,3,6,7,10,11,14,15) and self._pos[nx][ny] >= 8:
            return True
        if nx < x and self._pos[x][y] % 2 == 1 and self._pos[nx][ny] in (4,5,6,712,13,14,15):
            return True

    def change_to_visited(self, position: tuple[int, int]) -> None:
        """
        座標(x, y)のvisitedをTrueに変更
        """
        x, y = position
        self._pos[x][y].visited = True

    @abstractmethod
    def maze_gen(self):
        ...


if __name__ == "__main__":
    # 実行するときはmaze_gen()メソッドをコメントアウト
    maze_gen = MazeGeneratorBasic()
    print("= 迷路の初期化 =")
    maze_gen.maze_show()
    print("= break_wall()の検証 =")
    maze_gen.break_wall(1, 1, "N")
    maze_gen.break_wall(3, 3, "E")
    maze_gen.break_wall(6, 6, "S")
    maze_gen.break_wall(9, 9, "W")
    maze_gen.maze_show()


# 0  0000
# 1  0001
# 2  0010
# 3  0011
# 4  0100
# 5  0101
# 6  0110
# 7  0111
# 8  0000
# 9  1001
# 10 1010
# 11 1011
# 12 1100
# 13 1101
# 14 1110
# 15 1111


# N: 9-15
# E:
# S: 2,3,6,7,10,11,14,15
# W: 奇数
