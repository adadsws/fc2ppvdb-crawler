from bs4 import BeautifulSoup
import requests
import os
import time
# headers = {
#     "accept": "*/*",
#     "accept-encoding": "gzip, deflate, br, zstd",
#     "accept-language": "zh-TW,zh-HK;q=0.9,zh;q=0.8,en-US;q=0.7,en;q=0.6,zh-Hans;q=0.5,und;q=0.4",
#     "content-length": "16587",
#     "content-type": "text/plain;charset=UTF-8",
#     "cookie": "age_pass=eyJpdiI6ImcrczdPVitHdTBUK0NzVWhXNkxDTWc9PSIsInZhbHVlIjoiSWRGSzJVaHNySjdGSUhRb0lYa0wwQ1hIUHgybU14UWQ1SGY2WWdQK0gvZU5pMVJpcDhaVjkxTkY0a1RETzJhdiIsIm1hYyI6ImZlNjdiOGNmMTM1ZGE4NGE5NzgxMjkzZGZmMmRjNDljZmEwN2UxMzc5MmVkZGUzNWZhMjU2YzAzNzZjZjEwN2EiLCJ0YWciOiIifQ%3D%3D; stype=eyJpdiI6ImVmMFVCc0ozb0Q1Q1E2QlAxTjdGdlE9PSIsInZhbHVlIjoiR2lLdVBWZzEwOGcraStkZ3o1eXhjZG1iV1FRS2R6ODBPYzVTelB1bUZMbXpKTHZ3ZWVtMkFoQ2hsbWxablBPdCIsIm1hYyI6IjZkYTU0ZDJmYmY3ZGI4MWE0OWNjNTA3YmEwM2VjOTFmNDIxMjVhNGI4OGQyNDM0YmQ4N2EzYjkwM2JiY2VjYTIiLCJ0YWciOiIifQ%3D%3D; XSRF-TOKEN=eyJpdiI6Ik0rN21ITjY0d01xM1lNY0ZuSHVzQWc9PSIsInZhbHVlIjoieGR1eUdKLytmQjQveS82bll1dmxaRUVueEdOSEZYcVNPZkZJUjYzVWQ3YjRiUDVPVGgxSU4xcmpxWStBdm5RQjB5VzJzWUpHZjROcS80UjhSTmg1SVVRL2NXdkVHTDRyMzRud3hubEF4UTNVK2M2NXFUVkc0elFkajRBcUJXbzgiLCJtYWMiOiIyOGQ3YjU3OWYxODQ0NWI2M2U5NGM4YjgyODk5YWE5MDQxMTY0MGM5NDgzNmI1YWNmZTgwYzUzNTg0NTRiYzM0IiwidGFnIjoiIn0%3D; fc2ppvdb_session=eyJpdiI6ImpsS2tFdFN6NEtrY3pIK3haenRlc3c9PSIsInZhbHVlIjoiNjJ2YmF3ajVYUzQ0RnRiUFZadlFLMUM3Wi85cUJtTUlVSllLSWxmd3Qrb0kzOTJoVUJLQ2syN2JpR3NHYmtKTUVid0dGLzFaYWc0OVVyMFZlWWxiQUZhN1VMQTZ5MGkxN3pTdkthUkltV1VtV1pyVE5qamdqK3hXOFlvcnVUUC8iLCJtYWMiOiI0MDg5YjdkODBjZGFlYWI4MGMwMDE1N2YzZjFmMjQ3NzYwODBmZjgxYzE3MTcxZWM5ZGJhMzE5NGZiMzA3MzFhIiwidGFnIjoiIn0%3D; cf_clearance=S32tQMCF7PUC_2R8O4VUMaz2oWGf9c4bYDm.SktJX7A-1745642828-1.2.1.1-S7kh_I07CpjJAuFCuinmQi1LdV855FveUnZjwEsmPDkZZnU1tEbv.A7mDPxdg.jW0xyUIJoFrOigNg.BnvjJhiS8lJp_oaqQXL4T_DUBaeD..So2kKgecLVOEE2ZrcDj2PzbWLtfhs69wWqH1lPKTRQ.j0iWXiBxfuBxRIjC4uW9LlnSJo7YdrLFKWjNq.fxguFPQ_AfLg6FavEdEwx12SNszZh5.a88b9wyoUMcP5eKJE2ykaB_qQvFVkr1nzuE_vddZ6XaVYp71iQMR.kw3ycslHPY2O5blCcI8O7fePY.ORtm80aV_1N5WRahlK3wc.KgWM6ax_cJreH1zDvtcz8oDredkNFNBG4QZ3AWzok",
#     "origin": "https://fc2ppvdb.com",
#     "priority": "u=1, i",
#     "sec-ch-ua": '"Chromium";v="134", "Not:A-Brand";v="24", "Google Chrome";v="134"',
#     "sec-ch-ua-mobile": "?0",
#     "sec-ch-ua-platform": '"Windows"',
#     "sec-fetch-dest": "empty",
#     "sec-fetch-mode": "cors",
#     "sec-fetch-site": "same-origin",
#     "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36"
# }

headers = {
    "cookie": "age_pass=eyJpdiI6ImcrczdPVitHdTBUK0NzVWhXNkxDTWc9PSIsInZhbHVlIjoiSWRGSzJVaHNySjdGSUhRb0lYa0wwQ1hIUHgybU14UWQ1SGY2WWdQK0gvZU5pMVJpcDhaVjkxTkY0a1RETzJhdiIsIm1hYyI6ImZlNjdiOGNmMTM1ZGE4NGE5NzgxMjkzZGZmMmRjNDljZmEwN2UxMzc5MmVkZGUzNWZhMjU2YzAzNzZjZjEwN2EiLCJ0YWciOiIifQ%3D%3D; stype=eyJpdiI6ImVmMFVCc0ozb0Q1Q1E2QlAxTjdGdlE9PSIsInZhbHVlIjoiR2lLdVBWZzEwOGcraStkZ3o1eXhjZG1iV1FRS2R6ODBPYzVTelB1bUZMbXpKTHZ3ZWVtMkFoQ2hsbWxablBPdCIsIm1hYyI6IjZkYTU0ZDJmYmY3ZGI4MWE0OWNjNTA3YmEwM2VjOTFmNDIxMjVhNGI4OGQyNDM0YmQ4N2EzYjkwM2JiY2VjYTIiLCJ0YWciOiIifQ%3D%3D; XSRF-TOKEN=eyJpdiI6Ik0rN21ITjY0d01xM1lNY0ZuSHVzQWc9PSIsInZhbHVlIjoieGR1eUdKLytmQjQveS82bll1dmxaRUVueEdOSEZYcVNPZkZJUjYzVWQ3YjRiUDVPVGgxSU4xcmpxWStBdm5RQjB5VzJzWUpHZjROcS80UjhSTmg1SVVRL2NXdkVHTDRyMzRud3hubEF4UTNVK2M2NXFUVkc0elFkajRBcUJXbzgiLCJtYWMiOiIyOGQ3YjU3OWYxODQ0NWI2M2U5NGM4YjgyODk5YWE5MDQxMTY0MGM5NDgzNmI1YWNmZTgwYzUzNTg0NTRiYzM0IiwidGFnIjoiIn0%3D; fc2ppvdb_session=eyJpdiI6ImpsS2tFdFN6NEtrY3pIK3haenRlc3c9PSIsInZhbHVlIjoiNjJ2YmF3ajVYUzQ0RnRiUFZadlFLMUM3Wi85cUJtTUlVSllLSWxmd3Qrb0kzOTJoVUJLQ2syN2JpR3NHYmtKTUVid0dGLzFaYWc0OVVyMFZlWWxiQUZhN1VMQTZ5MGkxN3pTdkthUkltV1VtV1pyVE5qamdqK3hXOFlvcnVUUC8iLCJtYWMiOiI0MDg5YjdkODBjZGFlYWI4MGMwMDE1N2YzZjFmMjQ3NzYwODBmZjgxYzE3MTcxZWM5ZGJhMzE5NGZiMzA3MzFhIiwidGFnIjoiIn0%3D; cf_clearance=S32tQMCF7PUC_2R8O4VUMaz2oWGf9c4bYDm.SktJX7A-1745642828-1.2.1.1-S7kh_I07CpjJAuFCuinmQi1LdV855FveUnZjwEsmPDkZZnU1tEbv.A7mDPxdg.jW0xyUIJoFrOigNg.BnvjJhiS8lJp_oaqQXL4T_DUBaeD..So2kKgecLVOEE2ZrcDj2PzbWLtfhs69wWqH1lPKTRQ.j0iWXiBxfuBxRIjC4uW9LlnSJo7YdrLFKWjNq.fxguFPQ_AfLg6FavEdEwx12SNszZh5.a88b9wyoUMcP5eKJE2ykaB_qQvFVkr1nzuE_vddZ6XaVYp71iQMR.kw3ycslHPY2O5blCcI8O7fePY.ORtm80aV_1N5WRahlK3wc.KgWM6ax_cJreH1zDvtcz8oDredkNFNBG4QZ3AWzok",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36"
}

# 目标网页 URL
url = "https://fc2ppvdb.com/actresses/4312"

time.sleep(5)
response = requests.get(url, headers=headers)

if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # 保存为文件
    html_content = soup.prettify()
    output_file = os.path.join("page_content.html")
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"网页内容已保存到: {output_file}")
else:
    print(f"无法访问网页，状态码: {response.status_code}")
    exit()

