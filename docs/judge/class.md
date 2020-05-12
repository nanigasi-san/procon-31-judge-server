# TODO: 各メソッドの詳細
# Agent()
エージェントを表すクラス
## Attributes
|name|type|description|
|:-|:-|:-|
|point|Point|現在の座標|
|on_field|bool|配置済みかどうか|
|next_activity|str|次の行動|

## methods
|name|type|description|
|:-|:-|:-|
||||

---

# Point(NamedTuple)
二次元座標を表すクラス
## Attributes
|name|type|description|
|:-|:-|:-|
|x|int|x座標|
|y|int|y座標|

## methods
|add|Point|引数に渡した差分を表すxyのタプルとの和の座標を表すPointを返す|
|gen_all_points|Iterable[Point]|指定された範囲のすべてのPointのIterableを返す(staticmethod)|

### add
引数の差分タプルをたしたPointオブジェクトを返す

#### Parameters
|name|type|description|
|:-|:-|:-|
|diff|Tuple[int, int]|(dx, dy)のタプル|

#### Returns
|name|type|description|
|:-|:-|:-|
||Point|差分を足したPoint|

### gen_all_points
(0, 0)から(height, width)までの全てのPointオブジェクトのイテレータを返す

#### Parameters
|name|type|description|
|:-|:-|:-|
|height|int|求める最大の(二次元配列における)x|
|width|int|求める最大の(二次元配列における)y|

#### Returns
|name|type|description|
|:-|:-|:-|
||Iterable|頂点のIterable|

---

# field.Grid(List[List[T]])
Fieldのマス目を表現し、様々な情報を持つ
## Attributes
|name|type|description|
|:-|:-|:-|
||||
## methods
|name|type|description|
|:-|:-|:-|
|at|T|その座標の値(これはGridによって変わる)を返す|

### at
引数のPointの座標の値を返す

#### Parameters
|name|type|description|
|:-|:-|:-|
|point|Point|アクセスしたい座標の座標|

#### Returns
|name|type|description|
|:-|:-|:-|
||||

---

# field.Field
盤面を表すクラス
## Attributes
|name|type|description|
|:-|:-|:-|
|height|int|盤面の高さ|
|width|int|盤面の幅|
|base_point|Grid|マスの素点を表す二次元配列|
|status|Grid|マスの状態を表す二次元配列(*、O, X, +, -)|

## methods
|name|type|description|
|:-|:-|:-|
||||

---

# judge.Path(List[Point])
Pointの連続で経路を表すクラス
## Attributes
|name|type|description|
|:-|:-|:-|
||||

## methods
|reduction|Path|自身を縮約(x軸またはy軸に平行な直線部分を始点と終点の二点にまとめる)した経路を返す|

### reduction
縮約した経路を返す

#### Parameters
|name|type|description|
|:-|:-|:-|
||||

#### Returns
|name|type|description|
|:-|:-|:-|
|reducted_path|Path||

---

# judge.Judge
審判を表すクラス
## Attributes
|name|type|description|
|:-|:-|:-|
|field|Field|フィールド|
|teams|tuple[str, str]|チーム名|
|agents|dict[str, list[Agent]]|チーム名：エージェントのリストの辞書|
|wall_mark|tuple[str, str]|城壁を表す文字のタプル|
|zone_mark|tuple[str, str]|領域を表す文字のタプル|

## methods
|name|type|description|
|:-|:-|:-|
|calc_point|dict[str, int]|盤面から得点を計算する|
|build_castle|None|指定した頂点を繋ぐように城郭を築く|
|fill|None|盤面の指定した頂点を繋ぐ城壁を生成し、内部を領域にする|
|judge_castle|list[list[tuple[int, int]]]|城郭を判定してパス(list[tuple[int, int]])のタプルとして返す|
|judge_zone|list[tuple[int, int]]|全ての点に対して、その点が領域になるかどうかを判定し、更新する|
|submit_agents_activity|Grid[int]|jsonを基にエージェントの行動を仮置きする(重複などを許さないように調整する)|
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
|team_point|dict[str, int]|各チームの得点。`チーム名:得点`の形式で格納される|


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


### judge_castle
城郭判別

#### Parameters
|name|type|description|
|:-|:-|:-|
||||

#### Returns
|name|type|description|
|:-|:-|:-|
|castles|dict[str, list[list[tuple[int, int]]]]|(城郭を表すタプル(頂点のタプル)のタプル)のタプル|


### judge_zone
領域判定

#### Parameters
|name|type|description|
|:-|:-|:-|
||||

#### Returns
|name|type|description|
|:-|:-|:-|
|zones|dict[str, set[tuple[int, int]]]|領域判定したマス|

### submit_agents_activity
エージェントの行動を仮置きする関数

#### Parameters
|name|type|description|
|:-|:-|:-|
|json_path|str|jsonファイルのパス|

#### Returns
|name|type|description|
|:-|:-|:-|
|temp_grid|Grid||


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
