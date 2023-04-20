from loader import load


def recommend(user_animes, user_tags):
    pass


if __name__ == "__main__":
    animes, tags = load()
    user_animes = []
    user_tags = []
    while True:
        print("""input command:
            1. show all tags available
            2. show all animes available
            3. add your preference tag
            4. add your preference anime
            5. get recommendation
            6. clear all tags
            7. quit
              """)
        c = input()
        if c == "1":
            print(list(tags.keys()))
        elif c == "2":
            print(list(animes.keys()))
        elif c == "3":
            while True:
                t = input()
                if t == "break":
                    break
                if t in tags:
                    user_tags.append(t)
                    print("Current tags:")
                    print(user_tags)
                    break
                else:
                    print("Invalid tag, please input again or type break to stop")
        elif c == "4":
            while True:
                a = input()
                if a == "break":
                    break
                if a in animes:
                    user_animes.append(a)
                    print("Current animes:")
                    print(user_animes)
                    break
                else:
                    print("Invalid anime, please input again or type break to stop")
        elif c == "5":
            pass
        elif c == "6":
            user_animes = []
            user_tags = []
        elif c == "7":
            break
        else:
            print("Invalid command, please input again")
