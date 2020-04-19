# field.Field
盤面を表すクラス
## Attributes
|name|type|description|
|:-|:-|:-|
|height|int|盤面の高さ|
|width|int|盤面の幅|
|base_point|list[list[int]]|マスの素点を表す二次元配列|
|status|list[list[str]]|マスの状態を表す二次元配列(*、O, X, +, -)|
|team|list[str]|チーム名のリスト(サイズ2)|

## methods
|name|type|description|
|:-|:-|:-|
||||

---

# judge.Judge
審判を表すクラス
## Attributes
|name|type|description|
|:-|:-|:-|
|team|tuple[str, str]|チーム名|

## methods
|name|type|description|
|:-|:-|:-|
|calc_point|dict[str, int]|盤面から得点を計算する|
|fill|None|盤面の指定した頂点を繋ぐ城壁を生成し、内部を領域にする|
|judge_castle|list[list[tuple[int, int]]]|城郭を判定してパス(list[tuple[int, int]])のタプルとして返す|
|judge_zone|list[tuple[int, int]]|全ての点に対して、その点が領域になるかどうかを判定し、更新する|
|update|None|盤面を更新する|


### calc_point
盤面から得点を計算して辞書を返す関数

#### Parameters
|name|type|description|
|:-|:-|:-|
||||

#### Returns
|name|type|description|
|:-|:-|:-|
||dict[str, int]|各チームの得点。`チーム名:得点`の形式で格納される|

---

### build_castle
城郭を建てる

#### Parameters
|name|type|description|
|:-|:-|:-|
|wall|str|城壁を表す文字|
|tops|list[tuple[int, int]]|頂点集合|

#### Returns
|name|type|description|
|:-|:-|:-|
||||

---
### fill
指定した頂点をつなぐように城郭を繋ぎ、内部を陣地にする

#### Parameters
|name|type|description|
|:-|:-|:-|
|wall|str|城壁を表す文字|
|zone|str|領域を表す文字|
|tops|list[tuple[int, int]]|頂点のタプル。前後左右のどれかへの直進だけでたどりつける二点が並んでいないといけない|

#### Returns
|name|type|description|
|:-|:-|:-|
||||

---

### judge_castle
城郭判別

#### Parameters
|name|type|description|
|:-|:-|:-|
||||

#### Returns
|name|type|description|
|:-|:-|:-|
|castles|list[list[tuple[int, int]]]|(城郭を表すタプル(頂点のタプル)のタプル)のタプル|

---

### judge_zone
領域判定

#### Parameters
|name|type|description|
|:-|:-|:-|
|wall|str|城壁を表す文字|

#### Returns
|name|type|description|
|:-|:-|:-|
|zones|list[tuple[int, int]]|領域判定したマス|

---

### update
盤面をアップデートする(領域)

#### Parameters
|name|type|description|
|:-|:-|:-|
||||

#### Returns
|name|type|description|
|:-|:-|:-|
||||

---
