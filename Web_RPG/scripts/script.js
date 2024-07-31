// 敵キャラ定義
let enemy;
// アイテム
let potionCount = 0;
let weapon = 0;
let armor = 0;
// プレイヤー生成
let level = 1
let baseHp = 15;
let baseMp = 6;
let baseAttack = 3;
let baseDefence = 1;
let initialGold = 30;
let player = new Player(level, baseHp, baseMp, baseAttack, baseDefence, initialGold);
// ログ管理
let logList = [];
let logId = [];
// ダンジョン管理
let depth = 0;
let dungeonType = 0;
let caveBoss = 1;
let forestBoss = 1;

/* 戦闘関連(メイン処理) */
// 開始
function startBattle(enemyImage){
    cls();

    // 画像のsrc属性を設定
    document.getElementById("enemy-image").src = enemyImage;

    // ステータスを初期化して表示
    document.getElementById("player-hp").textContent = player.hp;
    document.getElementById("player-mp").textContent = player.mp;
    document.getElementById("potion-count").textContent = potionCount;
    document.getElementById("enemy-name").textContent = enemy.name;
    document.getElementById("enemy-hp").textContent = enemy.hp;
    document.getElementById("enemy-attack").textContent = enemy.attack;

    // 不必要なものを非表示
    document.getElementById("gate").style.display = "none"; // 街の門を非表示
    dungeonDisplayDel();

    // 戦闘関連表示
    document.getElementById("default-actions").style.display = "block";
    document.getElementById("game-container").style.display = "block";

    stockLog([2, `${enemy.name}が現れた！`, "red"]); // ログにメッセージ
}
// 通常攻撃
function attack(){
    cls();

    // プレイヤーが敵を攻撃
    player.attackEnemy(enemy);
    if(getWinPlayer(enemy)){
        return;
    }
    // 敵がプレイヤーを攻撃
    enemy.attackPlayer(player);
    if(getWinEnemy(player)){
        return;
    }
    
    printLog();
}
// 特技使用
function fire(){
    cls();

    // プレイヤーが敵を攻撃
    if(player.fire(enemy)){
        return;
    }
    if(getWinPlayer(enemy)){
        return;
    }
    // 敵がプレイヤーを攻撃
    enemy.attackPlayer(player);
    if(getWinEnemy(player)){
        return;
    }
    
    printLog();
}
function heal(){
    cls();

    // プレイヤーが回復
    if(player.heal(enemy)){
        return;
    }
    if(getWinPlayer(enemy)){
        return;
    }
    // 敵がプレイヤーを攻撃
    enemy.attackPlayer(player);
    if(getWinEnemy(player)){
        return;
    }
    
    printLog();
}
// 特技メニュー表示・戻る
function specialMenu(){
    document.getElementById("default-actions").style.display = "none";
    document.getElementById("special-actions").style.display = "block";
}
function back(){
    document.getElementById("default-actions").style.display = "block";
    document.getElementById("special-actions").style.display = "none";
}
// 勝利後のボタン
function leave(){
    cls();
    document.getElementById("game-container").style.display = "none";
    document.getElementById("victory").style.display = "none";
    safeSerchDungeon();
}

/* 戦闘関連(サブ処理) */
// 主人公の勝利判定
function getWinPlayer(enemy){
    if(enemy.hp === 0){
        player.exp += enemy.exp;
        player.gold += enemy.gold;
        stockLog([2, `${enemy.name}を倒した！`, "green"]);
        stockLog([2, `${enemy.exp}の経験値を得た`, "green"]);
        stockLog([2, `${enemy.gold}ゴールドを得た`, "green"]);
        player.levelUp();
        updateStatus();

        if(enemy.name === "ドラゴン"){
            caveBoss--;
        }else if(enemy.name === "ユニコーン"){
            forestBoss--;
        }

        document.getElementById("default-actions").style.display = "none";
        document.getElementById("special-actions").style.display = "none";
        document.getElementById("victory").style.display = "block";
        printLog();
        return true;
    }else{
        return false;
    }
}
// 敵の勝利判定
function getWinEnemy(player){
    if(player.hp === 0){
        stockLog([2, "プレイヤーはやられてしまった…", "red"]);
        defeat();
        updateStatus();
        printLog();
        return true;
    }else{
        updateStatus();
        return false;
    }
}

/* 表示関連 */
// ステータス更新
function updateStatus(){
    // プレイヤーのステータスを更新
    document.getElementById("player-hp").textContent = player.hp;
    document.getElementById("player-mp").textContent = player.mp;
    document.getElementById("potion-count").textContent = potionCount;

    // 敵のステータスを更新
    document.getElementById("enemy-hp").textContent = enemy.hp;
    document.getElementById("enemy-attack").textContent = enemy.attack;
}
// 時間を空けてメッセージをログに送信&タイマーIDを格納
function sleepLog(message, ms){
    logId.push(setTimeout(() => {
        const logMessages = document.getElementById("log-messages");
        const LogMessage = message;
        const LogEntry = document.createElement("div");
        LogEntry.textContent = LogMessage;
        logMessages.appendChild(LogEntry);
    }, ms));
}
function sleepLogColor(message, ms, color){
    logId.push(setTimeout(() => {
        const logMessages = document.getElementById("log-messages");
        const LogMessage = message;
        const LogEntry = document.createElement("div");
        LogEntry.textContent = LogMessage;
        LogEntry.style.color = color;
        logMessages.appendChild(LogEntry);
    }, ms));
}
// 表示文字と時間格納
function stockLog(list){
    logList.push(list);
}   
// 格納された文字をまとめて表示
function printLog() {
    for (let i = 0; i < logList.length; i++) {
        const type = logList[i][0];
        const message = logList[i][1];
        const delay = i * 300; // デフォルトの遅延時間

        if (type === 0) {
            sleepLog(message, delay);
        } else if (type === 1) {
            sleepLog(message, delay + 100);
        } else if (type === 2) {
            const color = logList[i][2];
            sleepLogColor(message, delay, color);
        }
    }
}
// 表示リセット
function cls(){
    const logMessages = document.getElementById("log-messages");
    logMessages.innerHTML = "";

    // タイマーリセット
    for(let i = 0; i < logId.length; i++){
        clearTimeout(logId[i]);
    }

    // 配列の初期化
    logList.splice(0);
    logId.splice(0);
}

/* 数値出力 */
// 1~maxの整数を出力
function randint(max){
    let num = Math.floor(Math.random() * max + 1);
    return num;
}