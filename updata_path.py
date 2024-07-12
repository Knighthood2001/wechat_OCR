import os
import re
from pathlib import Path

def get_updata_path(initial_path):
    if not os.path.exists(initial_path):
        print("微信已经更新，正在为您更换路径...")
        parent_directory = Path(initial_path).parent  # 获取上一级目录"G:/applicationsoftware/WeChat"

        for item in os.listdir(parent_directory):
            # 定义正则表达式模式
            pattern = r'^\[(.*)\]$'
            # 使用 re.match 进行匹配
            match = re.match(pattern, item)
            # 判断是否匹配成功
            if match:
                # 拼接完整路径
                item_path = os.path.join(parent_directory, item)
                print(item_path)
                return item_path
    else:
        return None

def update_path():
    # 打开文件并读取第二行内容
    with open('path.txt', 'r') as file:
        lines = file.readlines()
        if len(lines) == 2:
            second_line = lines[1].strip()  # 获取第二行并去除首尾空白符
            content = get_updata_path(second_line)
            if content:
                lines[1] = content + '\n'  # 注意要添加换行符
                # 将修改后的内容写回文件
                with open("path.txt", 'w') as file:
                    file.writelines(lines)
            else:
                return None

if __name__ == "__main__":
    update_path()




