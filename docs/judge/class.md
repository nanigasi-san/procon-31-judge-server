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
|calc_point|dict[str, int]|盤面から得点を計算する|

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

### fill
指定した頂点をつなぐように城郭を繋ぎ、内部を陣地にする

#### Parameters
|name|type|description|
|:-|:-|:-|
|marker|tuple[str]|城壁と陣地を表す文字|
|tops|tuple[tuple[int]]|頂点のタプル。前後左右のどれかへの直進だけでたどりつける二点が並んでいないといけない|

#### Returns
|name|type|description|
|:-|:-|:-|
||||

---
---