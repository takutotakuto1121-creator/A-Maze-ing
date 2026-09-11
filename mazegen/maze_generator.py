#!/usr/bin/env python3

from abc import ABC, abstractmethod
from pydantic import BaseModel, Field, field_validator, model_validator
import sys
import numpy as np
import math
import sys

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
    SEED: int = Field(default=42)

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
    is_42: bool = Field(default=False)
    is_min: bool = Field(default=False)

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
        self.make_42_pattern()
        self._rng = np.random.default_rng(self._config.SEED)
        self._parent = {}
        self._bonus = False

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
        x, y = pos
        nx, ny = n_pos
        distance = (x - nx) ** 2 + (y - ny) ** 2
        if distance != 1:
            return False
        # ビット定義: N=8, E=4, S=2, W=1
        if ny < y and (self._pos[x][y].value & 8) == 0 and (self._pos[nx][ny].value & 2) == 0:
            return True
        if nx > x and (self._pos[x][y].value & 4) == 0 and (self._pos[nx][ny].value & 1) == 0:
            return True
        if ny > y and (self._pos[x][y].value & 2) == 0 and (self._pos[nx][ny].value & 8) == 0:
            return True
        if nx < x and (self._pos[x][y].value & 1) == 0 and (self._pos[nx][ny].value & 4) == 0:
            return True
        return False

    def change_to_visited(self, position: tuple[int, int]) -> None:
        """
        座標(x, y)のvisitedをTrueに変更
        """
        x, y = position
        self._pos[x][y].visited = True

    def make_42_pattern(self) -> None:
        if self._config.WIDTH < 9 or self._config.HEIGHT < 7:
            return
        if self._config.WIDTH % 2 == 0:
            self.make_42_pattern_even()
        if self._config.WIDTH % 2 == 1:
            self.make_42_pattern_odd()

    def make_42_pattern_even(self) -> None:
        """
        """
        pattern_42 = [
            [True, False, False, False, False, True, True, True],
            [True, False, False, False, False, False, False, True],
            [True, True, True, False, False, True, True, True],
            [False, False, True, False, False, True, False, False],
            [False, False, True, False, False, True, True, True]
        ]
        width_42 = 8
        height_42 = 5
        width_start = (self._config.WIDTH - 8) // 2
        height_start = (self._config.HEIGHT - 5) // 2
        for x, nx in enumerate(range(width_start, width_start + width_42)):
            for y, ny in enumerate(range(height_start, height_start + height_42)):
                self._pos[nx][ny].visited = pattern_42[y][x]
                self._pos[nx][ny].is_42 = pattern_42[y][x]

    def make_42_pattern_odd(self) -> None:
        pattern_42 = [
            [True, False, False, False, True, True, True],
            [True, False, False, False, False, False, True],
            [True, True, True, False, True, True, True],
            [False, False, True, False, True, False, False],
            [False, False, True, False, True, True, True]
        ]
        width_42 = 7
        height_42 = 5
        width_start = (self._config.WIDTH - 7) // 2
        height_start = (self._config.HEIGHT - 5) // 2
        for x, nx in enumerate(range(width_start, width_start + width_42)):
            for y, ny in enumerate(range(height_start, height_start + height_42)):
                self._pos[nx][ny].visited = pattern_42[y][x]
                self._pos[nx][ny].is_42 = pattern_42[y][x]

    def make_non_complete_maze(self) -> None:
        if len(sys.argv) == 4 and sys.argv[2] == "--max-dead-ends":
            max_dead_end = int(sys.argv[3])
            keep_dead_end = self.pick_dead_end_to_keep(max_dead_end)
        else:
            keep_dead_end = []
        changed = True
        while changed:
            changed = False
            for x in range(self._config.WIDTH):
                for y in range(self._config.HEIGHT):
                    if (x, y) in keep_dead_end:
                        continue
                    if self.break_dead_end(x, y):
                        changed = True

    def break_dead_end(self, x: int, y: int) -> bool:
        if self._pos[x][y].is_42:
            return False

        value = self._pos[x][y].value
        open_count = 4 - bin(value).count("1")
        if open_count != 1:
            return False

        cardinals = []
        if y > 0 and value & 8 == 8 and self._pos[x][y - 1].is_42 is False:
            cardinals.append("N")
        if x < self._config.WIDTH - 1 and value & 4 == 4 and self._pos[x + 1][y].is_42 is False:
            cardinals.append("E")
        if y < self._config.HEIGHT - 1 and value & 2 == 2 and self._pos[x][y + 1].is_42 is False:
            cardinals.append("S")
        if x > 0 and value & 1 == 1 and self._pos[x - 1][y].is_42 is False:
            cardinals.append("W")

        if not cardinals:
            return False

        cardinal = self._rng.choice(cardinals)
        self.break_wall((x, y), cardinal)
        return True


    def pick_dead_end_to_keep(self, max_dead_end: int) -> list[tuple[int, int]] | None:
        if max_dead_end <= 0:
            return []

        candidates = []
        for x in range(self._config.WIDTH):
            for y in range(self._config.HEIGHT):
                if self._pos[x][y].is_42:
                    continue
                open_count = 4 - bin(self._pos[x][y].value).count("1")
                if open_count == 1:
                    candidates.append((x, y))
        if not candidates:
            return []

        pick_count = min(len(candidates), max_dead_end)

        index = self._rng.choice(len(candidates), size=pick_count, replace=False)
        return [candidates[i] for i in index]

    def check_big_space(self) -> bool:
        for x in range(self._config.WIDTH):
            for y in range(self._config.HEIGHT):
                if (
                    0 < x < self._config.WIDTH - 1 and 0 < y < self._config.HEIGHT - 1 and
                    self._pos[x][y] == 0 and
                    self._pos[x + 1][y - 1] & 2 == 0 and self._pos[x + 1][y - 1] & 1 == 0 and
                    self._pos[x - 1][y - 1] & 4 == 0 and self._pos[x - 1][y - 1] & 2 == 0 and
                    self._pos[x - 1][y + 1] & 8 == 0 and self._pos[x + 1][y + 1] & 4 == 0 and
                    self._pos[x + 1][y + 1] & 8 == 0 and self._pos[x + 1][y + 1] & 1 == 0
                    ):
                    return True
        return False

    def remake_maze(self) -> None:
        self._config.SEED += 1
        self.maze_gen()

    # def space_check(x: int, y: int, cardinal: list[str]) -> bool:
    #     #dead_endが橋の場合は3*3になり得るためそのチェック
    #     if cardinal == "N":
    #         if (
    #             self._pos[x][y] & 4 == 0 and
    #             self._pos[x + 1][y - 1] == 0 and
    #             self._pos[x + 2][y] & 8 == 0 and self._pos[x + 2][y - 2] & 1 == 0 and
    #             self._pos[x + 2][y - 2] & 2 == 0 and self._pos[x + 2][y - 2] & 1 == 0 and
    #             self._pos[x][y - 2] & 4 == 0 and self._pos[x][y - 2] & 2 == 0
    #         ):
    #             return

    def output_to_file(self) -> None:
        with open(self._config.OUTPUT_FILE, "w") as f:
            for y in range(self._config.HEIGHT):
                for x in range(self._config.WIDTH):
                    f.write(f"{self._pos[x][y].value:x}")
                f.write("\n")

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


# 完全迷路->不完全迷路
# 完全迷路->任意の２点間の距離は１通り
# 不完全迷路->任意の２点間の距離は少なくとも1通り + ４隅とセンターはオープン + (推奨)no_dead_end

# dead_endを見つける→破壊して3*3にならなければ破壊
