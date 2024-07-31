/* 武器防具屋 */
function goStore(){
    cls();
    document.getElementById("start-city").style.display = "none";
    document.getElementById("store").style.display = "block";
    stockLog([0, "色々な武器・防具が所狭しと並んでいる"]);
    printLog();
}
function buyDagger(){
    cls();
    buyAnyThing("ダガー", 20);
    printLog();
}
function buyLongsword(){
    cls();
    buyAnyThing("ロングソード", 80);
    printLog();
}
function buyCloth(){
    cls();
    buyAnyThing("布の服", 15)
    printLog();
}
function buyPlateArmor(){
    cls();
    buyAnyThing("鉄の鎧", 120)
    printLog();
}

/* 酒場 */
function goBar(){
    cls();
    document.getElementById("start-city").style.display = "none";
    document.getElementById("bar").style.display = "block";
    stockLog([0, "酒場だ"]);
    stockLog([0, "金を払えば宿屋としても利用できるみたいだ"]);
    printLog();
}
// 休憩
function breakTime(){
    cls();
    if(player.gold >= 30){
        player.gold -= 30;
        player.hp = player.maxHp;
        player.mp = player.maxMp;
        potionCount = 3;
        stockLog([0, "あなたは30ゴールドを支払って休憩することにした"]);
        stockLog([0, "HP・MPが最大になった"]);
        stockLog([0, "ポーション数が3個になった"]);
        updateGold();
        printLog();
    }else{
        stockLog([0, "ゴールドが足りないみたいだ…"]);
        printLog();
    }
}

/* 街の門 */
function goGate(){
    cls();
    
    document.getElementById("gold-display").style.display = "none";
    document.getElementById("start-city").style.display = "none";
    document.getElementById("gate").style.display = "block";
    stockLog([0, "ここを一歩出ればもう安全は保障されない"]);
    printLog();
}

/* スタート画面 */
function cityBack(){
    cls();

    document.getElementById("gold-display").style.display = "block";
    document.getElementById("store").style.display = "none";
    document.getElementById("bar").style.display = "none";
    document.getElementById("gate").style.display = "none";
    document.getElementById("start-city").style.display = "block";
    updateGold();
    stockLog([0, "何処へ行こう？"])
    printLog();
}

/* その他の処理 */
// 購入処理
function buyAnyThing(name, price){
    if(player.gold >= price){
        player.gold -= price
        stockLog([0, `あなたは${price}ゴールド支払って${name}を購入した`]);
        updateGold();
        equipment(name);
        return true;
    }else{
        stockLog([0, "ゴールドが足りないみたいだ…"]);
        return false;
    }
}
// 装備処理
function equipment(name){
    let message;
    if(name === "ダガー"){
        weapon = 3;
        message = `武器攻撃力が${weapon}になった`;
    }else if(name === "ロングソード"){
        weapon = 7;
        message = `武器攻撃力が${weapon}になった`;
    }else if(name === "布の服"){
        armor = 2;
        message = `防具防御力が${armor}になった`;
    }else if(name === "鉄の鎧"){
        armor = 6;
        message = `防具防御力が${armor}になった`;
    }
    player.attack = weapon + Math.floor(baseAttack * (1 + level / 3));
    player.defence = armor + Math.floor(baseDefence * (1 + level / 5));
    stockLog([0, message]);
}
// ゴールドの表示更新
function updateGold(){
    document.getElementById("gold").textContent = player.gold;
}