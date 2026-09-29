def g():
    try:
        return 10 / 0
    finally:
        print("B")
g()