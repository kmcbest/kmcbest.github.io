'use strict';




var allItems_en = ['4* Demolition Sig*5, Demolition T3C Essence 500*4', 'PBC*2, T3C Shard 100*5', 'Boost Crystal*5, AM Revive*2, AM Repair*2', '2* Sharkticon Crystals*3, Superior Sig Crystal*5', 'Knight Crystal (1/2/3/4), T1C*5', '4* Brawler Sig*5, Brawler T3C Essence 500*4', 'Exclusive 2* Crystal*3, T3B Essence 2000*5', 'PBC*2, Better Rank-up Crystal*2', '4* Warrior Sig*5, Warrior T3C Essence 500*4', 'Boost Crystal*5, AM Revive*1, AM Repair*1', '4* Bot Shard 100*5, Gold Crystal*5', 'T3C Shard 100*5, Rank-up Crystal*5', '3* Bot Crystal*1, 3* Sig*5 (6 classes)', 'T2A Essence 1250*2, T2C*3', '4* Scout Sig*5, Scout T3C Essence 500*4', 'Energon 20*10, Rank-up Crystal*5', 'T1A*2, 2* Sharkticon Crystals*3', 'Gold Crystal*5, AM Revive*2, AM Repair*2', 'T1 Mod Class Spark*3, PMC*3', 'T4B Essence 250*2, T3B Essence 2000*5', '4* Tech Sig*5, Tech T3C Essence 500*4', 'Knight Crystal (1/2/3/4), T2C*3', '3* Bot Crystal*1, Superior Sig Crystal*5', 'Gold Crystal*5, Tier 4 AM Revive*1, Tier 4 AM Repair*2', 'T2A Essence 1250*2, PBC*2', '4* Tactician Sig*5, Tactician T3C Essence 500*4', '4* Bot Shard 100*5, T1C*5', 'Exclusive 2* Crystal*3, T1A*2',];
var allItems_cn = ['4星爆破招牌程序*5,爆破T3类别火种精华500*4', '高等机器人水晶*2,T3类别火种碎片100*5', '加成水晶*5,盟战复活组件*2,盟战修复组件*2', '2星饿鲨水晶*3,超级招牌程序水晶*5', '1/2/3/4阶骑士水晶,T1类别火种*5', '4星斗士招牌程序*5,斗士T3类别火种精华500*4', '独家2星水晶*3,T3基础火种精华2000*5', '高等机器人水晶*2,更好的升阶水晶*2', '4星战士招牌程序*5,战士T3类别火种精华500*4', '加成水晶*5,盟战复活组件*1,盟战修复组件*1', '4星机器人碎片100*5,黄金水晶*5', 'T3类别火种碎片100*5,升阶水晶*5', '3星机器人水晶*1,（6类别）3星招牌程序*5', 'T2阿尔法火种精华1250*2,T2类别火种*3', '4星侦查招牌程序*5,侦查T3类别火种精华500*4', '能量晶体20*10,升阶水晶*5', 'T1阿尔法火种*2,2星饿鲨水晶*3', '黄金水晶*5,盟战复活组件*2,盟战修复组件*2', 'T1模块类别火种*3,高等模块水晶*3', 'T4基础火种精华250*2,T3基础火种精华2000*5', '4星科技招牌程序*5,科技T3类别火种精华500*4', '骑士水晶(1/2/3/4),T2类别火种*3', '3星机器人水晶*1,超级招牌程序水晶*5', '黄金水晶*5,4阶盟战复活组件*1,4阶盟战修复组件*2', 'T2阿尔法火种精华1250*2,高等机器人水晶*2', '4星战术招牌程序*5,战术T3类别火种精华500*4', '4星机器人碎片100*5,T1类别火种*5', '独家2星水晶*3,T1阿尔法火种*2'];

var itemCost_en; // To be implemented


function getItems(items, isToday) {
    var one_day = 1000 * 60 * 60 * 24;
    var startTime = new Date('4/8/2019');
    var today = new Date();
    var timeDiff = today.getTime() - startTime;
    var daysBetween = Math.floor(timeDiff / one_day) % 28;
    if (isToday === true) {
        return items[daysBetween];
    }
    else {
        return items[daysBetween + 1];
    }
}

function todayis(isToday) {
    var startDay = new Date();
    var tomorrowDay = new Date();
    var dd, mm, yyyy;
    var strTheDate;
    tomorrowDay.setDate(startDay.getDate() + 1);
    if (isToday === true) {
        dd = String(startDay.getDate()).padStart(2, '0');
        mm = String(startDay.getMonth() + 1).padStart(2, '0');
        yyyy = startDay.getFullYear();
        strTheDate = yyyy + '年' + mm + '月' + dd + '日';
        return strTheDate;
    }
    else {
        dd = String(tomorrowDay.getDate()).padStart(2, '0');
        mm = String(tomorrowDay.getMonth() + 1).padStart(2, '0');
        yyyy = tomorrowDay.getFullYear();
        strTheDate = yyyy + '年' + mm + '月' + dd + '日';
        return strTheDate;
    }
}
console.log(getItems(allItems_cn, false));
console.log(todayis(false));