import itertools
import time, os
# сортировка брони

class Armor:
    def __init__(self, line):
        armor = line.split(",")
        self.line = line
        self.tag = armor[3]
        self.tier = armor[4]
        self.type = armor[5]
        self.equippable = armor[7]
        self.masterworkType = armor[9]
        self.notes = armor[34]


        list_name_stats = [
            "Mobility",
            "Resilience",
            "Recovery",
            "Discipline",
            "Intellect",
            "Strength",
        ]
        self.stats = dict(zip(list_name_stats, armor[26:32]))
        for stat in self.stats:
            self.stats[stat] = int(self.stats[stat]) + 2.5  # сет в абсадюте

    def clear_tags(self):
        # if not self.tag in 'infuse':
        self.tag = "junk"
        self.notes = ""

    def show_line(self):
        armor = self.line.split(',')
        armor[3] = self.tag
        armor[34] = self.notes
        armor = ','.join(armor)
        return armor

class TypeArmor:
    def __init__(self, energy):
        self.energy = energy
        self.helmet = list()
        self.gauntlets = list()
        self.chest_armor = list()
        self.leg_armor = list()

    def add(self, armor):
        if armor.type in ["Helmet", "Шлем"]:
            self.helmet.append(armor)
        if armor.type in ["Gauntlets", "Рукавицы"]:
            self.gauntlets.append(armor)
        if armor.type in ["Chest Armor", "Нагрудник"]:
            self.chest_armor.append(armor)
        if armor.type in ["Leg Armor", "Броня для ног"]:
            self.leg_armor.append(armor)
    
    def show(self):
        arrayAllArmors = []
        for armor in self.helmet:
            arrayAllArmors.append(armor.show_line() + '\n')
        for armor in self.gauntlets:
            arrayAllArmors.append(armor.show_line() + '\n')
        for armor in self.chest_armor:
            arrayAllArmors.append(armor.show_line() + '\n')
        for armor in self.leg_armor:
            arrayAllArmors.append(armor.show_line() + '\n')
        return arrayAllArmors

    def sorting_armors(self, list_stats):
        self.setArmor = (None, None, None, None)
        self.list_stats = list_stats

        arr_set_armor = itertools.product(
            self.helmet,
            self.gauntlets,
            self.chest_armor,
            self.leg_armor,
            )

        self.arrState = [[[i, 0] for i in self.list_stats[1:]]]
        self.sum_stats = self.cal_sum_stats(self.arrState[0], 2)

        coun = 0
        for setArmor in arr_set_armor:
            coun += 1
            self.check_stat(setArmor)

        self.tag_record()
        return

    def check_stat(self, setArmor):
        arrStats = self.cal_set_stat(setArmor)
        res_comparison = self.comparison(arrStats, 0)
        if res_comparison == 1:
            self.setArmor = list(setArmor)
        elif res_comparison == 2:
            self.setArmor = list(set(self.setArmor) | set(setArmor))

    def cal_set_stat(self, setArmor):  # Подсчет статов в сете
        arrStats = [[i, 0] for i in self.list_stats[1:]]
        for item in setArmor:
            for stat in arrStats:
                stat[1] += item.stats[stat[0]]
        return [[i[0], int(i[1])] for i in arrStats]

    def cal_sum_stats(self, arrState, size):  # сумма первых двух статов
        sum = 0
        for num in range(size):
            sum += arrState[num][1] // 10
        return sum

    def comparison(self, arrState, num):
        new_sum_stats = self.cal_sum_stats(arrState, 2)
        if new_sum_stats > self.sum_stats:
            self.sum_stats = new_sum_stats
            if len(self.arrState) > 1:
                self.arrState = [self.arrState[num]]
            self.arrState[num] = arrState
            return 1
        elif new_sum_stats == self.sum_stats:
            return self.stat_comparison(arrState, 2, num)

    def stat_comparison(self, arrState, pos, num):
        if arrState[pos][1] // 10 > self.arrState[num][pos][1] // 10:
            if len(self.arrState) > 1:
                self.arrState = [self.arrState[num]]
            self.arrState[num] = arrState
            return 1
        elif arrState[pos][1] // 10 == self.arrState[num][pos][1] // 10:
            if pos + 1 <= 4:
                return self.stat_comparison(arrState, pos + 1, num)
            else:
                self.arrState.append(arrState)
                return 2

    def tag_record(self):
        for armor in self.setArmor:
            armor.tag = "favorite"
            if armor.notes == "":
                armor.notes = self.list_stats[0] + ' ' +  self.energy
            else: armor.notes = armor.notes + " - " + self.list_stats[0] + ' ' +  self.energy


class ClassArmor:
    def __init__(self):
        self.all_energy = TypeArmor('All')
        self.void_energy = TypeArmor('Void')
        self.solar_energy = TypeArmor('Solar')
        self.arc_energy = TypeArmor('Arc')


    def add(self, armor):
        armor.clear_tags()

        self.all_energy.add(armor)
        if armor.masterworkType in ["Void Energy Capacity", "Энергетическая емкость (Пустота)"]:
            self.void_energy.add(armor)
        elif armor.masterworkType in ["Solar Energy Capacity", "Энергетическая емкость (Солнце)"]:
            self.solar_energy.add(armor)
        elif armor.masterworkType in ["Arc Energy Capacity", "Энергетическая емкость (Молния)"]:
            self.arc_energy.add(armor)


    def sorting(self, list_stat):
        self.all_energy.sorting_armors(list_stat[0])
        self.all_energy.sorting_armors(list_stat[1])
        self.arc_energy.sorting_armors(list_stat[0])
        self.arc_energy.sorting_armors(list_stat[1])
        self.void_energy.sorting_armors(list_stat[0])
        self.void_energy.sorting_armors(list_stat[1])
        self.solar_energy.sorting_armors(list_stat[0])
        self.solar_energy.sorting_armors(list_stat[1])

    def show(self):
        arrayAllArmors = self.all_energy.show()
        return arrayAllArmors

class Main:
    def __init__(self, filename):
        self.warlock = ClassArmor()
        self.titan = ClassArmor()
        self.hunter = ClassArmor()

        self.read_file(filename)
        self.sorting()
        self.write_file(filename)

    def read_file(self, filename):
        exception_tags = ["infuse", "keep"]
        # exception_tags = ["keep"]
        # exception_tags = ['']
        with open(filename, "r", encoding="utf-8") as file:
            lines = file.read().split("\n")
        for line in lines[1:]:
            armor = Armor(line)
            if (armor.tier == "Legendary") and (not armor.tag in exception_tags):
                if armor.equippable in ["Warlock", "Варлок"]:
                    self.warlock.add(armor)
                if armor.equippable in ["Titan", "Титан"]:
                    self.titan.add(armor)
                if armor.equippable in ["Hunter", "Охотник"]:
                    self.hunter.add(armor)
        

    def sorting(self):
        list_warlock_stats = (
            ("PVP", "Resilience", "Recovery", "Discipline", "Intellect", "Strength",),
            ("PVE", "Recovery", "Discipline", "Resilience", "Intellect", "Strength"),
        )
        self.warlock.sorting(list_warlock_stats)

        list_titan_stats = (
            ("PVP", "Resilience", "Recovery", "Discipline", "Intellect", "Strength",),
            ("PVE", "Recovery", "Strength", "Resilience", "Discipline", "Intellect"),
        )
        self.titan.sorting(list_titan_stats)

        list_hunter_stats = (
            ("PVP", "Resilience", "Recovery", "Discipline", "Intellect", "Strength",),
            ("PVE", "Recovery", "Discipline", "Resilience", "Intellect", "Strength"),
        )
        self.hunter.sorting(list_hunter_stats)

    def write_file(self, filename):
        with open(filename, "r", encoding="utf-8") as file:
            lines = file.readline()
        with open(filename, "w", encoding='utf-8') as file:
            file.write(lines)
            file.writelines(self.warlock.show())
            file.writelines(self.titan.show())
            file.writelines(self.hunter.show())

        return

if __name__ == "__main__":
    start_time = time.time()

    path = "E:/python/PRO/Destiny_2/"
    time_f = 0
    fail_Arm = ""
    
    all_f = os.listdir(path)

    for f in all_f:
        if f.find("Armor") > 0 and f.find(".csv") > 0:
            if time_f < (os.stat(path + f).st_mtime):
                time_f = os.stat(path + f).st_mtime
                fail_Arm = f

    process = Main(path + fail_Arm)

    print("__name__ --- %0.3f seconds ---" % (time.time() - start_time))
    print('The END')
