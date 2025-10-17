
with open("deceptive-opinion.csv","r",encoding="utf-8") as f:
    for i, line in enumerate(f, 1):
        c = line.rstrip("\n\r")
        if c.count(",") != 1:
            print(f"Line {i} -> {c!r}")




