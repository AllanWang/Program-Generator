from generator.generate import generate
from generator.result import Result
from pprint import pprint
from beeprint import pp



def main():
    while True:
        command = input("Enter command:")
        if command == 'quit':
            print("Exited")
            return
        result = generate(command)
        print("\n")
        pp(result)
        print("\n")


if __name__ == '__main__':
    main()
