import random
import subprocess
import time

KP = 0 # 経験値
BP = 0 # ダンジョンの階層
SP = 0 # 死神の出現フラグ
HA = 0 # 連撃
PP = 0 # ポーション
NKP = 0 # 拘束時間
PDP = 0 # 攻撃無効
MKP = 0 # 無敵時間
EP = 0 # 英雄の証
EEP = 0 # 古代の進化(ゴーレム)
GA = 0 # 5連撃

# ゲームスタート
def main():
    subprocess.call("cls", shell=True)
    player_name = input("プレイヤーの名前を入力してください: ")
    subprocess.call("cls", shell=True)
    if player_name == "ああああ":
        player = Player(player_name, 100, 9999, 9999, 99, 99, 999, 99, 999, 99, ["透明な液体", "透明な液体", "透明な液体", "透明な液体", "死者の魂"])
    elif player_name == "テスト":
        player = Player(player_name, 250, 60, 40, 25, 5, 85, 2, 95, 2, [])
    else:
        player = Player(player_name, 100, 20, 0, 5, 1, 25, 2, 35, 2, [])
    subprocess.call("cls", shell=True)
    home_start(player)

    # メインループ
    while True:
        if SP % 5 == 0 and SP != 0:
            enemy = SPenemy
        else:
            if BP <= 1:
                enemy = random.choice(enemies1)
            elif BP == 2 or BP == 3: 
                enemy = random.choice(enemies2)
            elif BP == 4 or BP == 5:
                enemy = random.choice(enemies3)
            elif BP == 6:
                enemy = enemy4
            elif BP == 7:
                enemy = enemy5
            elif BP == 8:
                enemy = enemy6
            elif BP == 9:
                enemy = enemy7

        battle(player, enemy)

        if player.hp <= 0:
            print("ゲームオーバー！")
            break
        if BP == 10:
            print("\n", "congratulation!!!", "\n", "ゲームクリア")
            break
        if player.hp > 0 :
            time.sleep(0.5)
            print("無事生き延びることが出来たようだ")
            while True:
                select = input("どうする？ [1]先へ進む, [2]拠点に戻って休憩する, [3]アイテムを確認する >")
                subprocess.call("cls", shell=True)
                if select == "1":
                    time.sleep(0.5)
                    print("\n", "敵が現れた！")
                    break
                elif select == "2":
                    home(player)
                    break
                elif select == "3":
                    itemK(player)
                else:
                    print("そんなコマンドはない！")

# プレイヤー
class Player:
    def __init__(self, name, hp, attack, defence, speed, level, Heal, HealC, Fire, FireC, item):
        self.name = name
        self.hp = hp
        self.max_hp = hp
        self.attack = attack
        self.attack_S = attack
        self.defence = defence
        self.defence_S = defence
        self.speed = speed
        self.speed_S = speed
        self.level = level
        self.Heal = Heal
        self.HealC = HealC
        self.HealC_S = HealC
        self.Fire = Fire
        self.FireC = FireC
        self.FireC_S = FireC
        self.item = item
    
    def __str__(self):
        return "{}: {} / {}".format(self.name, self.hp, self.max_hp)
    
    def printStr(self):
        time.sleep(0.8)
        subprocess.call("cls", shell=True)
        print("攻撃力：{}".format(self.attack))
        print("防御力：{}".format(self.defence))
        print("魔法攻撃力：{}".format(self.Fire))
        print("魔法回復力：{}".format(self.Heal))
        print("\n")

    def attack_enemy(self, enemy):
        crt1 = random.randint(1, 10)
        if "番犬のチョーカー" in self.item:
            crt1 -= 3
        if crt1 >= 3:
            damage = self.attack + random.randint(-4, 4) - enemy.defence
            if enemy.name == "ゴーレム":
                damage /= 2
            if damage < 1:
                damage = 1
            enemy.hp -= int(damage)
            print("{}の攻撃".format(self.name))
            time.sleep(0.8)
            print("{}のダメージを与えた！".format(int(damage)))
            time.sleep(0.5)
        else:
            damage = self.attack * 1.5 + random.randint(-5, 5)
            enemy.hp -= int(damage)
            print("{}の攻撃".format(self.name))
            time.sleep(1.0)
            print("クリティカル！")
            time.sleep(0.5)
            print("{}のダメージを与えた！".format(int(damage)))
            time.sleep(0.5)
    
    def heal(self):
        self.HealC -= 1
        heal_points = self.Heal + random.randint(-10, 10) + 30
        self.hp += heal_points
        if self.hp > self.max_hp:
            self.hp = self.max_hp
        time.sleep(0.5)
        print("{}は回復魔法を唱えた".format(self.name))
        time.sleep(0.5)
        print("{}回復した！".format(heal_points))
        time.sleep(0.5)

    def fire(self, enemy):
        self.FireC -= 1
        fire_points = self.Fire + random.randint(-10, 10)
        if enemy.name == "スライム" or enemy.name == "スコーピオン" or enemy.name == "ゴーレム":
            fire_points /= 2
        time.sleep(0.5)
        print("{}は攻撃魔法を唱えた".format(self.name))
        if enemy.name == "ゴースト":
            fire_points = 0
            time.sleep(0.8)
            print("{}には効かなかった".format(enemy.name))
            time.sleep(0.5)
        else:
            enemy.hp -= int(fire_points)
            time.sleep(0.8)
            print("{}のダメージを与えた！".format(int(fire_points)))
            time.sleep(0.5) 

    def level_up(self):
        self.level += 1
        self.max_hp += 60
        self.attack_S += 15
        self.defence_S += 10
        self.speed_S += 5
        self.Heal += 15
        self.Fire += 15
        self.hp = self.max_hp
        print("{}はレベルアップした！".format(self.name))
        time.sleep(0.5)
        print("HPが最大になった")
        time.sleep(0.5)
        print("HPが60上がった")
        time.sleep(0.5)
        print("攻撃力が15上がった")
        time.sleep(0.5)
        print("防御力が10上がった")
        time.sleep(0.5)
        print("素早さが5上がった")
        time.sleep(0.5)
        print("特技の性能が上がった")
        time.sleep(0.5)
        if self.level % 2 == 0:
            self.HealC_S += 1
            self.FireC_S += 1
            print("特技の使用回数が増えた")
            time.sleep(0.5)

# 敵キャラ
class Enemy:
    def __init__(self, name, hp, attack, defence, speed, level):
        self.name = name
        self.hp = hp
        self.max_hp = hp
        self.attack = attack
        self.defence = defence
        self.speed = speed
        self.level = level
    
    def __str__(self):
        return "{}: {} / {}".format(self.name, self.hp, self.max_hp)
    
    def attack_player(self, player):
        global NKP, MKP
        if NKP >= 1:
            time.sleep(0.5)
            print("{}の攻撃！".format(self.name))
            time.sleep(0.5)
            print("しかし攻撃は当たらなかった")
            time.sleep(0.5)
            NKP -= 1
            return
        damage = self.attack + random.randint(-2, 2) - player.defence
        if damage < 1:
            damage = 1
        if MKP >= 1:
            damage = 0
            MKP -= 1
        player.hp -= int(damage)
        print("{}の攻撃".format(self.name))
        time.sleep(0.8)
        print("{}のダメージをくらった！".format(int(damage)))
        time.sleep(0.5)
class EnemySli(Enemy): # スライム
    def attack_player(self, player):
        global NKP, MKP
        if NKP >= 1:
            time.sleep(0.5)
            print("{}の攻撃！".format(self.name))
            time.sleep(0.5)
            print("しかし攻撃は当たらなかった")
            time.sleep(0.5)
            NKP -= 1
            return
        SA = random.randint(1, 5)
        if SA <= 2:
            damage = self.attack + random.randint(3, 10)
            if MKP >= 1:
                damage = 0
                MKP -= 1
            player.hp -= int(damage)
            print("{}の「溶解液」".format(self.name))
            time.sleep(0.8)
            print("{}のダメージをくらった！".format(int(damage)))
            time.sleep(0.5)
        else:
            damage = self.attack + random.randint(-2, 2) - player.defence
            if damage < 1:
                damage = 1
            if MKP >= 1:
                damage = 0
                MKP -= 1
            player.hp -= int(damage)
            print("{}の攻撃".format(self.name))
            time.sleep(0.8)
            print("{}のダメージをくらった！".format(int(damage)))
            time.sleep(0.5)
class EnemyGob(Enemy): # ゴブリン
    def attack_player(self, player):
        global PP, NKP, MKP
        if NKP >= 1:
            time.sleep(0.5)
            print("{}の攻撃！".format(self.name))
            time.sleep(0.5)
            print("しかし攻撃は当たらなかった")
            time.sleep(0.5)
            NKP -= 1
            return
        gobATT = random.randint(1, 4)
        portion = random.randint(28, 31)
        if gobATT == 1 and self.hp < 20 and PP == 0:
            print("{}はポーションを使った".format(self.name))
            time.sleep(0.8)
            print("{}回復した".format(portion))
            time.sleep(0.5)
            self.hp += portion
            PP += 1
        elif gobATT == 2 and self.hp < 30:
            damage = 30 + random.randint(-2, 2)
            if MKP >= 1:
                damage = 0
                MKP -= 1
            player.hp -= int(damage)
            print("{}は火炎瓶を投げつけてきた".format(self.name))
            time.sleep(0.8)
            print("{}のダメージをくらった！".format(int(damage)))
            time.sleep(0.5)
        else:
            damage = self.attack + random.randint(-2, 2) - player.defence
            if damage < 1:
                damage = 1
            if MKP >= 1:
                damage = 0
                MKP -= 1
            player.hp -= int(damage)
            print("{}の攻撃".format(self.name))
            time.sleep(0.8)
            print("{}のダメージをくらった！".format(int(damage)))
            time.sleep(0.5)
class EnemyGho(Enemy): # ゴースト
    def attack_player(self, player):
        global NKP, MKP
        if NKP >= 1:
            time.sleep(0.5)
            print("{}の攻撃！".format(self.name))
            time.sleep(0.5)
            print("しかし攻撃は当たらなかった")
            time.sleep(0.5)
            NKP -= 1
            return
        GA = random.randint(1, 5)
        if GA == 1 and len(player.item) >= 1:
            del_item = player.item.pop(0)
            print("{}の「消失」".format(self.name))
            time.sleep(1.0)
            print("「{}」が音もなく崩れ去っていった".format(del_item))
            time.sleep(0.5)
        else:
            damage = self.attack + random.randint(-2, 2) - player.defence
            if damage < 1:
                damage = 1
            if MKP >= 1:
                damage = 0
                MKP -= 1
            player.hp -= int(damage)
            print("{}の攻撃".format(self.name))
            time.sleep(0.8)
            print("{}のダメージをくらった！".format(int(damage)))
            time.sleep(0.5)
class EnemySco(Enemy): # スコーピオン
    def attack_player(self, player):
        global NKP, MKP
        if NKP >= 1:
            time.sleep(0.5)
            print("{}の攻撃！".format(self.name))
            time.sleep(0.5)
            print("しかし攻撃は当たらなかった")
            time.sleep(0.5)
            NKP -= 1
            return
        T = random.randint(1, 5)
        if T == 1:
            damage = self.attack * 1.4 + random.randint(-2, 2)
            if MKP >= 1:
                damage = 0
                MKP -= 1
            print("{}の「致命の一撃」".format((self.name)))
        else:
            damage = self.attack + random.randint(-2, 2) - player.defence
            if damage < 1:
                damage = 1
            if MKP >= 1:
                damage = 0
                MKP -= 1
            print("{}の攻撃".format((self.name)))
        player.hp -= int(damage)
        time.sleep(0.8)
        print("{}のダメージをくらった！".format(int(damage)))
        time.sleep(0.5)
class EnemyKel(Enemy): # ケルベロス
    def attack_player(self, player):
        global HA, NKP, MKP
        if NKP >= 1:
            time.sleep(0.5)
            print("{}の攻撃！".format(self.name))
            time.sleep(0.5)
            print("しかし攻撃は当たらなかった")
            time.sleep(0.5)
            NKP -= 1
            return
        T = random.randint(1, 5)
        if T <= 2 and self.hp < self.max_hp / 2:
            HA = 0
            print("{}の「二連撃」".format(self.name))
            damage = 0
            while HA < 2:
                damage5 = int(self.attack * 0.8 + random.randint(-2, 2) - player.defence / 2)
                if damage5 < 1:
                    damage5 = 1
                if MKP >= 1:
                    damage5 = 0
                time.sleep(0.8)
                print("{}のダメージをくらった！".format(damage5))
                damage += damage5
                HA += 1
        else:
            damage = int(self.attack + random.randint(-2, 2) - player.defence)
            if damage < 1:
                damage = 1
            if MKP >= 1:
                damage = 0
            print("{}の攻撃".format(self.name))
            time.sleep(0.8)
            print("{}のダメージをくらった！".format(damage))
        player.hp -= damage
        time.sleep(0.5)
        if MKP >= 1:
            MKP -= 1
class BOSSenemyVan(Enemy): # ヴァンパイア
    def attack_player(self, player):
        global NKP, MKP
        if NKP >= 1:
            time.sleep(0.5)
            print("{}の攻撃！".format(self.name))
            time.sleep(0.5)
            print("しかし攻撃は当たらなかった")
            time.sleep(0.5)
            NKP -= 1
            return
        T = random.randint(1, 5)
        if T <= 1 and self.hp < self.max_hp / 2:
            damage = int(self.attack * 1.5 + random.randint(-2, 2) - player.defence)
            if damage < 1:
                damage = 1
            if MKP >= 1:
                damage = 0
                MKP -= 1
            print("{}の「吸血」".format(self.name))
            self.hp += damage
            if self.hp > self.max_hp:
                self.hp = self.max_hp
            time.sleep(0.8)
            print("{}のダメージをくらった！".format(damage))
            time.sleep(0.8)
            print("{}は{}回復した".format(self.name, damage))
        else:
            damage = int(self.attack + random.randint(-2, 2) - player.defence)
            if damage < 1:
                damage = 1
            if MKP >= 1:
                damage = 0
                MKP -= 1
            print("{}の攻撃".format(self.name))
            time.sleep(0.8)
            print("{}のダメージをくらった！".format(damage))
        player.hp -= damage
        time.sleep(0.5)
class BOSSenemyGol(Enemy): # ゴーレム
    def attack_player(self, player):
        global NKP, MKP, EEP
        if NKP >= 1:
            time.sleep(0.5)
            print("{}の攻撃！".format(self.name))
            time.sleep(0.5)
            print("しかし攻撃は当たらなかった")
            time.sleep(0.5)
            NKP -= 1
            return
        T = random.randint(1, 5)
        if self.hp <= self.max_hp / 2 and EEP == 0:
            print("{}の「古代の進化」".format(self.name))
            time.sleep(0.5)
            self.hp = self.max_hp
            print("{}のhpが最大になった".format(self.name))
            time.sleep(0.5)
            self.defence += 10
            print("{}の防御力が上昇した".format(self.name))
            time.sleep(0.5)
            self.attack += 20
            print("{}の攻撃力が上昇した".format(self.name))
            time.sleep(0.5)
            EEP += 1
        elif T <= 2:
            damage = self.attack * 1.4 + random.randint(-2, 2)
            if MKP >= 1:
                damage = 0
                MKP -= 1
            print("{}の「破滅の一撃」".format((self.name)))
            time.sleep(0.8)
            player.hp -= int(damage)
            print("{}のダメージをくらった！".format(int(damage)))
            time.sleep(0.5)
        else:
            damage = self.attack + random.randint(-2, 2) - player.defence
            if damage < 1:
                damage = 1
            if MKP >= 1:
                damage = 0
                MKP -= 1
            print("{}の攻撃".format((self.name)))
            time.sleep(0.8)
            player.hp -= int(damage)
            print("{}のダメージをくらった！".format(int(damage)))
            time.sleep(0.5)
class BOSSenemyHyu(Enemy): # ヒュドラ
    def attack_player(self, player):
        global HA, NKP, MKP
        if NKP >= 1:
            time.sleep(0.5)
            print("{}の攻撃！".format(self.name))
            time.sleep(0.5)
            print("しかし攻撃は当たらなかった")
            time.sleep(0.5)
            NKP -= 1
            return
        T = random.randint(1, 5)
        if T <= 2 and self.hp < self.max_hp / 2:
            HA = 0
            print("{}の「五連撃」".format(self.name))
            damage = 0
            while HA < 5:
                damage5 = random.randint(25, 35)
                if damage5 < 1:
                    damage5 = 1
                if MKP >= 1:
                    damage5 = 0
                time.sleep(0.8)
                print("{}のダメージをくらった！".format(damage5))
                damage += damage5
                HA += 1
        else:
            damage = int(self.attack + random.randint(-2, 2) - player.defence)
            if damage < 1:
                damage = 1
            if MKP >= 1:
                damage = 0
            print("{}の攻撃".format(self.name))
            time.sleep(0.8)
            print("{}のダメージをくらった！".format(damage))
        player.hp -= damage
        time.sleep(0.5)
        if MKP >= 1:
            MKP -= 1
class BOSSenemyDor(Enemy): # ドラゴン
    def attack_player(self, player):
        global HA, NKP, MKP, GA
        if NKP >= 1:
            time.sleep(0.5)
            print("{}の攻撃！".format(self.name))
            time.sleep(0.5)
            print("しかし攻撃は当たらなかった")
            time.sleep(0.5)
            NKP -= 1
            return
        T = random.randint(1, 5)
        if T <= 1 and self.hp < self.max_hp / 2:
            print("{}は灼熱の火炎を吐いた".format(self.name))
            damage = int(self.attack * 1.5 + random.randint(-15, 15))
            if MKP >= 1:
                damage = 0
            time.sleep(1.0)
            print("{}のダメージをくらった！".format(damage))
        elif GA == 0:
            GA += 3
            HA = 0
            print("{}の「五連撃」".format(self.name))
            damage = 0
            while HA < 5:
                damage5 = int(self.attack * 0.5 + random.randint(-2, 2) - player.defence / 2)
                if damage5 < 1:
                    damage5 = 1
                if MKP >= 1:
                    damage5 = 0
                time.sleep(0.8)
                print("{}のダメージをくらった！".format(damage5))
                damage += damage5
                HA += 1
        else:
            damage = int(self.attack + random.randint(-2, 2) - player.defence)
            if damage < 1:
                damage = 1
            if MKP >= 1:
                damage = 0
            print("{}の攻撃".format(self.name))
            time.sleep(0.8)
            print("{}のダメージをくらった！".format(damage))
        player.hp -= damage
        time.sleep(0.5)
        if MKP >= 1:
            MKP -= 1
        if GA >=1:
            GA -= 1

# 戦闘
def battle(player, enemy):
    global PP, NKP, MKP, EEP, GA
    f2 = 0
    PP = 0
    NKP = 0
    MKP = 0
    EEP = 0
    enemy.hp = enemy.max_hp
    player.speed = player.speed_S
    player.attack = player.attack_S
    player.defence = player.defence_S
    player.HealC = player.HealC_S
    player.FireC = player.FireC_S
    if "透明な指輪" in player.item:
        player.speed += 20
    if "古びた指輪" in player.item:
        player.attack += 5
    if "鋼鉄の指輪" in player.item:
        player.defence += 7
    time.sleep(0.5)
    print("{}が現れた！".format(enemy.name))
    while True:
        print(player)
        print(enemy)
        command = input("どうする？ [a]攻撃, [s]特技, [i]アイテム, [r]逃げる > ")
        subprocess.call("cls", shell=True)
        if command == "a":
            enemyS = random.randint(-5, 5) + enemy.speed
            if player.speed >= enemyS:
                player.attack_enemy(enemy)
                if enemy.hp > 0:
                    enemy.attack_player(player)
                    usezomring(player)
            elif player.speed < enemyS:
                enemy.attack_player(player)
                if player.hp > 0:
                    player.attack_enemy(enemy)
                    usezomring(player)
            if enemy.hp <= 0:
                if enemy.name == "ゾンビ":
                    f = random.randint(1, 5)
                    if f <= 4 and f2 == 0:
                        print("{}を倒した！".format(enemy.name))
                        time.sleep(1.0)
                        print("なんと！{}は復活した！！".format(enemy.name))
                        time.sleep(0.5)
                        enemy.hp = int(enemy.max_hp / 2)
                        f2 += 1
                    else:
                        battle_win(player, enemy)
                        break
                else:
                    battle_win(player, enemy)
                    break
            if player.hp <= 0 and "死者の魂" not in player.item:
                time.sleep(0.5)
                print("{}は死んでしまった...".format(player.name))
                break
            elif player.hp <= 0 and "死者の魂" in player.item:
                usezomsoul(player)
        elif command == "s":
            while True:
                print(player)
                print(enemy)
                print("どうする？ [h]ヒール({}), [f]ファイア({})".format(player.HealC, player.FireC))
                print("※ スペースキーで戻る")
                commands = input("> ")
                subprocess.call("cls", shell=True)
                if commands == "h":
                    if player.HealC <= 0:
                        print("もう回復呪文は使えない！")
                    else:
                        player.heal()
                        enemy.attack_player(player)
                        usezomring(player)
                        break
                elif commands == "f":
                    if player.FireC <= 0:
                        print("もう攻撃魔法は使えない！")
                    else:
                        player.fire(enemy)
                        if enemy.hp > 0:
                            enemy.attack_player(player)
                        usezomring(player)
                        break
                elif commands == " ":
                    break
                else:
                    print("そんなコマンドはない！")
                    time.sleep(0.5)
            if enemy.hp <= 0:
                if enemy.name == "ゾンビ":
                    f = random.randint(1, 5)
                    if f <= 4 and f2 == 0:
                        print("{}を倒した！".format(enemy.name))
                        time.sleep(1.0)
                        print("なんと！{}は復活した！！".format(enemy.name))
                        time.sleep(0.5)
                        enemy.hp = int(enemy.max_hp / 2)
                        f2 += 1
                    else:
                        battle_win(player, enemy)
                        break
                else:
                    battle_win(player, enemy)
                    break
            if player.hp <= 0 and "死者の魂" not in player.item:
                time.sleep(0.5)
                print("{}は死んでしまった...".format(player.name))
                break
            elif player.hp <= 0 and "死者の魂" in player.item:
                usezomsoul(player)
        elif command == "i":
            print(player)
            print(enemy)
            while True:
                print("どれを使う？", end="")
                for i, j in enumerate(player.item):
                    index = int(i)
                    print("[{}]{}, ".format(index + 1, j), end="")
                print("\n", "※ スペースキーで戻る")
                select = input("> ")
                subprocess.call("cls", shell=True)
                try:
                    if 0 <= int(select) - 1 and int(select) - 1 <= 4:
                        useitem(player, enemy, player.item[int(select) - 1], int(select) - 1)
                        time.sleep(0.5)
                        break
                    else:
                        print("そんなコマンドはない！")
                        time.sleep(0.5)
                except ValueError:
                    if select == " ":
                        break
                    else:
                        print("そんなコマンドはない！")
                        time.sleep(0.5)
                except IndexError:
                    print("そんなコマンドはない！")
                    time.sleep(0.5)
            if enemy.hp <= 0:
                if enemy.name == "ゾンビ":
                    f = random.randint(1, 5)
                    if f <= 3 and f2 == 0:
                        print("{}を倒した！".format(enemy.name))
                        time.sleep(1.0)
                        print("なんと！{}は復活した！！".format(enemy.name))
                        time.sleep(0.5)
                        enemy.hp = enemy.max_hp
                        f2 += 1
                    else:
                        battle_win(player, enemy)
                        break
                else:
                    battle_win(player, enemy)
                    break
            if player.hp <= 0 and "死者の魂" not in player.item:
                time.sleep(0.5)
                print("{}は死んでしまった...".format(player.name))
                break
            elif player.hp <= 0 and "死者の魂" in player.item:
                usezomsoul(player)
        elif command == "r":
            R = random.randint(1, 10)
            if  R >= 6:
                print("{}は逃げ出した".format(player.name))
                time.sleep(1.0)
                break
            else:
                print("逃げられなかった")
                time.sleep(0.8)
                enemy.attack_player(player)
                usezomring(player)
                if player.hp <= 0 and "死者の魂" not in player.item:
                    time.sleep(0.5)
                    print("{}は死んでしまった...".format(player.name))
                    break
                elif player.hp <= 0 and "死者の魂" in player.item:
                    usezomsoul(player)
        else:
            print("そんなコマンドはない！")

# 拠点
def home(player):
    global BP, SP
    BP = 0
    time.sleep(0.5)
    print("{}はしっかり体を休めた".format(player.name))
    time.sleep(0.5)
    player.hp = player.max_hp
    print("HPが最大になった")
    time.sleep(0.5)
    while True:
        select = input("どうする？ [1]ダンジョンに挑む, [2]アイテムを整理する, [3]ステータスを確認する >")
        if select == "1":
            SP += 1
            subprocess.call("cls", shell=True)
            time.sleep(0.5)
            print("\n", "敵が現れた！")
            break
        elif select == "2":
            itemK(player)
            continue
        elif select == "3":
            Player.printStr(player)
        else:
            print("そんなコマンドはない！")
def home_start(player):
    global SP
    while True:
        select = input("どうする？ [1]ダンジョンに挑む, [2]アイテムを確認する, [3]ステータスを確認する >")
        if select == "1":
            SP += 1
            subprocess.call("cls", shell=True)
            time.sleep(0.5)
            print("\n", "敵が現れた！")
            break
        elif select == "2":
            itemK(player)        
            continue
        elif select == "3":
            player.printStr()
        else:
            print("そんなコマンドはない！")

# アイテムの整理・追加・使用
def itemK(player): # アイテムの整理(安全時)
    while True:
        print("どれを確認する？", end="")
        for i, j in enumerate(player.item):
            index = int(i)
            print("[{}]{}, ".format(index + 1, j), end="")
        print("\n", "※ スペースキーで戻る")
        select = input("> ")
        subprocess.call("cls", shell=True)
        try:
            if 0 <= int(select) - 1 and int(select) - 1 <= 4:
                itemC(player.item[int(select) - 1])
                time.sleep(0.5)
                break
            else:
                print("そんなコマンドはない！")
                time.sleep(0.5)
        except ValueError:
            if select == " ":
                break
            else:
                print("そんなコマンドはない！")
                time.sleep(0.5)
        except IndexError:
            print("そんなコマンドはない！")
            time.sleep(0.5)
def itemC(item_name): # アイテムの確認・説明
    if item_name == "スライムの粘液":
        print("「スライムの粘液」")
        time.sleep(0.5)
        print("透明で不気味な光を放つネバネバとした液体で、触れる者に寒気を走らせる。")
        print("※ 使用時、命中した敵は1ターン行動不能\n")
        time.sleep(0.5)
    elif item_name == "スライムゼリー":
        print("「スライムゼリー」")
        time.sleep(0.5)
        print("スライムから得られる半固形の物質。")
        print("緑と紫を混ぜたようなの色合いで謎めいた輝きを放っており、妙に神秘的な印象を受ける。")
        print("※ 使用時、特技使用回数回復\n")
        time.sleep(0.5)
    elif item_name == "ポーション":
        print("ポーション")
        time.sleep(0.5)
        print("消耗した冒険者の肉体と魂を癒し、再生させる能力を持っている。")
        print("乱用すると狂気に陥る危険が伴うと言われているが、その真偽は定かではない。")
        print("※ 使用時、hpを100回復\n")
        time.sleep(0.5)
    elif item_name == "古びた指輪":
        print("「古びた指輪」")
        time.sleep(0.5)
        print("長い年月を経て錆びついた鉄製の指輪。")
        print("着用者の筋力を僅かに上昇させる効果があるようだが、本来の力を発揮出来ていないようだ。")
        print("※ 攻撃力が10上昇\n")
        time.sleep(0.5)
    elif item_name == "透明な液体":
        print("「透明な液体」")
        time.sleep(0.5)
        print("透明だが不可解な輝きを放っており、粘性もあるため目を凝らせば視認出来る。")
        print("毒性を兼ね備えているが、自らを透明化出来るという魔力に誘われた服用者が後を絶たない。")
        print("※ 使用時、自分に100ダメージ又は3ターン攻撃無効化\n")
        time.sleep(0.5)
    elif item_name == "透明な指輪":
        print("「透明な指輪」")
        time.sleep(0.5)
        print("特殊な素材で構成されており、実際に手で触れることによってその存在を認知できる。")
        print("着用者の俊敏性は、ゴーストに勝るとも劣らない。")
        print("※ 素早さが20上昇\n")
        time.sleep(0.5)
    elif item_name == "腐った指輪":
        print("「腐った指輪」")
        time.sleep(0.5)
        print("これを手に入れたあなたは、その見た目よりも先に強烈な悪臭に顔をしかめることになるだろう。")
        print("今にも崩れ落ちてしまいそうな程朽ちているが、反面、強力な生命力を感じる。")
        print("※ 毎ターン終了時hpを15回復\n")
        time.sleep(0.5)
    elif item_name == "死者の魂":
        print("「死者の魂」")
        time.sleep(0.5)
        print("宝石の如く美しい白色の玉。")
        print("淡い輝きを放っているそれは、あなたが窮地に陥ったとき必ず役に立つだろう。")
        print("※ 死亡時に自動的に使用、最大hpの半分で復活\n")
        time.sleep(0.5)
    elif item_name == "番犬のチョーカー":
        print("「番犬のチョーカー」")
        time.sleep(0.5)
        print("一見すると何処にでも売っていそうな印象を受けるチョーカー。")
        print("その実、集中力を高める効果があるといわれており、間一髪で命拾いすることもあるだろう。")
        print("※ クリティカル率が上昇\n")
        time.sleep(0.5)
    elif item_name == "キャンディー":
        print("「キャンディー」")
        time.sleep(0.5)
        print("およそ人々に恐れられる番犬が食べているとは思えない程に普通のキャンディー。")
        print("もしかしたら何か特別な効果があるのかもしれないが、食べてみないことには分からない。")
        print("※ 使用時、2ターンの間攻撃を無効化\n")
        time.sleep(0.5)
    elif item_name == "毒針":
        print("「毒針」")
        time.sleep(0.5)
        print("スコーピオンから取れる尻尾で先端には鋭い針がある。")
        print("別名、ワンショットポイズンとも呼ばれており刺されたものは致命的なダメージを受ける。")
        print("※ 使用時、敵に1ダメージ又は大ダメージ\n")
        time.sleep(0.5)
    elif item_name == "鋼鉄の指輪":
        print("「鋼鉄の指輪」")
        time.sleep(0.5)
        print("はるか昔に女性がつけていた綺麗な指輪。")
        print("その女性が亡くなって以降その指輪には守護の力が宿ったと言う伝説が残された。")
        print("しかし現在所在が分からず知る者は誰も居ない。")
        print("※ 防御力が10上昇\n")
        time.sleep(0.5)
    elif item_name == "吸血の牙":
        print("「吸血の牙」")
        time.sleep(0.5)
        print("ヴァンパイアが持つ背筋が凍るほどに鋭利な牙。")
        print("刺されれば生命力を吸い取られてしまうであろうそれは刺突武器として使えそうだが、耐久力は高くないようだ。")
        print("※ 使用時、敵にダメージ＆回復\n")
        time.sleep(0.5)
    elif item_name == "ヴァンパイアの血液":
        print("「ヴァンパイアの血液」")
        time.sleep(0.5)
        print("赤黒く濁っているドロドロの血液。")
        print("一時的にヴァンパイア並の身体能力を得ることが出来ると言われているが、その副作用は明らかになっていない。")
        print("※ 使用時、すべてのステータスが一時的に上昇\n")
        time.sleep(0.5)
    elif item_name == "古代の秘宝":
        print("「古代の秘宝」")
        time.sleep(0.5)
        print("ゴーレムの動力源となっているコアの中でも、特に良質なもの。")
        print("無尽蔵のエネルギーに満ちており、もし手にしたものが現れたならこれをめぐる争いは避けられないだろう。")
        print("※ 使用時、敵味方に極大ダメージ\n")
        time.sleep(0.5)
    elif item_name == "英雄の証":
        print("「英雄の証」")
        time.sleep(0.5)
        print("英雄ーーー")
        print("時代によってその呼称や定義に多少の違いはあれど、そう呼ばれる者たちは決まって生物としての領域を逸脱していた。")
        print("彼らの共通点として、「ヒュドラ」の討伐に成功しており、致命傷を受けてもみるみるうちに傷が塞がってしまうというものがあるが、信憑性は低そうだ。")
        print("最も、今は「ヒュドラ」を打ち倒せる者などおらず、伝説上の存在となりつつある。")
        print("※ 使用時、hpを最大まで回復\n")
        time.sleep(0.5)
    elif item_name == "伝説の宝玉":
        print("「伝説の秘宝」")
        time.sleep(0.5)
        time.sleep(0.5)
def itemClean(player): # アイテムの整理(戦闘勝利後)
    while True:
        if len(player.item) > 5:
            get = input("アイテムがいっぱいだ [1]手持ちのアイテムと交換する, [2]交換しない > ")
            if get == "1":
                subprocess.call("cls", shell=True)
                print("どれを捨てる？", end="")
                for i, j in enumerate(player.item):
                    index = int(i)
                    print("[{}]{}, ".format(index + 1, j), end="")
                print("\n", "※ スペースキーで戻る")
                select = input("> ")
                subprocess.call("cls", shell=True)
                try:
                    if 0 <= int(select) - 1 and int(select) - 1 <= 5:
                        print("{}は{}を捨てた".format(player.name, player.item[int(select) - 1]))
                        player.item.pop(int(select) - 1)
                        time.sleep(0.5)
                        break
                    else:
                        print("そんなコマンドはない！")
                        time.sleep(0.5)
                except ValueError:
                    if select == " ":
                        pass
                    else:
                        print("そんなコマンドはない！")
                        time.sleep(0.5)
                except IndexError:
                    print("そんなコマンドはない！")
                    time.sleep(0.5)
            elif get == "2":
                subprocess.call("cls", shell=True)
                print("{}は{}を捨てた".format(player.name, player.item[5]))
                player.item.pop(5)
                break
            else:
                print("そんなコマンドはない")
        else:
            break

def useitem(player, enemy, item_name, item_number): #アイテムの使用
    global NKP, MKP
    if item_name == "スライムの粘液":
        nkp_select = random.randint(1, 5)
        time.sleep(0.5)
        print("{}は「スライムの粘液」を投げつけた".format(player.name))
        player.item.pop(item_number)
        if nkp_select <= 3:
            time.sleep(0.8)
            print("命中した！")
            time.sleep(0.5)
            print("{}はとても動きづらそうにしている".format(enemy.name))
            time.sleep(0.8)
            NKP += 1
        else:
            time.sleep(0.5)
            print("外してしまった…")
            time.sleep(0.8)
    elif item_name == "スライムゼリー":
        player.HealC += 1
        if player.HealC > 2:
            player.HealC = 2
        player.FireC += 1
        if player.FireC > 3:
            player.FireC = 3
        time.sleep(0.5)
        print("{}は「スライムゼリー」を使った".format(player.name))
        time.sleep(0.5)
        print("特技使用回数が回復した")
        time.sleep(0.8)
        player.item.pop(item_number)
    elif item_name == "ポーション":
        player.hp += 100
        if player.hp > player.max_hp:
            player.hp = player.max_hp
        time.sleep(0.5)
        print("{}は「ポーション」を使った".format(player.name))
        time.sleep(0.5)
        print("HPが回復した")
        time.sleep(0.8)
        player.item.pop(item_number)
    elif item_name == "古びた指輪":
        time.sleep(0.5)
        print("{}は「古びた指輪」を使った".format(player.name))
        time.sleep(0.5)
        print("しかし何も起こらなかった")
        time.sleep(0.8)
    elif item_name == "透明な液体":
        time.sleep(0.5)
        print("{}は「透明な液体」を使った".format(player.name))
        use_select = random.randint(1, 2)
        player.item.pop(item_number)
        if use_select == 1:
            player.hp -= 100
            time.sleep(0.5)
            print("苦い！毒が入っていたようだ…")
            time.sleep(0.5)
            print("{}はhpを100失った".format(player.name))
            time.sleep(0.8)
        else:
            time.sleep(0.8)
            print("{}の体は突然透明になった！".format(player.name))
            time.sleep(0.5)
            print("しばらくの間、敵に気付かれずに行動できそうだ")
            time.sleep(0.8)
            NKP += 3
    elif item_name == "透明な指輪":
        time.sleep(0.5)
        print("{}は「透明な指輪」を使った".format(player.name))
        time.sleep(0.5)
        print("しかし何も起こらなかった")
        time.sleep(0.8)
    elif item_name == "腐った指輪":
        time.sleep(0.5)
        print("{}は「腐った指輪」を使った".format(player.name))
        time.sleep(0.5)
        print("しかし何も起こらなかった")
        time.sleep(0.8)
    elif item_name == "死者の魂":
        time.sleep(0.5)
        print("{}は「死者の魂」を使った".format(player.name))
        time.sleep(0.5)
        print("しかし何も起こらなかった")
        time.sleep(0.8)
    elif item_name == "番犬のチョーカー":
        time.sleep(0.5)
        print("{}は「番犬のチョーカー」を使った".format(player.name))
        time.sleep(0.5)
        print("しかし何も起こらなかった")
        time.sleep(0.8)
    elif item_name == "キャンディー":
        time.sleep(0.5)
        print("{}は「キャンディー」を食べた".format(player.name))
        time.sleep(0.5)
        print("少しの間どんな攻撃にも耐えられそうだ")
        time.sleep(0.5)
        MKP += 2
        player.item.pop(item_number)
    elif item_name == "毒針":
        time.sleep(0.5)
        print("{}は{}に対して「毒針」を思い切り投げつけた！".format(player.name, enemy.name))
        doku = random.randint(1, 2)
        if doku <= 1:
            time.sleep(0.8)
            print("深く突き刺さった！")
            damage = 200
        else:
            time.sleep(0.5)
            print("……が、弾かれてしまった")
            damage = 1
        enemy.hp -= damage
        time.sleep(0.8)
        print("{}のダメージ".format(damage))
        time.sleep(0.8)
        player.item.pop(item_number)
    elif item_name == "鋼鉄の指輪":
        time.sleep(0.5)
        print("{}は「鋼鉄の指輪」を使った".format(player.name))
        time.sleep(0.5)
        print("しかし何も起こらなかった")
        time.sleep(0.8)
    elif item_name == "吸血の牙":
        time.sleep(0.5)
        print("{}は「吸血の牙」を使った".format(player.name))
        time.sleep(0.5)
        damage = int(player.attack * 1.3 + random.randint(-2, 2) - enemy.defence / 3)
        print("{}のダメージを与えた".format(damage))
        time.sleep(0.5)
        print("{}は{}回復した".format(player.name, damage))
        enemy.hp -= damage
        player.hp += damage
        if player.hp >= player.max_hp:
            player.hp = player.max_hp
        player.item.pop(item_number)
        time.sleep(0.8)
    elif item_name == "ヴァンパイアの血液":
        time.sleep(0.5)
        print("{}は「ヴァンパイアの血液」を使った".format(player.name))
        time.sleep(0.5)
        print("すべてのステータスが一時期的に大きく上昇した")
        time.sleep(0.8)
        player.attack += 20
        player.defence += 20
        player.speed += 20
        player.item.pop(item_number)
    elif item_name == "古代の秘宝":
        damage = 300
        handou = 100
        enemy.hp -= damage
        player.hp -= handou
        time.sleep(0.5)
        print("{}は「古代の秘宝」を使った".format(player.name))
        time.sleep(0.5)
        print("想像を絶する程の爆発が{}を襲う".format(enemy.name))
        time.sleep(1.0)
        print("{}に{}のダメージ".format(enemy.name, damage))
        time.sleep(0.5)
        print("{}は反動で{}のダメージをくらった".format(player.name, handou))
        time.sleep(0.8)
        player.item.pop(item_number)
    elif item_name == "英雄の証":
        global EP
        time.sleep(0.5)
        print("{}は「英雄の証」を使った".format(player.name))
        time.sleep(0.8)
        print("神々しい光が辺りを包み込む")
        time.sleep(0.8)
        print("なんと、hpが最大まで回復した")
        time.sleep(0.5)
        player.hp = player.max_hp
        EP -= 1
        if EP == 2:
            print("「英雄の証」に傷が入った")
        elif EP == 1:
            print("「英雄の証」の傷がかなり大きくなった")
        elif EP == 0:
            print("「英雄の証」は静かに崩れ落ちていった")
            player.item.pop(item_number)
        time.sleep(0.8)
    elif item_name == "伝説の宝玉":
        pass
def getItem(player, enemy):
    if enemy.name == "スライム":
        I = random.randint(1, 10)
        if I > 5:
            player.item += ["スライムの粘液"]
            print("なんと、スライムは「スライムの粘液」を落とした")
            time.sleep(0.5)
        elif I < 4:
            player.item += ["スライムゼリー"]
            print("なんと、スライムは「スライムゼリー」を落とした")
            time.sleep(0.5)
        itemClean(player)
    if enemy.name == "ゴブリン":
        I = random.randint(1, 10)
        if I > 5:
            player.item += ["ポーション"]
            print("なんと、ゴブリンは「ポーション」を落とした")
            time.sleep(0.5)
        elif I < 4:
            player.item += ["古びた指輪"]
            print("なんと、ゴブリンは「古びた指輪」を落とした")
            time.sleep(0.5)
        itemClean(player)
    if enemy.name == "ゴースト":
        I = random.randint(1, 10)
        if I > 5:
            player.item += ["透明な液体"]
            print("なんと、ゴーストは「透明な液体」を落とした")
            time.sleep(0.5)
        elif I < 4:
            player.item += ["透明な指輪"]
            print("なんと、ゴーストは「透明な指輪」を落とした")
            time.sleep(0.5)
        itemClean(player)
    if enemy.name == "ゾンビ":
        I = random.randint(1, 10)
        if I > 5:
            player.item += ["腐った指輪"]
            print("なんと、ゾンビは「腐った指輪」を落とした")
            time.sleep(0.5)
        elif I < 4:
            player.item += ["死者の魂"]
            print("なんと、ゾンビは「死者の魂」を落とした")
            time.sleep(0.5)
        itemClean(player)
    if enemy.name == "ケルベロス":
        I = random.randint(1, 10)
        if I > 5:
            player.item += ["番犬のチョーカー"]
            print("なんと、ケルベロスは「番犬のチョーカー」を落とした")
            time.sleep(0.5)
        elif I < 4:
            player.item += ["キャンディー"]
            print("なんと、ケルベロスは「キャンディー」を落とした")
            time.sleep(0.5)
        itemClean(player)
    if enemy.name == "スコーピオン":
        I = random.randint(1, 10)
        if I > 5:
            player.item += ["毒針"]
            print("なんと、スコーピオンは「毒針」を落とした")
            time.sleep(0.5)
        elif I < 4:
            player.item += ["鋼鉄の指輪"]
            print("なんと、スコーピオンは「鋼鉄の指輪」を落とした")
            time.sleep(0.5)
        itemClean(player)
    if enemy.name == "ヴァンパイア":
        I = random.randint(1, 10)
        if I > 3:
            player.item += ["吸血の牙"]
            print("なんと、ヴァンパイアは「吸血の牙」を落とした")
            time.sleep(0.5)
        elif I < 2:
            player.item += ["ヴァンパイアの血液"]
            print("なんと、ヴァンパイアは「ヴァンパイアの血液」を落とした")
            time.sleep(0.5)
        itemClean(player)
    if enemy.name == "ゴーレム":
        I = random.randint(1, 2)
        if I == 1:
            player.item += ["古代の秘宝"]
            print("なんと、ゴーレムは「古代の秘宝」を落とした")
            time.sleep(0.5)
        itemClean(player)
    if enemy.name == "ヒュドラ":
        global EP
        if "英雄の証" not in player.item:
            player.item += ["英雄の証"]
            print("なんと、ヒュドラは「英雄の証」を落とした")
            EP += 3
            time.sleep(0.5)
        itemClean(player)
    if enemy.name == "ドラゴン":
        if "伝説の宝玉" not in player.item:
            player.item += ["伝説の宝玉"]
            print("なんと、ドラゴンは「伝説の宝玉」を落とした")
            time.sleep(0.5)
        itemClean(player)

def usezomring(player):
    if "腐った指輪" in player.item:
        time.sleep(0.5)
        print("「腐った指輪」の効果でhpが15回復した\n")
        time.sleep(0.5)
        player.hp += 15
        if player.hp >= player.max_hp:
            player.hp = player.max_hp

def usezomsoul(player):
        time.sleep(0.8)
        print("なんと、{}は「死者の魂」の効果で復活した！".format(player.name))
        time.sleep(0.5)
        player.hp = int(player.max_hp / 2)
        count = 0
        while count < 5:
            if player.item[count] == "死者の魂":
                player.item.pop(count)
                break
            count += 1

# 戦闘に勝利
def battle_win(player, enemy):
    global KP, BP
    if enemy.name == "ヒュドラ":
        time.sleep(0.5)
        print("{}を倒した！".format(enemy.name))
        BP += 1
        time.sleep(0.8)
        if player.level <= enemy.level:
            KP += 2
            if KP % 2 == 0:
                player.level_up()
    else:
        time.sleep(0.5)
        print("{}を倒した！".format(enemy.name))
        BP += 1
        time.sleep(0.8)
        if player.level <= enemy.level:
            KP += 1
            if KP % 2 == 0:
                player.level_up()
    getItem(player, enemy)

# 敵の作成
enemies1 = [EnemySli("スライム", 30, 10, 10, 0, 1), EnemyGob("ゴブリン", 50, 20, 0, 5, 1)]
enemies2 = [Enemy("ゾンビ", 120, 50, 0, 0, 2), EnemyGho("ゴースト", 3, 35, 99, 99, 2)]
enemies3 = [EnemyKel("ケルベロス", 150, 70, 15, 15, 3), EnemySco("スコーピオン", 75, 80, 30, 15, 3)]
enemy4 = BOSSenemyVan("ヴァンパイア", 200, 80, 20, 10, 4)
enemy5 = BOSSenemyGol("ゴーレム", 120, 80, 20, 0, 4)
enemy6 = BOSSenemyHyu("ヒュドラ", 400, 100, 30, 40, 5)
enemy7 = BOSSenemyDor("ドラゴン", 800, 120, 40, 35, 6)
SPenemy = Enemy("死神", 9999, 999, 50, 70, 99)

if __name__ == "__main__":
    main()