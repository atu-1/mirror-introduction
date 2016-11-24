import bpy
import bmesh
from bpy.props import IntProperty, BoolProperty, PointerProperty
import enum
from mathutils import Vector

bl_info = {
    "name": "サンプル3-2: マウスの右クリックで面を削除する",
    "author": "Nutti",
    "version": (2, 0),
    "blender": (2, 75, 0),
    "location": "3Dビュー > プロパティパネル > 特殊オブジェクト編集モード",
    "description": "オブジェクトの並進移動、拡大・縮小、回転をキーボードから行うアドオン",
    "warning": "",
    "support": "TESTING",
    "wiki_url": "",
    "tracker_url": "",
    "category": "Object"
}


EditType = enum.Enum('EditType', 'NONE TRANSLATE SCALE ROTATE')
EditAxis = enum.Enum('EditAxis', 'NONE X Y Z')
EditOption = enum.Enum('EditOption', 'NONE + -')


# プロパティ
class SOEM_Properties(bpy.types.PropertyGroup):
    is_special_mode = BoolProperty(
        name = "特殊オブジェクト編集モード中",
        description = "特殊オブジェクト編集モード中か？",
        default = False)


# 特殊オブジェクト編集モード時の処理
class SpecialObjectEditMode(bpy.types.Operator):
    bl_idname = "mesh.special_object_edit_mode"
    bl_label = "特殊オブジェクト編集モード"
    bl_description = "特殊オブジェクト編集モードへ移行します"

    # メンバ変数の設定
    def __init__(self):
        self.edit_type = EditType['NONE']
        self.edit_axis = EditAxis['NONE']
        self.edit_opt = EditOption['NONE']

    # 発生したイベントをもとに、次の状態を返却するプライベートなメンバ関数
    # 本来であれば本処理を工夫し、本書のコラムに書いたバグを無くすべきだが、
    # 処理を単純化するためにバグをそのまま残している
    # 引数ev_value：イベントの値
    # 引数on：'PRESS'イベント発生時の状態遷移先
    # 引数off：'PRESS'以外のイベント発生時の状態遷移先
    def __change_state(self, ev_value, on, off):
        if ev_value == 'PRESS':
            return on
        elif ev_value == 'RELEASE':
            return off
        return off

    def modal(self, context, event):
        props = context.scene.soem_props

        # 3Dビューの画面を更新
        if context.area:
            context.area.tag_redraw()

//! [exit_modal_mode]
        # キーボードのQキーが押された場合は、特殊オブジェクト編集モードを終了
        if event.type == 'Q' and event.value == 'PRESS':
            props.is_special_mode = False
            print("サンプル3-2: 通常モードへ移行しました。")
            return {'FINISHED'}
//! [exit_modal_mode]

        # 処理するキーイベントのリスト
        # 要素1：キーの識別子
        # 要素2：状態を格納するメンバ変数名
        # 要素3：'PRESS'イベント発生時の状態遷移先
        # 要素4：'PRESS'以外のイベント発生時の状態遷移先
        ev_key_list = (
            # 編集タイプ（並進移動、拡大・縮小、回転）
            ('T', "edit_type", EditType['TRANSLATE'], EditType['NONE']),
            ('S', "edit_type", EditType['SCALE'], EditType['NONE']),
            ('R', "edit_type", EditType['ROTATE'], EditType['NONE']),
            # 軸（X軸、Y軸、Z軸）
            ('X', "edit_axis", EditAxis['X'], EditAxis['NONE']),
            ('Y', "edit_axis", EditAxis['Y'], EditAxis['NONE']),
            ('Z', "edit_axis", EditAxis['Z'], EditAxis['NONE']),
            # 方向（正方向、負方向）
            ('RIGHT_ARROW', "edit_opt", EditOption['+'], EditOption['NONE']),
            ('LEFT_ARROW', "edit_opt", EditOption['-'], EditOption['NONE'])
        )
        # キーボードのキーイベントが発生しているかを確認し、現在の状態を更新
        for ev_key in ev_key_list:
            if event.type == ev_key[0]:
                # self.__dict__には、クラスのメンバ変数の一覧が、ディクショナリ型
                # （キー：値）＝（メンバ変数名：値）として保存されている
                self.__dict__[ev_key[1]] = self.__change_state(
                    event.value, ev_key[2], ev_key[3])

        # オブジェクト変換処理のための条件が揃っていない時は何もしない
        if self.edit_type == EditType['NONE']:
            return {'RUNNING_MODAL'}
        if self.edit_axis == EditAxis['NONE']:
            return {'RUNNING_MODAL'}
        if self.edit_opt == EditOption['NONE']:
            return {'RUNNING_MODAL'}

        # オブジェクトに変形処理を適用
        # 移動
        if self.edit_type == EditType['TRANSLATE']:
            value = Vector((0.0, 0.0, 0.0))
            for i, axis in enumerate(['X', 'Y', 'Z']):
                if self.edit_axis == EditAxis[axis]:
                    if self.edit_opt == EditOption['+']:
                        value[i] = 1.0
                    elif self.edit_opt == EditOption['-']:
                        value[i] = -1.0
            # bpy.ops.transform.translate()：選択中のオブジェクトを並進移動する
            # 引数value：並進移動量
            bpy.ops.transform.translate(value=value)
        # 拡大・縮小
        if self.edit_type == EditType['SCALE']:
            value = Vector((1.0, 1.0, 1.0))
            for i, axis in enumerate(['X', 'Y', 'Z']):
                if self.edit_axis == EditAxis[axis]:
                    if self.edit_opt == EditOption['+']:
                        value[i] = 1.1
                    elif self.edit_opt == EditOption['-']:
                        value[i] = 0.9
            # bpy.ops.transform.resize()：選択中のオブジェクトを拡大・縮小する
            # 引数value：拡大・縮小量
            bpy.ops.transform.resize(value=value)
        # 回転
        elif self.edit_type == EditType['ROTATE']:
            rot_axis = Vector((0.0, 0.0, 0.0))
            for i, axis in enumerate(['X', 'Y', 'Z']):
                if self.edit_axis == EditAxis[axis]:
                    rot_axis[i] = 1.0
            if self.edit_opt == EditOption['+']:
                value = 0.1
            elif self.edit_opt == EditOption['-']:
                value = -0.1
            # bpy.ops.transform.rotate()：選択中のオブジェクトを回転する
            # 引数value：回転量
            # 引数rot_axis：回転軸
            bpy.ops.transform.rotate(value=value, axis=rot_axis)

        return {'RUNNING_MODAL'}

    def invoke(self, context, event):
        props = context.scene.soem_props
        if context.area.type == 'VIEW_3D':
            # 処理開始
            if props.is_special_mode is False:
                props.is_special_mode = True
                # modal処理クラスを追加
                context.window_manager.modal_handler_add(self)
                print("サンプル3-2: 特殊オブジェクト編集モードへ移行しました。")
                return {'RUNNING_MODAL'}
            # 処理停止
            else:
                props.is_special_mode = False
                print("サンプル3-2: 通常モードへ移行しました。")
                return {'FINISHED'}
        else:
            return {'CANCELLED'}


# UI
class OBJECT_PT_SOEM(bpy.types.Panel):
    bl_label = "特殊オブジェクト編集モード"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"

    def draw(self, context):
        sc = context.scene
        layout = self.layout
        props = context.scene.soem_props
        # 開始/停止ボタンを追加
        if props.is_special_mode is False:
            layout.operator(SpecialObjectEditMode.bl_idname, text="開始", icon="PLAY")
        else:
            layout.operator(SpecialObjectEditMode.bl_idname, text="終了", icon="PAUSE")


def register():
    bpy.utils.register_module(__name__)
    sc = bpy.types.Scene
    sc.soem_props = PointerProperty(
        name = "プロパティ",
        description = "本アドオンで利用するプロパティ一覧",
        type = SOEM_Properties)
    print("サンプル3-2: アドオン「サンプル3-2」が有効化されました。")


def unregister():
    del bpy.types.Scene.soem_props
    bpy.utils.unregister_module(__name__)
    print("サンプル3-2: アドオン「サンプル3-2」が無効化されました。")


if __name__ == "__main__":
    register()