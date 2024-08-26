"""
アイテム使用・説明追加
墓場・洞窟の敵の詳細書く
宝箱システム
"""

import random
import subprocess
import time
import sys

KP = 0 # 経験値
BP = 0 # ダンジョンの階層
SP = 0 # 死神の出現フラグ
MKP = 0 # 無敵時間
EP = 2 # 英雄の証
GOLD = 300 # ゴールド
game_type = False
player_str = {} # 自キャラのステータス一覧
enemy_str = {} # 敵キャラのステータス一覧
shop_weapon_list = [["ダガー", 30, 300], ["ロングソード", 70, 700], ["モーニングスター", 150, 1500]] # 装備一覧
shop_item_list = [["ポーション", 50], ["スライムゼリー", 80], ["聖印", 500]] # アイテム一覧
item_list = {} # アイテムの名前・説明・効果

# ゲームスタート
def main():
    global game_type
    subprocess.call("cls", shell=True)
    player_name = input("プレイヤーの名前を入力してください: ")
    if player_name == "Untot":
        player = Player_True(player_name, 900, 200, 100, 30, 10, 250, 1, 250, 3, 1, 0, 0, [], ["なし", 0, 0])
        game_type = True
    elif player_name == "ああああ":
        player = Player(player_name, 999, 9999, 9999, 99, 99, 999, 99, 999, 99, ["英雄の証", "透明な液体", "古代の秘宝", "古代の秘宝", "伝説の宝玉"], 0)
    elif player_name == "SUPER BOSS":
        player = Player(player_name, 400, 125, 55, 50, 6, 125, 5, 110, 5, ["英雄の証", "古代の秘宝", "古代の秘宝", "吸血の牙", "吸血の牙"], 0)
    else:
        player = Player(player_name, 100, 25, 5, 10, 1, 25, 2, 35, 2, [], 0)
    subprocess.call("cls", shell=True)
    if game_type:
        enemies = town(player)
        while True:
            if BP <= 0:
                enemy = enemies[0]
            elif BP == 1:
                enemy = enemies[1]
            elif BP == 2:
                enemy = enemies[2]
            elif BP == 3:
                enemy = enemies[3]

            battle_True(player, enemy)
            
            if player.hp <= 0:
                print("ゲームオーバー！")
                break
            if BP >= 4:
                player.SpecialC += 1
                time.sleep(0.5)
                print("\n{}の周りが明るい光に包み込まれる。".format(player.name))
                time.sleep(1.0)
                print("特技：神の加護の使用回数が1増加した。")
                time.sleep(1.0)
                print("気が付くと、目の前には見慣れた光景が広がっていた。\n")
                time.sleep(1.0)
                enemies = town(player)
            else:
                print("無事生き延びることが出来たようだ")
                while True:
                    select = input("どうする？ [1]先へ進む, [2]街に戻る, [3]アイテムを確認する >")
                    subprocess.call("cls", shell=True)
                    if select == "1":
                        time.sleep(0.5)
                        print("\n", "敵が現れた！")
                        break
                    elif select == "2":
                        enemies = town(player)
                        break
                    elif select == "3":
                        item_org(player)
                    else:
                        print("そんなコマンドはない！")
    else:
        home_start(player)
        enemies = create_enemies()
        # メインループ
        while True:
            if SP % 3 == 0 and SP != 0:
                enemy = enemies[7]
            else:
                if BP <= 1:
                    enemy = random.choice(enemies[0])
                elif BP <= 3: 
                    enemy = random.choice(enemies[1])
                elif BP <= 5:
                    enemy = random.choice(enemies[2])
                elif BP == 6:
                    enemy = enemies[3]
                elif BP == 7:
                    enemy = enemies[4]
                elif BP == 8:
                    enemy = enemies[5]
                elif BP == 9:
                    enemy = enemies[6]

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
                        item_org(player)
                    else:
                        print("そんなコマンドはない！")

# プレイヤー
class Player:
    def __init__(self, name, hp, attack, defence, speed, level, Heal, HealC, Fire, FireC, item, state):
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
        self.state = state
    
    def __str__(self):
        return "{}: {} / {}".format(self.name, self.hp, self.max_hp)
    
    def print_str(self):
        subprocess.call("cls", shell=True)
        time.sleep(0.5)
        print("レベル：{}".format(self.level))
        time.sleep(0.2)
        print("名前：{}".format(self.name))
        time.sleep(0.2)
        print("HP：{} / {}".format(self.hp, self.max_hp))
        time.sleep(0.2)
        print("攻撃力：{}".format(self.attack))
        time.sleep(0.2)
        print("防御力：{}".format(self.defence))
        time.sleep(0.2)
        print("素早さ：{}".format(self.speed))
        time.sleep(0.2)
        print("魔法攻撃力：{}".format(self.Fire))
        time.sleep(0.2)
        print("特技使用回数(ファイアー)：{}".format(self.FireC))
        time.sleep(0.2)
        print("魔法回復力：{}".format(self.Heal))
        time.sleep(0.2)
        print("特技使用回数(ヒール)：{}\n".format(self.HealC))
        time.sleep(0.2)

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
        self.attack_S += 20
        self.defence_S += 10
        self.speed_S += 8
        self.Heal += 20
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
        print("魔法攻撃力が上がった")
        time.sleep(0.5)
        print("魔法回復力が上がった")
        time.sleep(0.5)
        if self.level % 2 == 0:
            self.HealC_S += 1
            self.FireC_S += 1
            print("特技の使用回数が増えた")
            time.sleep(0.5)
class Player_True(Player):
    def __init__(self, name, hp, attack, defence, speed, level, Heal, HealC, Fire, FireC, PowerC, SpecialC, state, item, weapon):
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
        self.PowerC = PowerC
        self.PowerC_S = PowerC
        self.SpecialC = SpecialC
        self.state = state
        self.state_S = state
        self.item = item
        self.weapon = weapon
    
    def attack_enemy(self, enemy):
        crt1 = random.randint(1, 10)
        if self.state >= 1:
            self.state -= 1
            time.sleep(0.8)
            print("{}は動けない".format(self.name))
            time.sleep(0.5)
        elif crt1 >= 3:
            damage = self.attack + random.randint(-4, 4) - enemy.defence
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
    
    def attack_enemy_power(self, enemy):
        if self.state >= 1:
            self.state -= 1
            time.sleep(0.8)
            print("{}は動けない".format(self.name))
            time.sleep(0.5)
            return
        self.PowerC -= 1
        miss = random.randint(0, 5)
        print("{}は、洗練された動きから渾身の一撃を繰り出す…！".format(self.name))
        time.sleep(1.5)
        if miss == 0:
            print("外してしまった…")
            time.sleep(0.5)
        else:
            damage = int(self.attack * 3 + random.randint(-10, 10))
            enemy.hp -= damage
            print("クリティカル！")
            time.sleep(0.5)
            print("{}のダメージを与えた！".format(damage))
            time.sleep(0.5)

    def special(self):
        global MKP
        if self.state >= 1:
            self.state -= 1
            time.sleep(0.8)
            print("{}は動けない".format(self.name))
            time.sleep(0.5)
            return
        self.SpecialC -= 1
        self.hp = self.max_hp
        MKP += 2
        time.sleep(1.0)
        print("{}を、神々しい程の光が包み込む".format(self.name))
        time.sleep(0.5)
        print("その圧倒的な光は、みるみる内に{}の傷を塞いでいく".format(self.name))
        time.sleep(0.5)
        print("なんと、{}のHPが最大になった！".format(self.name))
        self.hp = self.max_hp
        time.sleep(0.5)
        print("さらに、{}は3ターンの間敵の攻撃を無効化する効果を得た！".format(self.name))
        time.sleep(0.8)

    def heal(self):
        if self.state >= 1:
            self.state -= 1
            time.sleep(0.8)
            print("{}は動けない".format(self.name))
            time.sleep(0.5)
            return
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
        if self.state >= 1:
            self.state -= 1
            time.sleep(0.8)
            print("{}は動けない".format(self.name))
            time.sleep(0.5)
            return
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

    def print_str(self):
        subprocess.call("cls", shell=True)
        time.sleep(0.5)
        print("レベル：{}".format(self.level))
        time.sleep(0.2)
        print("名前：{}".format(self.name))
        time.sleep(0.2)
        print("所持金：{} G".format(GOLD))
        time.sleep(0.2)
        print("武器：{}({})".format(self.weapon[0], self.weapon[1]))
        time.sleep(0.2)
        print("HP：{} / {}".format(self.hp, self.max_hp))
        time.sleep(0.2)
        print("攻撃力：{}".format(self.attack))
        time.sleep(0.2)
        print("防御力：{}".format(self.defence))
        time.sleep(0.2)
        print("素早さ：{}".format(self.speed))
        time.sleep(0.2)
        print("魔法攻撃力：{}".format(self.Fire))
        time.sleep(0.2)
        print("特技使用回数(ファイアー)：{}".format(self.FireC))
        time.sleep(0.2)
        print("魔法回復力：{}".format(self.Heal))
        time.sleep(0.2)
        print("特技使用回数(ヒール)：{}".format(self.HealC))
        time.sleep(0.2)
        print("特技使用回数(渾身の一撃)：{}".format(self.PowerC))
        time.sleep(0.2)
        print("特技使用回数(必殺)：{}\n".format(self.SpecialC))
        time.sleep(0.2)

# 敵キャラ
class Enemy:
    def __init__(self, name, hp, attack, defence, speed, level, item):
        self.name = name
        self.hp = hp
        self.max_hp = hp
        self.attack = attack
        self.defence = defence
        self.speed = speed
        self.level = level
        self.item = item
    
    def __str__(self):
        return "{}: {} / {}".format(self.name, self.hp, self.max_hp)
    
    def attack_player(self, player):
        global MKP
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
    
    def attack_player_miss(self, miss_attack):
        time.sleep(0.5)
        print("{}の攻撃！".format(self.name))
        time.sleep(0.5)
        print("しかし攻撃は当たらなかった")
        time.sleep(0.5)
        miss_attack -= 1
class Enemy_Sli(Enemy): # スライム
    def attack_player(self, player):
        global MKP
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
class Enemy_Gob(Enemy): # ゴブリン
    def __init__(self, name, hp, attack, defence, speed, level, item, portion):
        self.name = name
        self.hp = hp
        self.max_hp = hp
        self.attack = attack
        self.defence = defence
        self.speed = speed
        self.level = level
        self.item = item
        self.portion = portion
        self.portion_S = portion
    
    def attack_player(self, player):
        global MKP
        gobATT = random.randint(1, 4)
        if gobATT == 1 and self.hp < 20 and self.portion == 0:
            portion = random.randint(28, 31)
            print("{}はポーションを使った".format(self.name))
            time.sleep(0.8)
            print("{}回復した".format(portion))
            time.sleep(0.5)
            self.hp += portion
            self.portion += 1
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
class Enemy_Gho(Enemy): # ゴースト
    def attack_player(self, player):
        global MKP
        GH_attack = random.randint(1, 5)
        if GH_attack == 1 and len(player.item) >= 1:
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
class Enemy_Zom(Enemy): # ゾンビ
    def __init__(self, name, hp, attack, defence, speed, level, item, revival):
        self.name = name
        self.hp = hp
        self.max_hp = hp
        self.attack = attack
        self.defence = defence
        self.speed = speed
        self.level = level
        self.item = item
        self.revival = revival
        self.revival_S = revival
class Enemy_Sco(Enemy): # スコーピオン
    def attack_player(self, player):
        global MKP
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
class Enemy_Kel(Enemy): # ケルベロス
    def attack_player(self, player):
        global MKP
        T = random.randint(1, 5)
        if T <= 2:
            print("{}の「二連撃」".format(self.name))
            damage = 0
            for _ in range(2):
                damage2 = int(self.attack * 0.8 + random.randint(-2, 2) - player.defence / 2)
                if damage2 < 1:
                    damage2 = 1
                if MKP >= 1:
                    damage2 = 0
                time.sleep(0.8)
                print("{}のダメージをくらった！".format(damage2))
                damage += damage2
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
class Enemy_Van(Enemy): # ヴァンパイア
    def attack_player(self, player):
        global MKP
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
class Enemy_Gol(Enemy): # ゴーレム
    def __init__(self, name, hp, attack, defence, speed, level, item, evolution):
        self.name = name
        self.hp = hp
        self.max_hp = hp
        self.attack = attack
        self.defence = defence
        self.speed = speed
        self.level = level
        self.item = item
        self.evolution = evolution
        self.evolution_S = evolution

    def attack_player(self, player):
        global MKP
        T = random.randint(1, 5)
        if self.hp <= self.max_hp / 2 and self.evolution == 0:
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
            self.evolution += 1
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
class Enemy_Hyu(Enemy): # ヒュドラ
    def attack_player(self, player):
        global MKP
        T = random.randint(1, 5)
        if T <= 3 and self.hp < self.max_hp / 2:
            print("{}の「五連撃」".format(self.name))
            damage = 0
            for _ in range(5):
                damage5 = int(random.randint(30, 40) - player.defence / 10)
                if damage5 < 1:
                    damage5 = 1
                if MKP >= 1:
                    damage5 = 0
                time.sleep(0.8)
                print("{}のダメージをくらった！".format(damage5))
                damage += damage5
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
class BOSSEnemy_Dor(Enemy): # ドラゴン
    def __init__(self, name, hp, attack, defence, speed, level, item, attack_state):
        self.name = name
        self.hp = hp
        self.max_hp = hp
        self.attack = attack
        self.defence = defence
        self.speed = speed
        self.level = level
        self.item = item
        self.attack_state = attack_state

    def attack_player(self, player):
        global MKP
        T = random.randint(1, 5)
        if T <= 2 and self.hp < self.max_hp / 2:
            print("{}は灼熱の火炎を吐いた".format(self.name))
            damage = int(self.attack * 1.5 + random.randint(-15, 15))
            if MKP >= 1:
                damage = 0
            time.sleep(1.0)
            print("{}のダメージをくらった！".format(damage))
            self.attack_state = 0
        elif self.attack_state / 3 == 0:
            print("{}の「五連撃」".format(self.name))
            damage = 0
            for _ in range(5):
                damage5 = int(self.attack * 0.5 + random.randint(-2, 2) - player.defence / 2)
                if damage5 < 1:
                    damage5 = 1
                if MKP >= 1:
                    damage5 = 0
                time.sleep(0.8)
                print("{}のダメージをくらった！".format(damage5))
                damage += damage5
            self.attack_state += 1
        else:
            damage = int(self.attack + random.randint(-2, 2) - player.defence)
            if damage < 1:
                damage = 1
            if MKP >= 1:
                damage = 0
            print("{}の攻撃".format(self.name))
            time.sleep(0.8)
            print("{}のダメージをくらった！".format(damage))
            self.attack_state += 1
        player.hp -= damage
        time.sleep(0.5)
        if MKP >= 1:
            MKP -= 1
class BOSSEnemy_Death(Enemy): # 死神
    def attack_player(self, player):
        global MKP
        T = random.randint(1, 5)
        if T <= 1:
            if player.state == 0:
                print("{}の「死の刻印」".format(self.name))
                time.sleep(0.5)
                print("{}は死の刻印を体に刻まれてしまった".format(self.name))
                time.sleep(0.5)
                player.state = 1
                return
            elif player.state == 1:
                print("{}に刻まれていた死の刻印がその効果を発揮する…！")
                time.sleep(0.5)
                damage = 4444
                if MKP >= 1:
                    damage2 = 0
                print("{}のダメージをくらった！".format(int(damage)))
                player.state = 0
        elif T <= 2:
            self.attack *= 1.1
            self.defence *= 1.1
            self.hp += 100
            if self.hp > self.max_hp:
                self.hp = self.max_hp
            print("{}の「シャドウステップ」".format(self.name))
            time.sleep(0.8)
            print("{}の攻撃力が上昇した！".format(self.name))
            time.sleep(0.5)
            print("{}の防御力が上昇した！".format(self.name))
            time.sleep(0.5)
            print("{}のhpが回復した！".format(self.name))
            time.sleep(0.5)
            return
        else:
            print("{}の「連撃」".format((self.name)))
            damage = 0
            for _ in range(2):
                damage2 = int(self.attack * 0.6 + random.randint(-5, 5))
                if MKP >= 1:
                    damage2 = 0
                time.sleep(0.8)
                print("{}のダメージをくらった！".format(damage2))
                damage += damage2
        player.hp -= int(damage)
        time.sleep(0.8)
        if MKP >= 1:
            MKP -= 1
        
# 失意の館
class Enemy_True:
    def __init__(self, name, hp, attack, defence, speed, level, item, gold):
        self.name = name
        self.hp = hp
        self.max_hp = hp
        self.attack = attack
        self.defence = defence
        self.speed = speed
        self.level = level
        self.item = item
        self.gold = gold
    
    def __str__(self):
        return "{}: {} / {}".format(self.name, self.hp, self.max_hp)
    
    def attack_player_miss(self, miss_attack):
        time.sleep(0.5)
        print("{}の攻撃！".format(self.name))
        time.sleep(0.5)
        print("しかし攻撃は当たらなかった")
        time.sleep(0.5)
        miss_attack -= 1
class Enemy_Night(Enemy_True): # ナイトメア
    def attack_player(self, player):
        global MKP
        SA = random.randint(1, 5)
        if SA <= 3:
            print("{}の「悪夢の一撃」".format(self.name))
            damage = self.attack * 0.7 + random.randint(-2, 2) - player.defence / 2
            time.sleep(0.5)
            print("{}のダメージをくらった！".format(int(damage)))
            if damage < 1:
                damage = 1
            if MKP >= 1:
                damage = 0
            time.sleep(0.8)
            if random.randint(0, 2) == 1 and "聖印" not in player.item:
                player.state += 1
                print("{}は恐怖で足がすくんでしまった".format(player.name))
        else:
            damage = self.attack + random.randint(-2, 2) - player.defence
            if damage < 1:
                damage = 1
            if MKP >= 1:
                damage = 0
            print("{}の攻撃".format(self.name))
            time.sleep(0.5)
            print("{}のダメージをくらった！".format(int(damage)))
        time.sleep(0.5)
        player.hp -= int(damage)
        if MKP >= 1:
            MKP -= 1
class Enemy_Mar(Enemy_True): # マリオネット
    def attack_player(self, player):
        global MKP
        SA = random.randint(1, 5)
        if SA <= 2:
            print("{}の「剣の舞」".format(self.name))
            self.attack *= 2
            time.sleep(0.5)
            print("{}の攻撃力が大幅に上昇した".format(self.name))
            time.sleep(0.5)
            return
        elif SA <= 3:
            print("{}の「鎌の舞」".format(self.name))
            damage = 0
            for _ in range(3):
                damage3 = int(self.attack * 0.7 + random.randint(-2, 2) - player.defence / 2)
                if damage3 < 1:
                    damage3 = 1
                if MKP >= 1:
                    damage3 = 0
                time.sleep(0.8)
                print("{}のダメージをくらった！".format(damage3))
                damage += damage3
        
        else:
            damage = self.attack + random.randint(-2, 2) - player.defence
            if damage < 1:
                damage = 1
            if MKP >= 1:
                damage = 0
            print("{}の攻撃".format(self.name))
            time.sleep(0.5)
            print("{}のダメージをくらった！".format(int(damage)))
        time.sleep(0.5)
        player.hp -= int(damage)
        if MKP >= 1:
            MKP -= 1
class Enemy_DeaPer(Enemy_True): # デスペラード
    def attack_player(self, player):
        global MKP
        SA = random.randint(1, 5)
        if SA <= 1:
            print("{}の「死の弾丸」".format(self.name))
            damage = player.hp * 0.5
            if MKP >= 1:
                damage = 0
            time.sleep(0.5)
        elif SA <= 3:
            print("{}の「業火の弾丸」".format(self.name))
            damage = player.max_hp * 0.3 + random.randint(-5, 5)
            if MKP >= 1:
                damage = 0
            time.sleep(0.5)
        else:
            damage = self.attack + random.randint(-2, 2) - player.defence
            if damage < 1:
                damage = 1
            if MKP >= 1:
                damage = 0
            print("{}の攻撃".format(self.name))
            time.sleep(0.5)
        print("{}のダメージをくらった！".format(int(damage)))
        time.sleep(0.5)
        player.hp -= int(damage)
        if MKP >= 1:
            MKP -= 1
class BOSSEnemy_Witch(Enemy_True): # 失意の魔女
    def attack_player(self, player):
        global MKP
        SA = random.randint(1, 5)
        if SA <= 2:
            print("{}の「絶望の呪詛」".format(self.name))
            damage = 0
            state = False
            for _ in range(3):
                damage3 = int(self.attack * 0.7 + random.randint(-2, 2) - player.defence / 2)
                if damage3 < 1:
                    damage3 = 1
                if MKP >= 1:
                    damage3 = 0
                time.sleep(0.8)
                print("{}のダメージをくらった！".format(damage3))
                damage += damage3
                if random.randint(0, 9) == 1:
                    state = True
            if state and "聖印" not in player.item:
                player.state += 1
                time.sleep(0.5)
                print("{}は恐怖で足がすくんでしまった".format(player.name))
        elif SA <= 3:
            print("{}の「悲劇の霧」".format(self.name))
            player.attack *= 0.9
            player.defence *= 0.9
            time.sleep(0.5)
            print("{}の攻撃力が減少してしまった".format(player.name))
            time.sleep(0.5)
            print("{}の防御力が減少してしまった".format(player.name))
            time.sleep(0.8)
            if random.randint(0, 3) == 1 and "聖印" not in player.item:
                player.state += 1
                print("{}は恐怖で足がすくんでしまった".format(player.name))
                time.sleep(0.5)
            return
        else:
            damage = self.attack + random.randint(-2, 2) - player.defence
            if damage < 1:
                damage = 1
            if MKP >= 1:
                damage = 0
            print("{}の攻撃".format(self.name))
            time.sleep(0.5)
            print("{}のダメージをくらった！".format(int(damage)))
        time.sleep(0.5)
        player.hp -= int(damage)
        if MKP >= 1:
            MKP -= 1

# 絶望の墓場
class Enemy_DarGho(Enemy_True):  # ダークゴースト
    def attack_player(self, player):
        print("{}の「呪いの叫び」".format(self.name))
        player.attack *= 0.9
        time.sleep(0.5)
        print("{}の攻撃力が減少した".format(player.name))
class Enemy_GriZom(Enemy_True):  # グリムゾンビ
    def attack_player(self, player):
        print("{}の攻撃".format(self.name))
        damage = self.attack + random.randint(-2, 2) - player.defence
        if damage < 1:
            damage = 1
        print("{}のダメージをくらった！".format(int(damage)))
        time.sleep(0.5)
        player.hp -= int(damage)
        self.hp += 20
        print("{}はHPを20回復した".format(self.name))
class Enemy_DeaHou(Enemy_True):  # デスハウンド
    def attack_player(self, player):
        print("{}の「暗黒の噛みつき」".format(self.name))
        damage = self.attack + random.randint(-2, 2) - player.defence
        if damage < 1:
            damage = 1
        time.sleep(0.5)
        player.hp -= int(damage)
        print("{}のダメージをくらった！".format(int(damage)))
        if random.randint(1, 5) == 1:
            player.state += 1
            print("{}は毒状態になった！".format(player.name))
class BOSSEnemy_VanLor(Enemy_True):  # ヴァンパイアロード
    def attack_player(self, player):
        global MKP
        if MKP >= 1:
            damage = 0
        else:
            damage = self.attack + random.randint(-2, 2) - player.defence
            if damage < 1:
                damage = 1
        print("{}の「骨の盾」".format(self.name))
        time.sleep(0.5)
        print("{}のダメージを半減する".format(self.name))
        time.sleep(0.5)
        player.hp -= int(damage)

# 終焉の洞窟
class Enemy_InfeSli(Enemy_True):  # インフェルノスライム
    def attack_player(self, player):
        print("{}の「亡者の剣」".format(self.name))
        damage = self.attack + random.randint(-2, 2) - player.defence
        if damage < 1:
            damage = 1
        print("{}のダメージをくらった！".format(int(damage)))
        player.hp -= int(damage)
        self.hp += int(damage * 0.1)
        print("{}はHPを回復した".format(self.name))
class Enemy_HighGob(Enemy_True):  # ハイゴブリン
    def attack_player(self, player):
        print("{}の「暗黒魔法」".format(self.name))
        damage = self.attack + random.randint(-2, 2) - player.defence
        if damage < 1:
            damage = 1
        time.sleep(0.5)
        print("{}のダメージをくらった！".format(int(damage)))
        player.hp -= int(damage)
        if random.randint(1, 3) == 1:
            player.state += 1
            print("{}は麻痺状態になった！".format(player.name))
class Enemy_ObsidianGol(Enemy_True):  # オブシディアンゴーレム
    def __init__(self, name, hp, attack, defence, speed, level, item, gold, evolution):
        self.name = name
        self.hp = hp
        self.max_hp = hp
        self.attack = attack
        self.defence = defence
        self.speed = speed
        self.level = level
        self.item = item
        self.gold = gold
        self.evolution = evolution
        self.evolution_S = evolution

    def attack_player(self, player):
        global MKP
        T = random.randint(1, 5)
        if self.hp <= self.max_hp / 2 and self.evolution == 0:
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
            self.evolution += 1
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
class BOSSEnemy_ShadowDra(Enemy_True):  # シャドウドラゴン
    def attack_player(self, player):
        print("{}の「闇のブレス」".format(self.name))
        damage = self.attack + random.randint(-2, 2) - player.defence
        if damage < 1:
            damage = 1
        print("全体攻撃を行った！")
        time.sleep(0.5)
        player.hp -= int(damage)
        print("{}のダメージをくらった！".format(int(damage)))
        if random.randint(1, 2) == 1:
            print("{}の視界が奪われた！命中率が下がる".format(player.name))

# 戦闘
def battle(player, enemy):
    global MKP
    MKP = 0
    miss_attack = 0
    enemy.hp = enemy.max_hp
    if enemy.name == "ゾンビ":
        enemy.revival = enemy.revival_S
    elif enemy.name == "ゴーレム":
        enemy.evolution = enemy.evolution_S
    elif enemy.name == "ゴブリン":
        enemy.portion = enemy.portion_S
    player.speed = player.speed_S
    player.attack = player.attack_S
    player.defence = player.defence_S
    player.HealC = player.HealC_S
    player.FireC = player.FireC_S
    if "透明な指輪" in player.item:
        player.speed += 50
    if "古びた指輪" in player.item:
        player.attack += 15
    if "鋼鉄の指輪" in player.item:
        player.defence += 10
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
                    if miss_attack >= 1:
                        enemy.attack_player_miss(miss_attack)
                    else:
                        enemy.attack_player(player)
                    zomring_use(player)
            elif player.speed < enemyS:
                if miss_attack >= 1:
                    enemy.attack_player_miss(miss_attack)
                else:
                    enemy.attack_player(player)
                if player.hp > 0:
                    player.attack_enemy(enemy)
                    zomring_use(player)
        elif command == "s":
            while True:
                print(player)
                print(enemy)
                print("どうする？ [h]ヒール({}), [f]ファイア({})".format(player.HealC, player.FireC))
                print("※ スペースキーで戻る")
                command_next = input("> ")
                subprocess.call("cls", shell=True)
                if command_next == "h":
                    if player.HealC <= 0:
                        print("もう回復呪文は使えない！")
                    else:
                        player.heal()
                        if miss_attack >= 1:
                            enemy.attack_player_miss(miss_attack)
                        else:
                            enemy.attack_player(player)
                        zomring_use(player)
                        break
                elif command_next == "f":
                    if player.FireC <= 0:
                        print("もう攻撃魔法は使えない！")
                    else:
                        player.fire(enemy)
                        if enemy.hp > 0:
                            if miss_attack >= 1:
                                enemy.attack_player_miss(miss_attack)
                            else:
                                enemy.attack_player(player)
                        zomring_use(player)
                        break
                elif command_next == " ":
                    break
                else:
                    print("そんなコマンドはない！")
                    time.sleep(0.5)
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
                        item_use(player, enemy, player.item[int(select) - 1], int(select) - 1, miss_attack)
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
        elif command == "r":
            R = random.randint(1, 10)
            if  R >= 6:
                print("{}は逃げ出した".format(player.name))
                time.sleep(1.0)
                break
            else:
                print("逃げられなかった")
                time.sleep(0.8)
                if miss_attack >= 1:
                    enemy.attack_player_miss(miss_attack)
                else:
                    enemy.attack_player(player)
                zomring_use(player)
        else:
            print("そんなコマンドはない！")
        if defeat_enemy(player, enemy):
            break
        if defeat_player(player):
            break
def battle_True(player, enemy):
    global MKP
    miss_attack = 0
    MKP = 0
    enemy.hp = enemy.max_hp
    player.speed = player.speed_S
    player.attack = player.attack_S + player.weapon[1]
    player.defence = player.defence_S
    player.HealC = player.HealC_S
    player.FireC = player.FireC_S
    player.PowerC = player.PowerC_S
    if "透明な指輪" in player.item:
        player.speed += 20
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
                    if miss_attack >= 1:
                        enemy.attack_player_miss(miss_attack)
                    else:
                        enemy.attack_player(player)
            elif player.speed < enemyS:
                if miss_attack >= 1:
                    enemy.attack_player_miss(miss_attack)
                else:
                    enemy.attack_player(player)
                if player.hp > 0:
                    player.attack_enemy(enemy)
        elif command == "s":
            while True:
                print(player)
                print(enemy)
                print("どうする？ [a]渾身の一撃({}), [s]天の加護({}) [h]ヒール({}), [f]ファイア({})".format(player.PowerC, player.SpecialC, player.HealC, player.FireC))
                print("※ スペースキーで戻る")
                command_next = input("> ")
                subprocess.call("cls", shell=True)
                if command_next == "a":
                    if player.PowerC <= 0:
                        print("もう渾身の一撃は使えない！")
                    else:
                        player.attack_enemy_power(enemy)
                        if enemy.hp > 0:
                            if miss_attack >= 1:
                                enemy.attack_player_miss(miss_attack)
                            else:
                                enemy.attack_player(player)
                        break
                elif command_next == "s":
                    if player.SpecialC <= 0:
                        print("今は天の加護を使えない！")
                    else:
                        player.special()
                        if miss_attack >= 1:
                            enemy.attack_player_miss(miss_attack)
                        else:
                            enemy.attack_player(player)
                        break
                elif command_next == "h":
                    if player.HealC <= 0:
                        print("もう回復呪文は使えない！")
                    else:
                        player.heal()
                        if miss_attack >= 1:
                            enemy.attack_player_miss(miss_attack)
                        else:
                            enemy.attack_player(player)
                        break
                elif command_next == "f":
                    if player.FireC <= 0:
                        print("もう攻撃魔法は使えない！")
                    else:
                        player.fire(enemy)
                        if enemy.hp > 0:
                            if miss_attack >= 1:
                                enemy.attack_player_miss(miss_attack)
                            else:
                                enemy.attack_player(player)
                        break
                elif command_next == " ":
                    break
                else:
                    print("そんなコマンドはない！")
                    time.sleep(0.5)
        elif command == "i":
            if player.state >= 1:
                time.sleep(0.5)
                print("今はアイテムを使えなさそうだ…\n")
                continue
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
                        item_use(player, enemy, player.item[int(select) - 1], int(select) - 1, miss_attack)
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
        elif command == "r":
            R = random.randint(1, 10)
            if  R >= 6:
                print("{}は逃げ出した".format(player.name))
                time.sleep(1.0)
                break
            else:
                print("逃げられなかった")
                time.sleep(0.8)
                if miss_attack >= 1:
                    enemy.attack_player_miss(miss_attack)
                else:
                    enemy.attack_player(player)
        else:
            print("そんなコマンドはない！")
        if defeat_enemy(player, enemy):
            break
        if defeat_player(player):
            break
def battle_win(player, enemy):
    global KP, BP, GOLD
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
        if game_type:
            time.sleep(0.5)
            print("{} Gを得た".format(enemy.gold))
            GOLD += enemy.gold
        BP += 1
        time.sleep(0.8)
        if player.level <= enemy.level:
            KP += 1
            if KP % 2 == 0:
                player.level_up()
    item_get(player, enemy)
def defeat_enemy(player, enemy):
    if enemy.hp <= 0:
        if enemy.name == "ゾンビ":
            f = random.randint(1, 5)
            if f <= 4 and enemy.revival >= 1:
                print("{}を倒した！".format(enemy.name))
                time.sleep(1.0)
                print("なんと！{}は復活した！！".format(enemy.name))
                time.sleep(0.5)
                enemy.hp = int(enemy.max_hp / 2)
                enemy.revival -= 1
            else:
                battle_win(player, enemy)
                return True
        else:
            battle_win(player, enemy)
            return True
    return False
def defeat_player(player):
    if player.hp <= 0 and "死者の魂" not in player.item:
        time.sleep(0.5)
        print("{}は死んでしまった...".format(player.name))
        return True
    elif player.hp <= 0 and "死者の魂" in player.item:
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
    return False

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
        select = input("どうする？ [1]ダンジョンに挑む, [2]アイテムを確認する, [3]ステータスを確認する >")
        if select == "1":
            SP += 1
            subprocess.call("cls", shell=True)
            time.sleep(0.5)
            print("\n", "敵が現れた！")
            break
        elif select == "2":
            item_org(player)
        elif select == "3":
            player.print_str()
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
            item_org(player)
        elif select == "3":
            player.print_str()
        elif select == "99":
            kinds = int(input("敵の種類を入力して下さい [0 or 1] >"))
            floor = int(input("階層を入力して下さい [0 ~ 7] >"))
            if kinds == 0:
                enemy = create_enemies()[floor]
            elif kinds == 1:
                dungeon = int(input("ダンジョンの種類を選択してください [0 ~ 2]"))
                enemy = create_enemies_True(dungeon)[floor]
            subprocess.call("cls", shell=True)
            battle(player, enemy)
            sys.exit()
        else:
            print("そんなコマンドはない！")

# アイテムの整理・追加・使用
def item_org(player): # アイテムの確認
    while True:
        subprocess.call("cls", shell=True)
        print("どれを確認する？", end="")
        for i, j in enumerate(player.item):
            index = int(i)
            print("[{}]{}, ".format(index + 1, j), end="")
        print("\n", "※ スペースキーで戻る")
        select = input("> ")
        subprocess.call("cls", shell=True)
        try:
            if 0 <= int(select) - 1 and int(select) - 1 <= 4:
                item_display(player.item[int(select) - 1])
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
def item_display(item_name): # アイテムの説明表示
    print("「{}」".format(item_name))
    time.sleep(0.5)
    if item_name == "スライムの粘液":
        print("透明で不気味な光を放つネバネバとした液体で、触れる者に寒気を走らせる。")
        print("※ 使用時、命中した敵は1ターン行動不能\n")
    elif item_name == "スライムゼリー":
        print("スライムから得られる半固形の物質。")
        print("緑と紫を混ぜたようなの色合いで謎めいた輝きを放っており、妙に神秘的な印象を受ける。")
        print("※ 使用時、特技使用回数回復\n")
    elif item_name == "ポーション":
        print("消耗した冒険者の肉体と魂を癒し、再生させる能力を持っている。")
        print("乱用すると狂気に陥る危険が伴うと言われているが、その真偽は定かではない。")
        print("※ 使用時、hpを100回復\n")
    elif item_name == "古びた指輪":
        print("長い年月を経て錆びついた鉄製の指輪。")
        print("着用者の筋力を僅かに上昇させる効果があるようだが、本来の力を発揮出来ていないようだ。")
        print("※ 所持時、攻撃力が10上昇\n")
    elif item_name == "透明な液体":
        print("透明だが不可解な輝きを放っており、粘性もあるため目を凝らせば視認出来る。")
        print("毒性を兼ね備えているが、自らを透明化出来るという魔力に誘われた服用者が後を絶たない。")
        print("※ 使用時、自分に100ダメージ又は3ターン攻撃無効化\n")
    elif item_name == "透明な指輪":
        print("特殊な素材で構成されており、実際に手で触れることによってその存在を認知できる。")
        print("着用者の俊敏性は、ゴーストに勝るとも劣らない。")
        print("※ 所持時、素早さが50上昇\n")
    elif item_name == "腐った指輪":
        print("これを手に入れたあなたは、その見た目よりも先に強烈な悪臭に顔をしかめることになるだろう。")
        print("今にも崩れ落ちてしまいそうな程朽ちているが、反面、強力な生命力を感じる。")
        print("※ 所持時、毎ターン終了時hpを15回復\n")
    elif item_name == "死者の魂":
        print("宝石の如く美しい白色の玉。")
        print("淡い輝きを放っているそれは、あなたが窮地に陥ったとき必ず役に立つだろう。")
        print("※ 死亡時に自動的に使用、最大hpの半分で復活\n")
    elif item_name == "番犬のチョーカー":
        print("一見すると何処にでも売っていそうな印象を受けるチョーカー。")
        print("その実、集中力を高める効果があるといわれており、間一髪で命拾いすることもあるだろう。")
        print("※ 所持時、クリティカル率が上昇\n")
    elif item_name == "キャンディー":
        print("およそ人々に恐れられる番犬が食べているとは思えない程に普通のキャンディー。")
        print("もしかしたら何か特別な効果があるのかもしれないが、食べてみないことには分からない。")
        print("※ 使用時、2ターンの間攻撃を無効化\n")
    elif item_name == "毒針":
        print("スコーピオンから取れる尻尾で先端には鋭い針がある。")
        print("別名、ワンショットポイズンとも呼ばれており刺されたものは致命的なダメージを受ける。")
        print("※ 使用時、敵に1ダメージ又は大ダメージ\n")
    elif item_name == "鋼鉄の指輪":
        print("はるか昔に高貴な女性がつけていた美しい指輪。")
        print("その女性が亡くなって以降その指輪には守護の力が宿ったと言う伝説が残された。")
        print("しかし現在所在が分からず詳細を知る者は誰も居ない。")
        print("※ 所持時、防御力が10上昇\n")
    elif item_name == "吸血の牙":
        print("ヴァンパイアが持つ背筋が凍るほどに鋭利な牙。")
        print("刺されれば生命力を吸い取られてしまうであろうそれは刺突武器として使えそうだが、耐久力は高くないようだ。")
        print("※ 使用時、敵にダメージ＆回復\n")
    elif item_name == "ヴァンパイアの血液":
        print("赤黒く濁っているドロドロの血液。")
        print("一時的にヴァンパイア並の身体能力を得ることが出来ると言われているが、その副作用は明らかになっていない。")
        print("※ 使用時、すべてのステータスが一時的に上昇\n")
    elif item_name == "古代の秘宝":
        print("ゴーレムの動力源となっているコアの中でも、特に良質なもの。")
        print("無尽蔵のエネルギーに満ちており、もし手にしたものが現れたならこれをめぐる争いは避けられないだろう。")
        print("※ 使用時、敵味方に極大ダメージ\n")
    elif item_name == "英雄の証":
        print("英雄ーーー")
        print("時代によってその呼称や定義に多少の違いはあれど、そう呼ばれる者たちは決まって生物としての領域を逸脱していた。")
        print("曰く、「彼ら」は人間ではない")
        print("曰く、その力は王国をも脅かす")
        print("その真意は不明だが、忌み嫌われる存在として語り継がれている。")
        print("※ 使用時、hpを最大まで回復\n")
    elif item_name == "伝説の宝玉":
        print("縲御ｼ晁ｪｬ縺ｮ螳晉脂縲")
        print("菴ｿ逕ｨ縺励※縺ｯ縺?￠縺ｪ縺\n")
    elif item_name == "聖印":
        print("精巧な装飾が施された美しい紋章")
        print("その素材が貴重であるが故に、教会の中でも高位の聖女しか扱うことを許されていない")
        print("※ 所持時、恐怖耐性を得る")
    elif item_name == "悪夢の残滓":
        print("")
        print("")
        print("")
    elif item_name == "木製の心臓":
        print("")
        print("")
        print("")
    elif item_name == "鉄の手枷":
        print("")
        print("")
        print("")
    elif item_name == "虚無の仮面":
        print("")
        print("")
        print("")
    elif item_name == "亡霊の灯火":
        print("")
        print("")
        print("")
    elif item_name == "腐食の牙":
        print("")
        print("")
        print("")
    elif item_name == "黄泉の心石":
        print("")
        print("")
        print("")
    elif item_name == "不死者の眼球":
        print("")
        print("")
        print("")
    elif item_name == "灼熱の核":
        print("")
        print("")
        print("")
    elif item_name == "略奪者の袋":
        print("")
        print("")
        print("")
    elif item_name == "黒曜石の魂":
        print("")
        print("")
        print("")
    elif item_name == "支配者の証":
        print("")
        print("")
        print("")
    time.sleep(0.5)
def item_check(player): # アイテムの所持数確認
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
                        print("{}は「{}」を捨てた".format(player.name, player.item[int(select) - 1]))
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
                print("{}は「{}」を捨てた".format(player.name, player.item[5]))
                player.item.pop(5)
                break
            else:
                print("そんなコマンドはない")
        else:
            break
def item_use(player, enemy, item_name, item_number, miss_attack): #アイテムの使用
    global MKP
    if item_name in ["古びた指輪", "透明な指輪", "腐った指輪", "死者の魂", "番犬のチョーカー", "鋼鉄の指輪", "聖印", "木製の心臓", "鉄の手枷"]:
        time.sleep(0.5)
        print("{}は「{}」を使った".format(player.name, item_name))
        time.sleep(0.5)
        print("しかし何も起こらなかった")
        time.sleep(0.8)
    elif item_name == "スライムの粘液":
        miss_select = random.randint(1, 5)
        time.sleep(0.5)
        print("{}は「スライムの粘液」を投げつけた".format(player.name))
        player.item.pop(item_number)
        if miss_select <= 3:
            time.sleep(0.8)
            print("命中した！")
            time.sleep(0.5)
            print("{}はとても動きづらそうにしている".format(enemy.name))
            time.sleep(0.8)
            miss_attack += 1
        else:
            time.sleep(0.5)
            print("外してしまった…")
            time.sleep(0.8)
    elif item_name == "スライムゼリー":
        player.HealC += 1
        if player.HealC > player.HealC_S:
            player.HealC = player.HealC_S
        player.FireC += 1
        if player.FireC > player.HealC_S:
            player.FireC = player.HealC_S
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
            miss_attack += 3
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
        doku = random.randint(1, 3)
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
        if EP == 2:
            print("「英雄の証」に大きな傷が入ってしまった")
        elif EP <= 1:
            print("「英雄の証」は静かに崩れ落ちていった")
            player.item.pop(item_number)
        EP -= 1
        time.sleep(0.8)
    elif item_name == "伝説の宝玉":
        subprocess.call("cls", shell=True)
        time.sleep(2.0)
        message = [ [0.1, "意図しないアイテムの使用が確認されました。\n"], \
                    [1.0, "\n"], \
                    [0.1, "使用者の特定を開始します。"], \
                    [0.25, "3...2...1..."], \
                    [2.0, "\n"], \
                    [0.1,  "失敗。\n"], \
                    [0.1, "\nゲームの強制的な初期化を試みます。"], \
                    [0.25, "3...2...1..."], \
                    [1.0, "\n"], \
                    [0.1,  "成功。\n\n"] ]
        for i in range(len(message)):
            print_time(message[i][0], message[i][1])
        time.sleep(1.0)
        print("\033[31m'Held name = Untot'\033[0m")
        sys.exit()
    elif item_name == "悪夢の残滓":
        time.sleep(0.5)
        print("{}は{}を使った".format(player.name, item_name))
        time.sleep(0.5)
        print("霧状のそれは、{}の周囲に纏わりついた".format(enemy.name))
        time.sleep(0.5)
        miss_attack += 1
        print("{}は恐怖で足がすくんでいる".format(enemy.name))
        time.sleep(0.8)
        player.item.pop(item_number)
    elif item_name == "虚無の仮面":
        pass

def item_passive_check(player):
    if "鉄の手枷" in player.item:
        player.attack += 30
        player.defence -= 30

def item_get(player, enemy): # アイテムの入手
    global EP
    random_number_item = random.randint(1, 10)
    item_type = enemy.item[0]
    if item_type == 0:
        if random_number_item > 4:
            player.item += [enemy.item[1]]
            print("なんと、{}は「{}」を落とした".format(enemy.name, enemy.item[1]))
        elif random_number_item < 3:
            player.item += [enemy.item[2]]
            print("なんと、{}は「{}」を落とした".format(enemy.name, enemy.item[2]))
    elif item_type == 1:
        if random_number_item >= 6:
            player.item += [enemy.item[1]]
            print("なんと、{}は「{}」を落とした".format(enemy.name, enemy.item[1]))
    elif item_type == 2:
        if enemy.item[1] not in player.item:
            player.item += [enemy.item[1]]
            print("なんと、{}は「{}」を落とした".format(enemy.name, enemy.item[1]))
            EP = 2
    elif item_type == 3:
        if enemy.item[1] not in player.item:
            player.item += [enemy.item[1]]
            print("なんと、{}は「{}」を落とした".format(enemy.name, enemy.item[1]))
    time.sleep(0.5)
    item_check(player)
def zomring_use(player): # 腐った指輪用の処理
    if "腐った指輪" in player.item:
        time.sleep(0.5)
        print("「腐った指輪」の効果でhpが15回復した\n")
        time.sleep(0.5)
        player.hp += 15
        if player.hp >= player.max_hp:
            player.hp = player.max_hp

# 一文字ずつ表示
def print_time(dis, str):
    leng = len(str)
    for i in range(leng):
        print(str[i], end="", flush=True)
        time.sleep(dis)

# 敵の作成
def create_enemies():
    enemies = [
        [
            Enemy_Sli("スライム", 30, 10, 10, 0, 1, [0, "スライムの粘液", "スライムゼリー"]),
            Enemy_Gob("ゴブリン", 50, 20, 0, 5, 1, [0, "古びた指輪", "ポーション"], 0),
        ],
        [
            Enemy_Zom("ゾンビ", 120, 50, 0, 0, 2, [0, "腐った指輪", "死者の魂"], 1),
            Enemy_Gho("ゴースト", 3, 35, 99, 99, 2, [0, "透明な指輪", "透明な液体"]),
        ],
        [
            Enemy_Kel("ケルベロス", 150, 70, 15, 15, 3, [0, "番犬のチョーカー", "キャンディー"]),
            Enemy_Sco("スコーピオン", 75, 80, 30, 15, 3, [0, "毒針", "鋼鉄の指輪"]),
        ],
        Enemy_Van("ヴァンパイア", 200, 80, 20, 10, 4, [0, "吸血の牙", "ヴァンパイアの血液"]),
        Enemy_Gol("ゴーレム", 120, 80, 20, 0, 4, [1, "古代の秘宝"], 0),
        Enemy_Hyu("ヒュドラ", 400, 100, 30, 40, 5, [2, "英雄の証"]),
        BOSSEnemy_Dor("ドラゴン", 800, 120, 40, 35, 6, [3, "伝説の宝玉"], 0),
        BOSSEnemy_Death("死神", 999, 70, 40, 70, 99, [3, "伝説の宝玉"]),
    ]
    return enemies
def create_enemies_True(type):
    enemies = ""
    if type == 1:
        enemies = [
            Enemy_Night("ナイトメア", 500, 200, 50, 30, 5, [1, "悪夢の残滓"], 75),
            Enemy_Mar("マリオネット", 700, 130, 50, 0, 5, [1, "木製の心臓"], 100),
            Enemy_DeaPer("デスペラード", 700, 1, 100, 40, 5, [1, "鉄の手枷"], 150),
            BOSSEnemy_Witch("失意の魔女", 1200, 220, 70, 10, 5, [1, "虚無の仮面"], 500),
        ]
    elif type == 2:
        enemies = [
            Enemy_DarGho("ダークゴースト", 500, 200, 50, 30, 5, [1, "亡霊の灯火"], 75),
            Enemy_GriZom("グリムゾンビ", 700, 130, 50, 0, 5, [1, "腐食の牙"], 100),
            Enemy_DeaHou("デスハウンド", 700, 1, 100, 40, 5, [1, "黄泉の心石"], 150),
            BOSSEnemy_VanLor("ヴァンパイアロード", 1200, 220, 70, 10, 5, [1, "不死者の眼球"], 500),
        ]
    elif type == 3:
        enemies = [
            Enemy_InfeSli("インフェルノスライム", 500, 200, 50, 30, 5, [1, "灼熱の核"], 75),
            Enemy_HighGob("ハイゴブリン", 700, 130, 50, 0, 5, [1, "略奪者の袋"], 100),
            Enemy_ObsidianGol("オブシディアンゴーレム", 700, 1, 100, 40, 5, [1, "黒曜石の魂"], 150, 0),
            BOSSEnemy_ShadowDra("シャドウドラゴン", 1200, 220, 70, 10, 5, [1, "支配者の証"], 500),
        ]
    return enemies

# 街
def town(player):
    global BP
    BP = 0
    time.sleep(0.5)
    print("街だ")
    time.sleep(0.5)
    print("活気でにぎわっている")
    while True:
        time.sleep(0.5)
        select = input("どうする？ [1]街の門へ行く, [2]アイテムを確認する, [3]ステータスを確認する, [4]武器屋へ行く, [5]道具屋へ行く, [6]酒場へ行く >")
        if select == "1":
            subprocess.call("cls", shell=True)
            time.sleep(0.5)
            print("ここを出れば、もう安全は保障されない")
            time.sleep(0.5)
            while True:
                print("どうする？ [1]失意の館へ行く, [2]絶望の墓場へ行く, [3]終焉の洞窟へ行く")
                print("※ スペースキーで戻る")
                select_next = input("> ")
                subprocess.call("cls", shell=True)
                if select_next == "1" or select_next == "2" or select_next == "3":
                    now_enemy = create_enemies_True(int(select_next))
                    print("\n敵が現れた！")
                    time.sleep(0.5)
                    return now_enemy
                elif select_next == " ":
                    break
                else:
                    print("そんなコマンドはない！")
        elif select == "2":
            item_org(player)
        elif select == "3":
            player.print_str()
        elif select == "4":
            town_weapon(player)
        elif select == "5":
            town_item(player)
        elif select == "6":
            town_bar(player)
        else:
            subprocess.call("cls", shell=True)
            print("そんなコマンドはない！")
def town_weapon(player):
    global GOLD
    subprocess.call("cls", shell=True)
    print("「……らっしゃい」")
    time.sleep(0.8)
    print("強面な男が座っている")
    while True:
        time.sleep(0.5)
        weapon_str = ["どれを買おう？ "]
        weapon_num = []
        for i in range(len(shop_weapon_list)):
            weapon_num.append(str(i + 1))
            weapon_str.append("[{}]{}({} G), ".format(i + 1, shop_weapon_list[i][0], shop_weapon_list[i][2]))
        print("".join(weapon_str))
        print("※ スペースキーで戻る")
        select = input("> ")
        print()
        subprocess.call("cls", shell=True)
        if select in weapon_num:
            if GOLD < shop_weapon_list[int(select) - 1][2]:
                print("金が足りない…")
            else:
                player.weapon = shop_weapon_list[int(select) - 1]
                print("{}は{}を買った".format(player.name, shop_weapon_list[int(select) - 1][0]))
                GOLD -= shop_weapon_list[int(select) - 1][2]
                time.sleep(0.5)
                break
        elif select == " ":
            subprocess.call("cls", shell=True)
            break
        else:
            print("そんなコマンドはない！")
        time.sleep(0.5)
def town_item(player):
    global GOLD
    subprocess.call("cls", shell=True)
    print("「いらっしゃい！」")
    time.sleep(0.8)
    print("明るい女性が元気な声で出迎えてくれる")
    while True:
        time.sleep(0.5)
        item_str = ["どれを買おう？ "]
        item_num = []
        for i in range(len(shop_item_list)):
            item_num.append(str(i + 1))
            item_str.append("[{}]{}({} G), ".format(i + 1, shop_item_list[i][0], shop_item_list[i][1]))
        print("".join(item_str))
        print("※ スペースキーで戻る")
        select = input("> ")
        print()
        subprocess.call("cls", shell=True)
        if select in item_num:
            if GOLD < shop_item_list[int(select) - 1][1]:
                print("金が足りない…")
            elif len(player.item) >= 5:
                print("アイテムがいっぱいだ…")
            else:
                player.item += [shop_item_list[int(select) - 1][0]]
                print("{}は{}を買った".format(player.name, shop_item_list[int(select) - 1][0]))
                GOLD -= shop_item_list[int(select) - 1][1]
                time.sleep(0.5)
                break
        elif select == " ":
            break
        else:
            print("そんなコマンドはない！")
        time.sleep(0.5)
def town_bar(player):
    global GOLD
    subprocess.call("cls", shell=True)
    print("少し騒々しいが、一息つくぐらいならば問題なさそうだ")
    while True:
        time.sleep(0.5)
        print("どうしよう？ [1]休憩する(200 G), [2]酒を飲む(100 G)")
        print("※ スペースキーで戻る")
        select = input("> ")
        print()
        subprocess.call("cls", shell=True)
        if select == "1":
            if GOLD < 200:
                print("金が足りない…")
            else:
                player.hp = player.max_hp
                GOLD -= 200
                print("{}は酒場の中にある宿屋で体を休めた".format(player.name))
                time.sleep(0.5)
                print("{}のHPが最大になった".format(player.name))
                time.sleep(0.5)
                break
        elif select == "2":
            if GOLD < 100:
                print("金が足りない…")
            else:
                print("{}は店主の出した酒を一気に飲み干した".format(player.name))
                time.sleep(0.5)
                print("HPが少し回復した")
                time.sleep(0.5)
                if player.hp < player.max_hp / 4:
                    print("「…あまり無理をするなよ」")
                    time.sleep(0.5)
                player.hp += 250
                if player.hp > player.max_hp:
                    player.hp = player.max_hp
                GOLD -= 100
                break
        elif select == " ":
            break
        else:
            print("そんなコマンドはない！")
        time.sleep(0.5)

if __name__ == "__main__":
    main()