from os import path


usrname_path = path.join(
    "static",
    "usrname.png"
)

anon_path = path.join(
    "static",
    "anon.jpg"
)


usrname = open(usrname_path, "rb").read()
anon = open(anon_path, "rb").read()
