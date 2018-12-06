from beeprint import pp


def main():
    while True:
        command = input("Enter command:")
        if command == 'quit':
            print("Exited")
            return
        result = 'todo'  # todo bind generator
        print("\n")
        pp(result)
        print("\n")


if __name__ == '__main__':
    main()
