

from re import T


test = "HOt                  The Beginning After the End                    "

tt = ""
for t in test.split():
    if "HOt" not in t:
        tt+=t
        tt+=' '
print(tt)