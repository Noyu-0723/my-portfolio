class Player{
    constructor(level, baseHp, baseMp, baseAttack, baseDefence, initialGold){
        this.level = level;
        this.exp = 0;
        this.gold = initialGold;
        this.hp = Math.floor(baseHp * (1 + level / 5));
        this.mp = Math.floor(baseMp * (1 + level / 7));
        this.attack = weapon + Math.floor(baseAttack * (1 + level / 3));
        this.defence = armor + Math.floor(baseDefence * (1 + level / 5));
        this.maxHp = Math.floor(baseHp * (1 + level / 5));
        this.maxMp = Math.floor(baseMp * (1 + level / 7));
    }
    attackEnemy(enemy){
        let damage =  Math.floor(this.attack - enemy.defence + randint(this.attack / 2) - this.attack / 4);
        if(damage < 1) damage = 1;
        enemy.hp -= damage;
        if(enemy.hp < 0) enemy.hp = 0;
        stockLog([0, "プレイヤーの攻撃！"]);
        stockLog([0, `${enemy.name}に ${damage} のダメージを与えた。`]);
    }
    fire(enemy){
        if(this.mp >= 2){
            this.mp -= 2;
            let damage = Math.floor(this.attack * 1.5 - enemy.defence / 2 + randint(this.attack / 2) - this.attack / 4 + 5);
            enemy.hp -= damage;
            if(enemy.hp < 0) enemy.hp = 0;
            stockLog([0, "プレイヤーの魔法攻撃！"]);
            stockLog([0, `${enemy.name}に ${damage} のダメージを与えた。`]);
            return false
        }else{
            stockLog([0, "MPが足りないようだ…"]);
            printLog();
            return true
        }
    }
    heal(){
        if(this.mp >= 3){
            this.mp -= 3;
            let amont = Math.floor(this.attack * 2 + randint(this.attack / 2) - this.attack / 4 + 10);
            let arg = this.maxHp - this.hp;
            this.hp += amont;
            if(this.hp > this.maxHp){
                amont = arg;
                this.hp = this.maxHp;
            }
            stockLog([0, "プレイヤーの回復魔法！"]);
            stockLog([0, `HPが${amont} 回復した。`]);
            return false
        }else{
            stockLog([0, "MPが足りないようだ…"]);
            printLog();
            return true
        }
    }
    levelUp(){
        while(true){
            if(this.exp >= 7 * (1.3 ** this.level)){
                player = new Player(this.level + 1, baseHp, baseMp, baseAttack, baseDefence, this.gold);
                stockLog([1, "レベルアップ！"]);
                this.exp -= this.level * 25;
            }else{
                break;
            }
        }
    }
}

// ポーション・逃げるボタン
function usePotion(){
    cls();

    if(potionCount === 0){
        stockLog([1, "プレイヤーはポーションを飲もうとしたが、もう持っていない…"]);
    }else if(player.hp === player.maxHp){
        stockLog([1, `今は飲む必要がなさそうだ。`]);
    }else if(potionCount > 0){
        player.hp = player.maxHp;
        stockLog([1, `プレイヤーはポーションを飲み、HPが最大まで回復した。`]);
        potionCount--;
    }
    printLog();
    updateStatus();
}
function run(){
    let esc = randint(3);
    if(esc <= 2){
        cls();
        stockLog([1, "なんとか逃げ切れたようだ"]);
        document.getElementById("game-container").style.display = "none";
        document.getElementById("victory").style.display = "none";
        safeSerchDungeon();
    }else{
        cls();
        stockLog([2, "回り込まれてしまった"]);
        enemy.attackPlayer(player);

        if(player.hp === 0){
            stockLog([2, "プレイヤーはやられてしまった…", "red"]);
            defeat();
            updateStatus();
        }else{
            updateStatus();
        }
        printLog();
    }
}

// 敗北
function defeat(){
    document.getElementById("attack-button").disabled = true;
    document.getElementById("special-button").disabled = true;
    document.getElementById("use-potion-button").disabled = true;
    document.getElementById("escape-button").disabled = true;
    document.getElementById("back-button").disabled = true;
    document.getElementById("fire-button").disabled = true;
    document.getElementById("heal-button").disabled = true;
}