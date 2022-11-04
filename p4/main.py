import sys
from vm.Assembler import Assembler
from vm.VirtualMachine import VirtualMachine

def main():
    if len(sys.argv) < 2:
        print("usage: python3 main.py <filename.ext>")
        exit(1)
    
    file_name = sys.argv[1]
    if file_name.endswith(".asm"):
        assem = Assembler(file_name)
    elif file_name.endswith(".bin"):
        runvm = VirtualMachine(file_name)
    else:
        print("file extension must be .asm or .bin")

    
if __name__ == '__main__':
    main()