<div id="sect_title_img_3_1"></div>

<div id="sect_title_text"></div>

# マウスクリックのイベントを扱う

<div id="preface"></div>

###### Blenderでは3DビューエリアのオブジェクトモードでSキーを押した時に、マウスの移動でオブジェクトのサイズを変更する機能があります。オブジェクトのサイズを入力して変更するよりも、マウスの移動に応じてオブジェクトのサイズを変更できるのは直感的で使いやすいですよね。このように、インタラクティブ性の高い機能をアドオンで提供するためにはどのようにしたらよいのでしょうか？<br>本節ではアドオンからマウスのイベントを扱う方法を紹介します。

## 作成するアドオンの仕様

* *編集モード* 時に、*3Dビュー* エリア上でマウスを右クリックした時に、マウスカーソルの位置にあるオブジェクトの面を削除する
* プロパティパネル（*3Dビュー* エリア上でNキーを押した時に右側に表示されるパネル）から、上記処理を開始または終了を切り替えるボタンを配置する

## アドオンを作成する

[1-5節](../chapter_01/05_Install_own_Add-on.md) を参考にして、以下のソースコードをテキスト・エディタに入力し、ファイル名 ```sample_3_1.py``` として保存してください。

[import](../../sample/src/chapter_03/sample_3_1.py)

## アドオンを使用する

### アドオンを有効化する

[1-5節](../chapter_01/05_Install_own_Add-on.md) を参考に作成したアドオンを有効化すると、コンソールウィンドウに以下の文字列が出力されます。

```sh
サンプル3-1: アドオン「サンプル3-1」が有効化されました。
```

<div id="sidebyside"></div>

|*3Dビュー* エリア上で *N* キーを押してプロパティパネルを表示し、*マウスの右クリックで面を削除* の項目が作成されていることを確認します。|![マウスの右クリックで面を削除 手順1](https://dl.dropboxusercontent.com/s/6pyxmbf4mak9o8j/use_add-on_1.png "マウスの右クリックで面を削除 手順1")|
|---|---|


### アドオンの機能を使用する

有効化したアドオンの機能を使い、動作を確認します。

<div id="process_title"></div>

##### Work

<div id="process_noimg"></div>

|<div id="box">1</div>|*3Dビュー* エリア上で *編集モード* に変更し、選択方法を面選択にします。|
|---|---|

<div id="process_sep"></div>

---

<div id="process"></div>

|<div id="box">2</div>|*3Dビュー* エリアのプロパティパネルから、*マウスの右クリックで面を削除* の項目の *開始* ボタンをクリックします。|![マウスの右クリックで面を削除 手順2](https://dl.dropboxusercontent.com/s/ltuh1pmujq0hbrf/use_add-on_2.png "マウスの右クリックで面を削除 手順2")|
|---|---|---|

<div id="process_sep"></div>

---

<div id="process"></div>

|<div id="box">3</div>|選択中のオブジェクトの任意の面にマウスカーソルを当てて *右クリック* すると、マウスカーソルを当てている面が削除されます。|![マウスの右クリックで面を削除 手順3](https://dl.dropboxusercontent.com/s/1ntqeqbtx5ni0ym/use_add-on_3.png "マウスの右クリックで面を削除 手順3")|
|---|---|---|

<div id="process_sep"></div>

---

<div id="process"></div>

|<div id="box">4</div>|*3Dビュー* エリアのプロパティパネルから、*マウスのクリックで面を削除* 項目の *終了* ボタンをクリックして、処理を終了します。<br>終了時に削除した面の数がスクリプト実行ログに表示されます。|![マウスの右クリックで面を削除 手順4](https://dl.dropboxusercontent.com/s/vz6982lhm4ofsyp/use_add-on_4.png "マウスの右クリックで面を削除 手順4")|
|---|---|---|

<div id="process_start_end"></div>

---


### アドオンを無効化する

[1-5節](../chapter_01/05_Install_own_Add-on.md)を参考に有効化したアドオンを無効化すると、コンソールウィンドウに以下の文字列が出力されます。

```sh
サンプル3-1: アドオン「サンプル3-1」が無効化されました。
```

## ソースコードの解説

本節で紹介したアドオンのソースコードについて解説します。本節で紹介したアドオンのソースコードに関して、ポイントとなる点は以下のとおりです。

* アドオンで共通利用するプロパティ定義
* アドオンの機能を利用するためのUI作成
* オペレータクラスの作成

### アドオン内で利用するプロパティ定義

本節のサンプルでは、オペレータクラス ```DeleteFaceByRClick``` と パネルクラス ```OBJECT_PT_DFRC``` が定義されていて、これら2つのクラス間でデータを共有する必要があります。本節のサンプルでは、アドオン内で共有するデータ全てを ```bpy.types.PropertyGroup``` クラスを継承したクラスのクラス変数に追加し、複数のクラス間でデータを共有します。

```bpy.types.PropertyGroup``` クラスは、[2-3節](../chapter_02/03_Use_Property_on_Tool_Shelf_1.md) で紹介したプロパティクラスをグループ化するためのクラスです。```bpy.types.PropertyGroup``` クラスを継承し、グループ化したいプロパティクラスをクラス変数に追加して使用します。

[import:"define_properties", unindent:"true"](../../sample_raw/src/chapter_03/sample_3_1.py)

本節のサンプルにおいてグループ化したプロパティ一覧を以下に示します。

|プロパティ|意味|
|---|---|
|```running```|値が ```True``` の時にマウスを右クリックすると、マウスカーソルの位置にある面を削除する|
|```right_mouse_down```|値が ```True``` の時は、マウスの右クリック中であることを示す。マウスを右クリックし続けた状態でマウスカーソルを移動した時に、他の面が削除できてしまう問題を解消するために使用する（後述）|
|```deleted```|値が ```True``` の時は、右クリックにより面が削除された状態であることを示す。マウスを右クリックし続けた状態でマウスカーソルを移動した時に、他の面が削除できてしまう問題を解消するために使用する（後述）|
|```deleted_count```|```running``` の値が ```True``` から ```False``` になるまでに削除された面の数|

作成したプロパティグループ ```DFRC_Properties``` は、```register()``` 関数の処理内で ```PointerProperty``` クラスを利用して登録します。

[import:"register_properties", unindent:"true"](../../sample_raw/src/chapter_03/sample_3_1.py)

アドオン有効時に、```PointerProperty``` の引数 ```type``` にプロパティをグループ化したクラス ```DFRC_Properties``` を指定してインスタンスを生成し、```bpy.types.Scene.dfrc_props``` 変数に代入します。以降、各プロパティには ```bpy.types.Scene``` からアクセスすることができます。例えば、プロパティ ```running``` の場合は、```bpy.types.Scene.dfrc_props.running``` でアクセスすることができます。

アドオン無効時には、以下のようにして追加したプロパティのグループを削除します。

[import:"unregister_properties", unindent:"true"](../../sample_raw/src/chapter_03/sample_3_1.py)


### UIを作成する

[2-7節](../chapter_02/07_Divide_Add-on_Source_into_Multiple_Files.md)までのサンプルでは、アドオンの機能を実行するためのUIをメニューに追加するだけでしたが、本節のサンプルのように処理の開始と終了という排他的な項目をメニューに両方追加するのはUIとして良いとは言えません。そこで本節のサンプルでは、[2-9節](../chapter_02/09_Control_Blender_UI_2.md)で紹介した方法を使って、3Dビューエリアのプロパティパネルにオペレータクラス ```DeleteFaceByRClick``` の処理を開始または終了するためのボタンを作成します。

プロパティパネルにボタンを追加するためには、[2-8節](../chapter_02/08_Control_Blender_UI_1.md)で説明したツールシェルフのタブに追加した方法と同様にして ```bpy.types.Panel``` クラスを継承してパネルクラスを作成し、```draw()``` メソッド内でUIを定義します。

本節のサンプルでは次のようなクラス変数を追加しています。パネルクラスの各クラス変数にの意味は、[2-8節](../chapter_02/08_Control_Blender_UI_1.md)を参照してください。

[import:"define_panel_class", unindent:"true"](../../sample_raw/src/chapter_03/sample_3_1.py)

続いて、UIの配置を定義する ```draw()``` メソッドを作成します。

[import:"define_draw_method", unindent:"true"](../../sample_raw/src/chapter_03/sample_3_1.py)


```draw()``` メソッドに渡されてくる引数 ```context``` には、 ```draw()``` メソッドが呼ばれた時のコンテキスト情報が含まれています。特に、```context.scene``` は ```bpy.types.Scene``` と同一であり、```context.scene.dfrc_props``` から、```register()``` 関数内で ```bpy.types.Scene.dfrc_props``` に登録したアドオン内のプロパティグループ ```DFRC_Properties``` を参照することができます。

直後の条件分岐では、面の削除処理の状態を確認した上で ```DeleteFaceByRClick``` の処理開始と処理終了のボタンを切り替えます。```DFRC_Properties``` クラスのクラス変数 ```running``` が ```False``` の時は削除処理が開始されていないため、開始ボタンを表示します。```running``` が ```True``` の時は、削除処理がすでに開始されている状態であるため、終了ボタンを表示します。


### オペレータクラスの作成

最後に、オペレータクラス ```DeleteFaceByRClick``` を作成します。

本節のアドオンのオペレータクラスでは、これまで紹介していたほとんどのオペレータクラスで毎回定義していた ```execute()``` メソッドが定義されていません。その代わり、```modal()``` メソッドと ```invoke()``` メソッドが定義されています。それぞれのメソッドについて説明します。

#### invoke()メソッド

本節のサンプルでは、ボタンが押した時に処理を開始/終了する処理を ```invoke()``` メソッドに記述します。

プロパティグループ ```DFRC_Properties``` を ```invoke()``` メソッドの引数 ```context``` から取得する方法は、UIの作成で説明した方法と同様に、```context.scene.dfrc_props``` で取得することができます。

[import:"press_start_button", unindent:"true"](../../sample_raw/src/chapter_03/sample_3_1.py)

面の削除処理中は、変数 ```props.running``` の値が ```True``` に設定されていなければならないため、変数 ```props.running``` を ```True``` に設定した後、```DFRC_Properties``` の各クラス変数を初期値に設定します。最後に ```context.window_manager.modal_handler_add()``` 関数を実行してモーダルクラスを登録し、```{'RUNNING_MODAL'}``` を返してモーダルモードへ移行します。

モーダルモードとは、マウスやキーボードなどからイベントを受け取り続けるモードのことを指します。
モーダルモード時は、```context.window_manager.modal_handler_add()``` 関数に指定したクラスの ```modal()``` メソッドが継続的に呼び出され、```{'FINISHED'}``` または ```{'CANCELLED'}``` を返すまで ```modal()``` メソッドの呼び出しが続きます。

本節のアドオンでは、 ```invoke()``` メソッドと ```modal()``` メソッドを同一のクラスで定義しているため、 ```context.window_manager.modal_handler_add()``` 関数の引数に自身のインスタンスである ```self``` を指定します。

[import:"press_stop_button", unindent:"true"](../../sample_raw/src/chapter_03/sample_3_1.py)

面の削除処理中でない場合は、変数 ```props.running``` の値が ```False``` に設定されていなければなりません。このため、面の削除処理中に *マウスの右クリックで面を削除* ボタンが押された時、すなわち ```invoke()``` メソッドが実行され ```props.running``` が ```True``` の時には、変数 ```props.running``` を ```False``` に設定後、面の削除処理中に削除した面の数を出力します。

最後に ```invoke()``` メソッドは、 ```{'FINISHED'}``` を返して処理を終えます。

<div id="space_l"></div>


#### modal()メソッド

続いて、モーダルモード中に呼ばれる ```modal()``` メソッドの処理を追ってみましょう。

[import:"redraw_view3d", unindent:"true"](../../sample_raw/src/chapter_03/sample_3_1.py)

```modal()``` メソッドの最初の処理では、```context.area.tag_redraw()``` 関数を実行し、*3Dビュー* エリアを更新しています。```context.area``` には ```modal()``` メソッドが実行されているエリア情報が保存されています。本節のサンプルでは、*マウスの右クリックで面を削除* ボタンを押した時に呼ばれる ```invoke()``` メソッドでモーダルモードに移行するため、```context.area``` は *3Dビュー* エリアの情報が保存されています。このため、```context.area.tag_redraw()``` 関数を実行することで、*3Dビュー* エリアを更新することができます。

[import:"exit_modal_mode", unindent:"true"](../../sample_raw/src/chapter_03/sample_3_1.py)

続いて面の削除処理が終了した状態であるか否かを調べ、削除処理が終了していた場合はモーダルモードを終了します。サンプルでは、```props.running``` が ```False``` である場合は面の削除処理が終了したことになるため、```{'FINISHED'}``` を返して ```modal()``` メソッドを終了し、モーダルモードを終了します。


[import:"update_click_status", unindent:"true"](../../sample_raw/src/chapter_03/sample_3_1.py)

次に、```modal()``` メソッドの引数 ```event``` を用いて、マウスのクリックやキーボードのキー入力を取得します。```event.type``` には発生した様々なイベントの種類が保存されています。イベントの一例を次に示します。

|値|値の意味|
|---|---|
|```RIGHTMOUSE```|マウス右ボタン|
|```LEFTMOUSE```|マウス左ボタン|
|```A```|キーボードAキー|
|```B```|キーボードBキー|

また、```event.value``` はイベントの種類に対するイベントの値を示しています。例えば次のような値が ```event.value``` に設定されます。

|値|値の意味|
|---|---|
|```PRESS```|ボタンやキーが押された|
|```RELEASE```|ボタンやキーが離された|

[import:"delete_face", unindent:"true"](../../sample_raw/src/chapter_03/sample_3_1.py)

マウスで右クリックされた時の処理を実装します。削除処理の前に、```if props.right_mouse_down is True and props.deleted is False``` によりキー入力の情報を確認し、削除処理を行うか否かを確認しています。この確認処理には少し工夫を加えていますので、詳しく説明します。

マウスが右クリックされたことを検出するためには、一見すると ```props.right_mouse_down``` が ```True``` であることの判定だけで問題ないように思えます。しかし、右クリックが押されたいる間は ```props.right_mouse_down``` が常に ```True``` になるため、クリックした状態でマウスを移動させると面を削除できてしまいます。これは、本来期待する動作(右クリックを行った直後の1回だけ面を削除)とは異なります。そこで、マウスを右クリックした後に1度面を削除した時に ```Ture``` に設定される変数 ```props.deleted``` が ```True``` である場合は、削除処理を行わないようにします。

[import:"clear_restrict_status", unindent:"true"](../../sample_raw/src/chapter_03/sample_3_1.py)

なお、```props.deleted``` が ```True``` の間は面を削除することができないため、  ```props.right_mouse_down``` が ```False``` に変わった時に ```props.deleted``` を ```False``` に戻すことで、次に右クリックされた時に面を削除できるようにします。

続いて面を削除の処理の説明をします。
面を削除するためには、削除対象のメッシュデータにアクセスする必要があります。

メッシュデータにアクセスするためには、```bpy.data.meshes``` からアクセスする方法と ```bmesh``` モジュールを用いる方法があります。本節のサンプルでは、 ```bmesh``` モジュールを用いて面の削除処理を実装しています。

```bmesh``` は比較的最近（バージョン2.63より）導入されたモジュールで、メッシュデータを簡単に扱う関数が多く提供されています。最近作成されているアドオンでは、```bmesh``` を使っている場合がほとんどですので、基本的に ```bmesh``` を使ってメッシュデータを扱うようにしましょう。```bmesh``` を利用するためには、次のように ```bmesh``` モジュールをインポートする必要があります。

[import:"import_bmesh", unindent:"true"](../../sample_raw/src/chapter_03/sample_3_1.py)

```bmesh``` を使った面の削除処理について説明します。

[import:"build_bmesh", unindent:"true"](../../sample_raw/src/chapter_03/sample_3_1.py)

メッシュデータにアクセスするためには、```bmesh``` 用のメッシュデータを構築する必要があります。```bmesh``` 用のメッシュデータを構築するためには、編集中のオブジェクトデータ ```context.edit_object.data``` を ```bmesh.from_edit_mesh()``` 関数の引数に渡す必要があります。ここで、```context.edit_object``` は編集中のオブジェクト情報を持つ変数で、```data``` 変数によりオブジェクトのデータを取得することができます。勘の良い方であれば気がつかれたと思いますが、```bmesh``` 用のメッシュデータを構築するためには *エディットモード* である必要があります。仮に、*オブジェクトモード* で ```bmesh``` を構築しようとするとエラーが発生して構築することができないため、注意が必要です。

次に、クリックされた面を削除する処理について説明します。クリックされた面の削除処理の流れを次のように3段階で行います。

<div id="custom_ol"></div>

1. クリック時にマウスの位置にある面を選択
2. 選択された面を取得
3. 面を削除

##### 1. クリック時にマウスの位置にある面を選択

[import:"select_clicked_face", unindent:"true"](../../sample_raw/src/chapter_03/sample_3_1.py)

クリック時のマウス位置は、```modal()``` メソッドの引数 ```event``` から取得できます。取得した位置情報は変数 ```loc``` に保存します。

次に面を選択する必要がありますが、面を選択するために ```bpy.ops.view3d.select()``` 関数を利用します。
```bpy.ops.view3d.select()``` 関数の引数 ```location``` にマウスの位置を指定することで、マウスの位置にある面を選択することができます。もしマウスの位置に面がなければ、```bpy.ops.view3d.select()``` 関数は ```{'PASS_THROUGH'}``` を返します。このため、```bpy.ops.view3d.select()``` 関数の戻り値 ```ret``` が ```{'PASS_THROUGH'}``` である場合は、マウスの位置に面がないことをコンソールウィンドウ出力した後に処理を終了します。





##### 2. 選択された面を取得

選択された面は、```bmesh``` の履歴情報のうち最後に選択された面として取得できます。頂点・辺・面の選択履歴 ```bm.select_history``` の最後の要素が面であるか否かを確認し、面であれば処理を継続します。面でなければ ```{'PASS_THROUGH'}``` を返して処理を終了します。

[import:"get_selected_face", unindent:"true"](../../sample_raw/src/chapter_03/sample_3_1.py)

最後に選択した面を削除します。

面の削除は ```bmesh.ops.delete()``` 関数で行い、以下に示す引数を指定します。

|引数|値の意味|
|---|---|
|第1引数|```bmesh``` 用のメッシュデータ|
|```geom```|削除するデータ|
|```context```|削除するデータの種類|

今回は面を削除するため、 ```context``` に ```5``` を指定しています。

[import:"delete_selected_face", unindent:"true"](../../sample_raw/src/chapter_03/sample_3_1.py)

面を削除したことをメッシュに反映させるため、 ```bmesh.update_edit_mesh()``` 関数を実行します。この関数を実行しないとメッシュが更新されませんので、 ```bmesh``` 用のメッシュデータを修正した時は必ず実行するようにしましょう。

[import:"update_bmesh", unindent:"true"](../../sample_raw/src/chapter_03/sample_3_1.py)

面の削除処理の説明はこれで終わりです。

最後に、削除した面数をカウントアップして変数 ```props.deleted``` を ```True``` に変更し、マウスの右ボタンが押された状態で連続して面が削除されないようにします。

[import:"post_process", unindent:"true"](../../sample_raw/src/chapter_03/sample_3_1.py)

最後に、```modal``` メソッドは ```{'PASS_THROUGH'}``` を返します。```{'PASS_THROUGH'}``` が返されるとイベントを本処理に閉じず、別の処理に対しても通知することができます。```{'PASS_THROUGH'}``` が指定されていないと、マウスやキーボードのイベントが発生した時に行う ```DeleteFaceByRClick``` の処理後にイベントが捨てられてしまい、マウスやキーボードからのイベントに対する他の処理が発生しなくなってしまいます。

試しに、 ```modal()``` メソッドの最終行である ```return {'PASS_THROUGH'}``` を ```return {'RUNNING_MODAL'}``` に変更してみましょう。

プロパティパネルからアドオンの機能を実行開始した後はボタンを押すことができなくなり、処理を終えることができなくなります。これは ```DeleteFaceByRClick``` の ```modal()``` メソッドでイベントが捨てられ、他の処理へイベントが通知されていないことを示します。

## まとめ

マウスから発生したイベントを扱う方法を紹介しました。これまでに説明していない内容がたくさん出てきましたが、理解できましたでしょうか？

マウスのイベントを用いることで、 アドオンで実現出来ることが広がると思いますので、ぜひ積極的に活用していきましょう。

<div id="point"></div>

### ポイント

<div id="point_item"></div>

* ```bpy.types.PropertyGroup``` クラスを継承したクラスのクラス変数にプロパティクラスを指定することで、プロパティをグループ化することができる
* プロパティパネルへメニューを追加するためには、 ```bpy.types.Panel``` クラスを継承し、 ```draw()``` メソッド内でUIを定義する必要がある
*  ```invoke()``` メソッドや ```execute()``` メソッドで ```{'RUNNING_MODAL'}``` を返すとモーダルモードへ移行し、登録されたモーダルクラスの ```modal()``` メソッドが実行される
* モーダルモードは、 ```{'FINISHED'}``` または ```{'CANCELLED'}``` を返すまで処理を終えずにイベントを受け取り続けるモードである
* ```modal()``` メソッドで ```{'PASS_THROUGH'}``` を返すことで、他の処理にもイベントを通知できる
* ```invoke()``` メソッドや ```modal()``` メソッドの引数 ```event``` を参照することで、発生したイベントやイベント時の状態を取得できる
* ```bmesh``` モジュールには、メッシュデータを簡単に扱うための関数が多数用意されている
