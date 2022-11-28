def isInSym(x, sym_table):
    if x in sym_table:
        return True, sym_table[x]
    for k, v in sym_table.items():
        if isinstance(v, dict):
            if x in v:
                return True, v[x]
            for k1, v1 in v.items():
                if isinstance(v1, dict):
                    if x in v1:
                        return True, v1[x]
    return False

def main():
    testsym1 = {
        "class 1": {
            "data member 1": ["type", "size", "offset"],
            "data member 2": ["type", "size", "offset"],
            "member function 1": {
                "local var 1": ["type", "size", "offset"]
            },
            "member function 2": {
                "local var 1": ["type", "size" "offset"]
            }
        },
        "class 2": {
            "data member 1": ["type", "size", "offset"],
            "member function 1": {
                "local var 1a": ["type", "size", "offset"]
            }
        },
        "compunit aka main()": {
            "local var 1": ["type", "size", "offset"],
            "local var 2": ["type", "size", "offset"],
            "local var 3": ["type", "size", "offset"]
        }
    }

    print(isInSym("local var 1a", testsym1))



    testsym2 = [
        {
            "data member 1": ["type", "size", "offset"],
            "data member 2": ["type", "size", "offset"],
            "member function 1": {
               "local var 1": ["type", "size", "offset"]
            },
            "member function 2": {
               "local var 1": ["type", "size" "offset"]
            }
        },
        {
            "data member 1": ["type", "size", "offset"],
            "member function 1": {
                "local var 1": ["type", "size", "offset"]
            }
        },
        {
            "local var 1": ["type", "size", "offset"],
            "local var 2": ["type", "size", "offset"],
            "local var 3": ["type", "size", "offset"]
        }
    ]


if __name__ == "__main__":
    main()