import PIL.ImageGrab
import os
import json
import time
from wechat_ocr.ocr_manager import OcrManager, OCR_MAX_TASK_ID
import pyperclip
import win32api
import win32con

from updata_path import update_path
# 实现保存剪切板图片
def save_clipboard_pic(save_path):
    try:
        img = PIL.ImageGrab.grabclipboard()
        img.save(save_path)
        print("剪切板中的图片已经保存")
        return True
    except AttributeError:
        print("剪切板中不是图片")
        return False


def ocr_result_callback(img_path: str, results: dict):
    result_file = os.path.join("json", os.path.basename(img_path) + ".json")  # json\01.png.json，这里是包含文件夹名称
    print(f"识别成功，img_path: {img_path}, result_file: {result_file}")
    with open(result_file, 'w', encoding='utf-8') as f:
        f.write(json.dumps(results, ensure_ascii=False, indent=2))

# 编写具体代码时，这个函数需要看情况封装
def save_to_json(img_file):
    # print(111)
    ocr_manager = OcrManager(wechat_dir)
    # 设置WeChatOcr目录
    ocr_manager.SetExePath(wechat_ocr_dir)
    # 设置微信所在路径
    ocr_manager.SetUsrLibDir(wechat_dir)
    # 设置ocr识别结果的回调函数
    ocr_manager.SetOcrResultCallback(ocr_result_callback)
    # 启动ocr服务
    ocr_manager.StartWeChatOCR()
    # TODO 识别图片
    ocr_manager.DoOCRTask(img_file)
    print("图片已经识别，保存在json文件中")
    time.sleep(1)
    while ocr_manager.m_task_id.qsize() != OCR_MAX_TASK_ID:
        pass
    # 识别输出结果
    ocr_manager.KillWeChatOCR()

def save_text(json_file, save_file, mode=1):
    # 打开 JSON 文件
    with open(json_file, 'r', encoding='utf-8') as file:
        # 从文件中加载 JSON 数据
        data = json.load(file)
    print("--------------识别内容----------------")
    # 换行保存
    if mode == 1:
        with open(save_file, 'w', encoding='utf-8') as f:
            # 提取每个对象的 text 字段
            for item in data['ocrResult']:
                print(item['text'])
                f.write(item['text'] + '\n')
    # 不换行保存
    if mode == 2:
        with open(save_file, 'w', encoding='utf-8') as f:
            # 提取每个对象的 text 字段
            for item in data['ocrResult']:
                print(item['text'])
                f.write(item['text'])
    print("------------------------------------")

def txt_copy(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        # 读取文件内容
        file_content = file.read()
    # 将文件内容复制到剪贴板
    pyperclip.copy(file_content)
    print("已将文件内容复制到剪贴板。")

## 读取path.txt中你放的文件路径
def read_path(file, line=1):
    with open(file, 'r') as file:
        lines = file.readlines()
        select_line = lines[line-1]
        # 添加 r 前缀
        select_line = r"{}".format(select_line.strip())
        # print(select_line)
        return select_line

if __name__ == '__main__':
    # TODO:创建对应文件夹
    if not os.path.exists("img"):   # 自动创建img文件夹，其中存放剪切板的图片
        os.makedirs("img")
    if not os.path.exists("json"):  # 自动创建json文件夹，其中存放剪切板的图片文字识别后的json文件
        os.makedirs("json")
    path = "path.txt"
    if not os.path.exists(path):
        with open(path, 'w'):
            pass
    # TODO:更新path.txt第二行内容
    update_path()
    # TODO：读取文件路径
    wechat_ocr_dir = read_path(path, line=1)
    wechat_dir = read_path(path, line=2)
    # TODO:配置并启动OCR服务
    ocr_manager = OcrManager(wechat_dir)
    # 设置WeChatOcr目录
    ocr_manager.SetExePath(wechat_ocr_dir)
    # 设置微信所在路径
    ocr_manager.SetUsrLibDir(wechat_dir)
    # 设置ocr识别结果的回调函数
    ocr_manager.SetOcrResultCallback(ocr_result_callback)
    # 启动ocr服务
    ocr_manager.StartWeChatOCR()

    # print("\033[31m本软件来自公众号：认知up吧。\033[0m", "\033[34m软件免费，请勿上当\033[0m")
    print("本软件来自公众号：认知up吧。\n软件免费，请勿上当\n")

    # 监视Ctrl+C 和 Esc 键
    ctrl_c_pressed = False
    esc_pressed = False

    try:
        print("按下 Ctrl+C 实现微信OCR识别图片并复制到剪切板")
        print("按下 Esc 退出程序")
        while not esc_pressed:
            # 获取键盘状态，检查 Ctrl+C 和 Esc 键是否被按下
            if win32api.GetAsyncKeyState(ord('C')) and win32api.GetAsyncKeyState(win32con.VK_CONTROL):
                ctrl_c_pressed = True
                print("Ctrl+C 被按下")
                img_file = r"img\~~~ocr.png"
                result = save_clipboard_pic(img_file)
                if result:  # True表示剪切板图片已经保存，False表示剪切板根本不是图片
                    file_name = os.path.basename(img_file)  # 使用 os.path.basename() 函数获取文件名
                    json_file = os.path.join("json", file_name + ".json")  # 通过上述操作将01.png变成json\01.png.json
                    save_file = "text_save.txt"
                    # save_to_json(img_file)
                    # TODO 识别图片
                    ocr_manager.DoOCRTask(img_file)
                    print("图片已经识别，保存在json文件中")
                    time.sleep(1)
                    while ocr_manager.m_task_id.qsize() != OCR_MAX_TASK_ID:
                        pass
                    # TODO 你可以将mode改成2，实现文字放在同一行。
                    save_text(json_file, save_file, mode=1)
                    txt_copy(save_file)  # 文本复制到剪切板
                # else:
                #     print("剪切板中不包含有效图片")
                #     pass

            # 检查 Esc 键是否被按下
            if win32api.GetAsyncKeyState(win32con.VK_ESCAPE):
                esc_pressed = True
                # 关闭微信OCR
                ocr_manager.KillWeChatOCR()
                print("Esc 键被按下，准备退出...")
            time.sleep(0.1)  # 在此处可以执行其他任务
    except KeyboardInterrupt:
        print("手动中断")
    print("程序结束")

