import os
import re


def extract_script_content(text):
    # 正则表达式模式，用于匹配 <script> 标签及其内容
    pattern = re.compile(r'<script.*?>(.*?)</script>', re.DOTALL | re.IGNORECASE)

    # 查找所有匹配项
    matches = pattern.findall(text)

    return matches


if __name__ == '__main__':
    current_file_path_os = os.path.abspath(__file__)
    current_dir_path_os = os.path.dirname(current_file_path_os)
    script_contents = None
    with open(os.path.join(current_dir_path_os, 'login.txt'), 'r') as f:
        text = f.read()
        # 提取 <script> 标签中的内容
        script_contents = extract_script_content(text)

        # 打印结果
        for i, content in enumerate(script_contents, 1):
            print(f"Script {i} content:\n{content}\n")

    js_file = os.path.join(current_dir_path_os, 'js_login.txt')
    if os.path.exists(js_file):
        os.remove(js_file)
    with open(js_file, 'a') as f:
        # 打印结果
        for i, content in enumerate(script_contents, 1):
            line = f"Script {i} content: ============================================================ \n{content}\n\n"
            f.write(line)
