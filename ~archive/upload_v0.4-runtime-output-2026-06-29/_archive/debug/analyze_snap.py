import re

c = open("debug_snapshot_5s.html", encoding="utf-8").read()
print("Size:", len(c))

# actress-articles 内容
idx = c.find('id="actress-articles"')
if idx >= 0:
    print("\n[actress-articles block - first 800 chars]:")
    print(c[idx:idx+800])
else:
    print("actress-articles NOT FOUND")

# 找所有 /articles/数字 链接
all_links = re.findall(r'href="([^"]*?/articles/\d+[^"]*?)"', c)
print(f"\nTotal /articles/ links: {len(all_links)}")
print("First 5:", all_links[:5])

# 找第一个链接的上下文，看看在哪个容器里
if all_links:
    link = all_links[0]
    li = c.find(f'href="{link}"')
    print(f"\nContext around first link ({link}):")
    print(c[max(0, li-200):li+100])

# 检查 XHR/fetch 请求相关
print("\n[data-* attributes on actress-articles]:")
m = re.search(r'id="actress-articles"([^>]*)', c)
if m:
    print(m.group(0))
