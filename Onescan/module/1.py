b=10
def a(c):
    global b
    c=10+20
    b = c
    print(b)
a(b)
print(b)