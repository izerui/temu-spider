import re

def extract_script_content(text):
    # 正则表达式模式，用于匹配 <script> 标签及其内容
    pattern = re.compile(r'<script.*?>(.*?)</script>', re.DOTALL | re.IGNORECASE)

    # 查找所有匹配项
    matches = pattern.findall(text)

    return matches

if __name__ == '__main__':
    with open('tests/2.txt', 'r') as f:
        text = f.read()
        # 提取 <script> 标签中的内容
        script_contents = extract_script_content(text)

        # 打印结果
        for i, content in enumerate(script_contents, 1):
            print(f"Script {i} content:\n{content}\n")
