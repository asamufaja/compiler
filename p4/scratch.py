import sys

from model.OpCode import OpCodes
import json
import mmap

def main():
    a = sys.stdin.read(1)
    print(a)
    b = sys.stdin.read(1)
    b += sys.stdin.read(1)
    print(b)

    # for ops in OpCodes:
    #     print(ops.name)
    # file = open("asm/we.bin")
    # mmapfile = mmap.mmap(file.fileno(), 0, access=mmap.ACCESS_READ)
    # print(int.from_bytes(mmapfile.read(4), "little"))
    #
    # mmapfile.flush()
    # mmapfile.close()
    # file.close()
    # print("R" + str(3))
    # a = ["a", "b", ["c"]]
    # for thing in a:
    #     print(thing)
    #     if isinstance(thing, list):
    #         thing = thing[0]
    #         print(thing)
    # print(int("-4"))
    # newln = ""
    # newln += "\\"
    # newln += "n"
    # if newln == "\\" + "n":
    #     print("true")
    #     newln = "\n"
    # print("hi", newln, "how r u", sep="")



if __name__ == "__main__":
    main()