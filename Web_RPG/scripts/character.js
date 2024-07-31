class Enemy{
    constructor(level, name, baseHp, baseAttack, baseDefence, baseExp, baseGold){
        this.level = level;
        this.name = name;
        this.hp = Math.floor(baseHp * (1 + level / 10));
        this.attack = Math.floor(baseAttack * (1 + level / 10));
        this.defence = Math.floor(baseDefence * (1 + level / 10));
        this.exp = Math.floor(baseExp * (1 + level / 10));
        this.gold = Math.floor(baseGold * (1 + level / 10));
    }
    attackPlayer(player){
        let damage = this.attack - player.defence + randint(2) - 1;
        if(damage < 1) damage = 1;
        player.hp -= damage; // プレイヤーにダメージを与える
        if(player.hp < 0) player.hp = 0;
        stockLog([0, `${this.name}の攻撃！`]);
        stockLog([0, `プレイヤーに ${damage} のダメージを与えた。`]);
    }
}

// スライムクラス
class Slime extends Enemy{
    constructor(level){
        super(level, "スライム", 8, 2, 1, 5, 3);
    }
}

// ゴブリンクラス
class Goblin extends Enemy{
    constructor(level){
        super(level, "ゴブリン", 12, 3, 0, 8, 6);
    }
}

// スコーピオンクラス
class Scorpion extends Enemy{
    constructor(level){
        super(level, "スコーピオン", 20, 8, 7, 35, 20);
    }
}

// ナイトメアクラス
class Nightmare extends Enemy{
    constructor(level){
        super(level, "ナイトメア", 18, 6, 3, 18, 12);
    }
}

// ドラゴンクラス
class Doragon extends Enemy{
    constructor(level){
        super(level, "ドラゴン", 40, 5, 3, 100, 50);
    }
    attackPlayer(player){
        let decide = randint(10);
        let damage;
        if(decide < 8){
            damage = this.attack - player.defence + randint(2) - 1;
            stockLog([0, `${this.name}の攻撃！`]);
        }else{
            damage = Math.floor(this.attack * 1.5 + randint(4) - 2);
            stockLog([0, `${this.name}の「火炎球」！`]);
        }
        if(damage < 1) damage = 1;
        player.hp -= damage;
        if(player.hp < 0) player.hp = 0;
        stockLog([0, `プレイヤーに ${damage} のダメージを与えた。`]);
    }
}

// ユニコーンクラス
class Unicorn extends Enemy{
    constructor(level){
        super(level, "ユニコーン", 100, 12, 5, 700, 250);
    }
    attackPlayer(player){
        let decide = randint(10);
        let damage;
        if(decide < 8){
            damage = this.attack - player.defence + randint(2) - 1;
            stockLog([0, `${this.name}の攻撃！`]);
        }else{
            damage = Math.floor(this.attack * 1.5 + randint(4) - 2);
            stockLog([0, `${this.name}の「突進」！`]);
        }
        if(damage < 1) damage = 1;
        player.hp -= damage;
        if(player.hp < 0) player.hp = 0;
        stockLog([0, `プレイヤーに ${damage} のダメージを与えた。`]);
    }
}