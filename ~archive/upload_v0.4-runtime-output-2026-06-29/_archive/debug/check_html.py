import re

with open('html/木下ひまり 女優 - FC2PPVDB.html', encoding='utf-8') as f:
    content = f.read()

# 脚本引用
scripts = re.findall(r'<script[^>]+src=["\']([^"\']+)["\']', content)
print("=== Scripts ===")
for s in scripts:
    print(s)

print("\n=== Frameworks ===")
for kw in ['livewire', 'wire:', 'x-data', 'alpine', 'Alpine', 'axios', 'fetch(', 'XMLHttpRequest', 'vue', 'Vue', 'react', 'React']:
    idx = content.find(kw)
    if idx >= 0:
        print(f"[{kw}] ...{content[max(0,idx-20):idx+80]}...")
