import os, re

if not os.path.exists("debug_snapshot.html"):
    print("debug_snapshot.html NOT FOUND - article count never exceeded 5")
else:
    content = open("debug_snapshot.html", encoding="utf-8").read()
    print("File size:", len(content))
    
    idx = content.find("actress-articles")
    if idx >= 0:
        print("\n[actress-articles context]")
        print(content[max(0, idx-50):idx+300])
    else:
        print("actress-articles NOT FOUND in live snapshot")
    
    matches = re.findall(r'<div class="([^"]*w-full p-4[^"]*)"', content)
    print("\n[Film container classes]", matches[:2] if matches else "NONE")
    
    spans = re.findall(r'<span class="([^"]*absolute[^"]*)"', content)
    print("\n[Span classes]", spans[:3] if spans else "NONE")
    
    links = re.findall(r'href="(https://fc2ppvdb\.com/articles/\d+)"', content)
    print("\n[Article links count]", len(links))
    if links:
        print("First 3:", links[:3])
