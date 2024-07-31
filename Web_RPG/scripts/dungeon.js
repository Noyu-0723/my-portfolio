// 始まりの洞窟探索
function searchDungeonCave(){
    cls();
    dungeonType = 1;

    if(depth < 0) depth = 0;

    document.getElementById("gate").style.display = "none"; // 街の門を非表示
    dungeonDisplayApp();
    let num = randint(10);

    if(depth === 5 && caveBoss === 0){
        stockLog([2, "最深部まで来てしまったようだ"]);
    }else if(depth === 5){
        enemy = new Doragon(randint(2));
        startBattle("images/doragon.jpg");
    }else if(num <= 3){
        enemy = new Slime(randint(3));
        startBattle("images/slime.png");
    }else if(num <= 5){
        enemy = new Goblin(randint(3));
        startBattle("images/goblin.png");
    }else{
        stockLog([1, "薄暗い洞窟だ…"]);
    }
    printLog();
}

// 悪夢の森探索
function searchForest(){
    cls();
    dungeonType = 2;

    if(depth < 0) depth = 0;

    document.getElementById("gate").style.display = "none"; // 街の門を非表示
    dungeonDisplayApp();
    
    let num = randint(10);

    if(depth === 5 && forestBoss === 0){
        stockLog([2, "これ以上進むのは危険だ、引き返そう"]);
    }else if(depth === 5){
        enemy = new Unicorn(randint(2));
        startBattle("images/unicorn.png");
    }else if(num <= 3){
        enemy = new Nightmare(randint(3));
        startBattle("images/akumu.png");
    }else if(num <= 5){
        enemy = new Scorpion(randint(3));
        startBattle("images/sasori.png");
    }else{
        stockLog([1, "鬱蒼とした森だ…"]);
    }
    printLog();
}

// 勝利後or逃走後のダンジョン表示
function safeSerchDungeon(){
    dungeonDisplayApp();
    if(dungeonType === 1){
        stockLog([1, "薄暗い洞窟だ…"]);
    }else if(dungeonType === 2){
        stockLog([1, "鬱蒼とした森だ…"]);
    }
    printLog();
}

// ダンジョンを進むor戻る
function goDungeon(){
    if(depth < 5){
        depth++;
    }
    if(dungeonType === 1){
        searchDungeonCave();
    }else if(dungeonType === 2){
        searchForest();
    }
}
function returnDungeon(){
    if(depth > -1){
        depth--;
        if(depth === -1){
            cls();
            dungeonDisplayDel();
            document.getElementById("gate").style.display = "block";
            stockLog([1, "無事に帰ってこれたようだ"]);
            printLog();
            return;
        }
    }
    if(dungeonType === 1){
        searchDungeonCave();
    }else if(dungeonType === 2){
        searchForest();
    }
}

// ダンジョン表示・非表示の選択
function dungeonDisplayDel(){
    let dun;
    if(dungeonType === 1){
        dun = document.getElementById("dungeon-cave");
    }else if(dungeonType === 2){
        dun = document.getElementById("dungeon-forest");
    }
    dun.style.display = "none";
}
function dungeonDisplayApp(){
    let dun;
    if(dungeonType === 1){
        dun = document.getElementById("dungeon-cave");
    }else if(dungeonType === 2){
        dun = document.getElementById("dungeon-forest");
    }
    dun.style.display = "block";
}