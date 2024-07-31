import random
import subprocess
import time
import sys

KP = 0 # 経験値
BP = 0 # ダンジョンの階層
SP = 0 # 死神の出現フラグ
PP = 0 # ポーション(ゴブリン)
NKP = 0 # 拘束時間
MKP = 0 # 無敵時間
EP = 0 # 英雄の証
EEP = 0 # 古代の進化(ゴーレム)
GA = 0 # ドラゴンの攻撃パターン制御
GOLD = 1000 # ゴールド

# ゲームスタート
def main():
    subprocess.call("cls", shell=True)
    game_type = False
    player_name = input("プレイヤーの名前を入力してください: ")
    if player_name == "Untot":
        player = Player_True(player_name, 700, 200, 100, 30, 10, 200, 3, 250, 3, 1, 0, 0, [])
        game_type = True
    elif player_name == "ああああ":
        player = Player(player_name, 999, 9999, 9999, 99, 99, 999, 99, 999, 99, ["英雄の証", "透明な液体", "古代の秘宝", "古代の秘宝", "伝説の宝玉"])
    else:
        player = Player(player_name, 100, 20, 0, 5, 1, 25, 2, 35, 2, [])
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
                        itemK(player)
                    else:
                        print("そんなコマンドはない！")
    else:
        homeStart(player)
        enemies = createEnemies_False()
        # メインループ
        while True:
            if SP % 5 == 0 and SP != 0:
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
        print("特技使用回数(ヒール)：{}".format(self.HealC))
        time.sleep(0.2)
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
    def __init__(self, name, hp, attack, defence, speed, level, Heal, HealC, Fire, FireC, PowerC, SpecialC, state, item):
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
        miss = random.randint(0, 2)
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

    def printStr(self):
        subprocess.call("cls", shell=True)
        time.sleep(0.5)
        print("レベル：{}".format(self.level))
        time.sleep(0.2)
        print("名前：{}".format(self.name))
        time.sleep(0.2)
        print("所持金：{}G".format(GOLD))
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
        print("特技使用回数(必殺)：{}".format(self.SpecialC))
        time.sleep(0.2)
        print("\n")

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
class EnemyZom(Enemy): # ゾンビ
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
class EnemyVan(Enemy): # ヴァンパイア
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
class EnemyGol(Enemy): # ゴーレム
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
class EnemyHyu(Enemy): # ヒュドラ
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
        if T <= 3 and self.hp < self.max_hp / 2:
            print("{}の「五連撃」".format(self.name))
            damage = 0
            for _ in range(5):
                damage5 = random.randint(30, 40) - player.defence / 10
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
class BOSSEnemyDor(Enemy): # ドラゴン
    def attack_player(self, player):
        global NKP, MKP, GA
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
class EnemyNight(Enemy_True): # ナイトメア
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
            if random.randint(0, 2) == 1:
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
class EnemyMar(Enemy_True): # マリオネット
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
class EnemyDeaPer(Enemy_True): # デスペラード
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
class EnemyWitch(Enemy_True): # 失意の魔女
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
            if state:
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
            if random.randint(0, 3) == 1:
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

# 戦闘
def battle(player, enemy):
    global PP, NKP, MKP, EEP, GA
    PP = 0
    NKP = 0
    MKP = 0
    EEP = 0
    enemy.hp = enemy.max_hp
    if enemy.name == "ゾンビ":
        enemy.revival = enemy.revival_S
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
                        enemy.attack_player(player)
                        usezomring(player)
                        break
                elif command_next == "f":
                    if player.FireC <= 0:
                        print("もう攻撃魔法は使えない！")
                    else:
                        player.fire(enemy)
                        if enemy.hp > 0:
                            enemy.attack_player(player)
                        usezomring(player)
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
                        useItem(player, enemy, player.item[int(select) - 1], int(select) - 1)
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
                enemy.attack_player(player)
                usezomring(player)
        else:
            print("そんなコマンドはない！")
        if enemy_defeat(player, enemy):
            break
        if player_defeat(player):
            break
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
def enemy_defeat(player, enemy):
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
def player_defeat(player):
    if player.hp <= 0 and "死者の魂" not in player.item:
        time.sleep(0.5)
        print("{}は死んでしまった...".format(player.name))
        return True
    elif player.hp <= 0 and "死者の魂" in player.item:
        usezomsoul(player)
    return False

def battle_True(player, enemy):
    global NKP, MKP
    NKP = 0
    MKP = 0
    enemy.hp = enemy.max_hp
    player.speed = player.speed_S
    player.attack = player.attack_S
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
                    enemy.attack_player(player)
            elif player.speed < enemyS:
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
                            enemy.attack_player(player)
                        break
                elif command_next == "s":
                    if player.SpecialC <= 0:
                        print("今は天の加護を使えない！")
                    else:
                        player.special()
                        enemy.attack_player(player)
                        break
                elif command_next == "h":
                    if player.HealC <= 0:
                        print("もう回復呪文は使えない！")
                    else:
                        player.heal()
                        enemy.attack_player(player)
                        break
                elif command_next == "f":
                    if player.FireC <= 0:
                        print("もう攻撃魔法は使えない！")
                    else:
                        player.fire(enemy)
                        if enemy.hp > 0:
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
                        useItem(player, enemy, player.item[int(select) - 1], int(select) - 1)
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
                enemy.attack_player(player)
        else:
            print("そんなコマンドはない！")
        if enemy_defeat(player, enemy):
            break
        if player_defeat(player):
            break

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
            itemK(player)
        elif select == "3":
            player.printStr()
        else:
            print("そんなコマンドはない！")
def homeStart(player):
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
        elif select == "3":
            player.printStr()
        elif select == "99":
            kinds = int(input("敵の種類を入力して下さい [0 or 1] >"))
            floor = int(input("階層を入力して下さい [0 ~ 7] >"))
            if kinds == 0:
                enemy = createEnemies_False()[floor]
            elif kinds == 1:
                enemy = createEnemies_True()[floor]
            subprocess.call("cls", shell=True)
            battle(player, enemy)
            sys.exit()
        else:
            print("そんなコマンドはない！")

# アイテムの整理・追加・使用
def itemK(player): # アイテムの整理
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
        print("※ 所持時、素早さが20上昇\n")
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
        print("はるか昔に女性がつけていた綺麗な指輪。")
        print("その女性が亡くなって以降その指輪には守護の力が宿ったと言う伝説が残された。")
        print("しかし現在所在が分からず知る者は誰も居ない。")
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
    time.sleep(0.5)
def useItem(player, enemy, item_name, item_number): #アイテムの使用
    global NKP, MKP
    if item_name in ["古びた指輪", "透明な指輪", "腐った指輪", "死者の魂", "番犬のチョーカー", "鋼鉄の指輪"]:
        time.sleep(0.5)
        print("{}は「{}」を使った".format(player.name, item_name))
        time.sleep(0.5)
        print("しかし何も起こらなかった")
        time.sleep(0.8)
    elif item_name == "スライムの粘液":
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
            timePrint(message[i][0], message[i][1])
        time.sleep(1.0)
        print("\033[31m'Held name = Untot'\033[0m")
        sys.exit()
def getItem(player, enemy): # アイテムの入手
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
def usezomring(player): # 腐った指輪用の処理
    if "腐った指輪" in player.item:
        time.sleep(0.5)
        print("「腐った指輪」の効果でhpが15回復した\n")
        time.sleep(0.5)
        player.hp += 15
        if player.hp >= player.max_hp:
            player.hp = player.max_hp
def usezomsoul(player): # 死者の魂用の処理
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

# 一文字ずつ表示
def timePrint(dis, str):
    leng = len(str)
    for i in range(leng):
        print(str[i], end="", flush=True)
        time.sleep(dis)

# 敵の作成
def createEnemies_False():
    enemies = [
        [
            EnemySli("スライム", 30, 10, 10, 0, 1, [0, "スライムの粘液", "スライムゼリー"]),
            EnemyGob("ゴブリン", 50, 20, 0, 5, 1, [0, "古びた指輪", "ポーション"]),
        ],
        [
            EnemyZom("ゾンビ", 120, 50, 0, 0, 2, [0, "腐った指輪", "死者の魂"], 1),
            EnemyGho("ゴースト", 3, 35, 99, 99, 2, [0, "透明な指輪", "透明な液体"]),
        ],
        [
            EnemyKel("ケルベロス", 150, 70, 15, 15, 3, [0, "番犬のチョーカー", "キャンディー"]),
            EnemySco("スコーピオン", 75, 80, 30, 15, 3, [0, "毒針", "鋼鉄の指輪"]),
        ],
        EnemyVan("ヴァンパイア", 200, 80, 20, 10, 4, [0, "吸血の牙", "ヴァンパイアの血液"]),
        EnemyGol("ゴーレム", 120, 80, 20, 0, 4, [1, "古代の秘宝"]),
        EnemyHyu("ヒュドラ", 400, 100, 30, 40, 5, [2, "英雄の証"]),
        BOSSEnemyDor("ドラゴン", 800, 120, 40, 35, 6, [3, "伝説の秘宝"]),
        Enemy("死神", 999, 200, 50, 70, 99, [3, "伝説の秘宝"]),
    ]
    return enemies
def createEnemies_True(type):
    enemies = ""
    if type == 1:
        enemies = [
            EnemyNight("ナイトメア", 500, 200, 50, 30, 5, [1, "吸血の牙"], 75),
            EnemyMar("マリオネット", 700, 130, 50, 0, 5, [1, "古代の秘宝"], 100),
            EnemyDeaPer("デスペラード", 700, 1, 100, 40, 5, [1, "英雄の証"], 150),
            EnemyWitch("失意の魔女", 1200, 220, 70, 10, 5, [1, "伝説の秘宝"], 500),
        ]
    elif type == 2:
        enemies = [
            EnemyNight("ナイトメア", 500, 200, 50, 30, 5, [1, "吸血の牙"], 75),
            EnemyMar("マリオネット", 700, 130, 50, 0, 5, [1, "古代の秘宝"], 100),
            EnemyDeaPer("デスペラード", 700, 1, 100, 40, 5, [1, "英雄の証"], 150),
            EnemyWitch("失意の魔女", 1200, 220, 70, 10, 5, [1, "伝説の秘宝"], 500),
        ]
    elif type == 3:
        enemies = [
            EnemyNight("ナイトメア", 500, 200, 50, 30, 5, [1, "吸血の牙"], 75),
            EnemyMar("マリオネット", 700, 130, 50, 0, 5, [1, "古代の秘宝"], 100),
            EnemyDeaPer("デスペラード", 700, 1, 100, 40, 5, [1, "英雄の証"], 150),
            EnemyWitch("失意の魔女", 1200, 220, 70, 10, 5, [1, "伝説の秘宝"], 500),
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
                    now_enemy = createEnemies_True(int(select_next))
                    print("\n敵が現れた！")
                    time.sleep(0.5)
                    return now_enemy
                elif select_next == " ":
                    break
                else:
                    print("そんなコマンドはない！")
        elif select == "2":
            itemK(player)
        elif select == "3":
            player.printStr()
        else:
            print("そんなコマンドはない！")

if __name__ == "__main__":
    main()