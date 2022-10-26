from random import randint as r
from random import shuffle as sh
import datetime
from datetime import datetime as DT

def print_array(array):
    for i in array:
        print(*i)
    print()

def get_random_date(start, end):
    delta = end - start
    return (start + datetime.timedelta(r(0, delta.days))).strftime('%d.%m.%Y')

def random_co():
    i_x = r(0, 9)
    j_x = r(0, 9)
    return i_x, j_x

def move(i_x, j_x):
    f = 1
    # print(i_x, j_x)
    while f:
        f = 0
        i = i_x + r(-1, 1)
        j = j_x + r(-1, 1)
        if i_x == i and j_x == j:
            f = 1
    # print(i, j)
    return i, j

def check(i, j, person):
    global map
    global base
    global today
    global season

    if 0 <= i <= 9 and 0 <= j <= 9:
        # print("Ход к", map[i][j], "координаты", i, j)
        if map[i][j] == "_":
            i_t, j_t = person["co"]
            person["co"] = i, j
            map[i_t][j_t] = "_"
            map[i][j] = person["name"]
        else:
            for person_2 in base:
                if person_2["co"][0] == i and person_2["co"][1] == j:
                    # print("Новый чел", person_2["name"], person_2["co"])
                    person_x = person_2
                    break
            # else:
                # print("Старт", i, j)
                # for person_2 in base:
                    # print(person_2["co"][0], person_2["co"][1])
                # exit()
            if person["name"] == person_x["name"]:
                # print("Cила_до", person["strength"], person_x["strength"])
                person["strength"] += 1
                person_x["strength"] += 1
                # print("Cила_после", person["strength"], person_x["strength"])
            else:
                # print("До сражения: ", person, person_x)
                str_1 = 3.14 * (int(today.split(".")[-1]) - int(person["birth"].split(".")[-1]))
                str_2 = + 3.14 * (int(today.split(".")[-1]) - int(person_x["birth"].split(".")[-1]))
                if person["name"] == season:
                    str_1 += person["strength"] * 1.5
                    str_1 = round(str_1)
                if person["name"] == season:
                    str_2 += person_x["strength"] * 1.5
                    str_2 = round(str_1)

                if str_1 > str_2:
                    person_x["name"] = person["name"]
                elif str_1 < str_2:
                    person["name"] = person_x["name"]
                # print("После сражения: ", person, person_x)


map = [["_" for i in range(10)] for j in range(10)]

today = DT.today().strftime('%d.%m.%Y')
# print(today)

base = []

for i in "1234":
    for j in range(10):
        f = 1
        while f:
            f = 0

            i_x, j_x = random_co()

            if map[i_x][j_x] != "_":
                f = 1
            else:
                map[i_x][j_x] = i
                strength = r(0, 100)

                start_dt = DT.strptime('01.01.1960', '%d.%m.%Y')
                # print(today)
                end_dt = DT.strptime(today, '%d.%m.%Y')

                birth = get_random_date(start_dt, end_dt)
                base.append({"name": i, "co": (i_x, j_x), "strength": strength, "birth": birth})
            # print(i_x, j_x)
            # print_map(map)

# print(*base, sep="\n")

for i in range(1, 101):
    season = str(i % 4 + 1)
    sh(base)
    print(f"Day {i}\n")
    # print(*base, sep="\n")
    print_array(map)
    for person in base:
        co = person["co"]
        move_co = move(co[0], co[1])
        check(move_co[0], move_co[1], person)

s = 0

result = [0, 0, 0, 0]

for i in map:
    for j in range(1, 5):
        result[j - 1] += i.count(str(j))

print("Результаты игр\n")

for i in range(1, 5):
    print(f"Племя {i} имеет {result[i - 1]} человек.")

print(f"\nПобедитель племя {result.index(max(result)) + 1}!")