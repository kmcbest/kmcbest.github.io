'use strict';




var allItems_en = ['4* Demolition Sig*5, Demolition T3C Essence 500*4', 'PBC*2, T3C Essence Crystal*2', 'Boost Crystal*5, Tier 2 AM Revive*2, Tier 3 AM Repair*2', '2* Sharkticon Crystals*3, Superior Sig Crystal*3', 'Knight Crystal (1/2/3/4), T1C*5', '4* Brawler Sig*5, Brawler T3C Essence 500*4', 'Exclusive 2* Crystal*3, T3B Essence 2000*5', 'PBC*2, Greater Rank-up Crystal*2', '4* Warrior Sig*5, Warrior T3C Essence 500*4', 'Boost Crystal*5, Tier 3 AM Revive*1, Tier 4 AM Repair*1', '4* Bot Shard 100*5, Gold Crystal*5', 'T3C Shard 100*5, Rank-up Crystal*5', '3* Bot Crystal*1, 3* Sig*5 (6 classes)', 'T2A Essence 1250*2, T2C*3', '4* Scout Sig*5, Scout T3C Essence 500*4', 'Energon 20*10, Rank-up Crystal*5', 'T1A*2, 2* Sharkticon Crystals*3', 'Gold Crystal*5, Tier 2 AM Revive*2, Tier 3 AM Repair*2', 'T1 Mod Class Spark*3, PMC*3', 'T4B Essence 250*2, T3B Essence 2000*5', '4* Tech Sig*5, Tech T3C Essence 500*4', 'Knight Crystal (1/2/3/4), T2C*3', '3* Bot Crystal*1, Superior Sig Crystal*3', 'Gold Crystal*5, Tier 4 AM Revive*1, Tier 4 AM Repair*2', 'T2A Essence 1250*2, PBC*2', '4* Tactician Sig*5, Tactician T3C Essence 500*4', '4* Bot Shard 100*5, T1C*5', 'Exclusive 2* Crystal*3, T1A*2'];
var allItems_cn = ['4星爆破招牌程序*5，T3爆破火种精华500*4', '高等机器人水晶*2，T3类别火种精华水晶*2', '加成水晶*5，一阶盟战复活组件（10%）*2，三阶盟战小队修复组件（15%）*2', '2星饿鲨水晶*3，超级招牌水晶*3', '1/2/3/4阶骑士水晶，T1类别火种水晶*5', '4星斗士招牌程序*5，T3斗士火种精华500*4', '独家2星水晶*3，T3基础火种精华2000*5', '高等机器人水晶*2，更好的升阶水晶*2', '4星战士招牌程序*5，T3战士火种精华500*4', '加成水晶*5，二阶盟战单体复活组件（25%）*1，四阶盟战小队修复组件（20%）*1', '4星机器人碎片100*5，黄金水晶*5', 'T3类别火种碎片100*5，升阶水晶*5', '3星机器人水晶*1，（6类别）3星招牌程序*5', 'T2阿尔法火种精华1250*2，T2类别火种*3', '4星侦查招牌程序*5，T3侦查火种精华500*4', '能量晶体20*10，升阶水晶*5', 'T1阿尔法火种*2，2星饿鲨水晶*3', '黄金水晶*5，一阶盟战小队复活组件（10%）*2，三阶盟战小队修复组件（15%）*2', 'T1模块类别火种*3，高等模块水晶*3', 'T4基础火种精华250*2，T3基础火种精华2000*5', '4星科技招牌程序*5，T3科技火种精华500*4', '1/2/3/4阶骑士水晶，T2类别火种*3', '3星机器人水晶*1，超级招牌水晶*3', '黄金水晶*5，二阶盟战单体复活组件（25%）*1，四阶盟战小队修复组件（20%）*1', 'T2阿尔法火种精华1250*2，高等机器人水晶*2', '4星战术招牌程序*5，T3战术火种精华500*4', '4星机器人碎片100*5，T1类别火种*5', '独家2星水晶*3，T1阿尔法火种*2'];
var item_prices = ['20000*5 + 35000*4', '3000*2 + 50000*2', '4000*5 + 6000*2 + 6000*2', '12000*3 + 8000*3', '110000 + 40000 + 15000*2 + 6000*3 + 5000*5', '20000*5 + 35000*4', '12000*3 + 20000*5', '3000*2 + 35000*2', '20000*5 + 35000*4', '4000*5 + 10000 + 10000', '25000*5 + 2000*5', '15000*5 + 4000*5', '40000 + 5000*5*6', '60000*2 + 10000*3', '20000*5 + 35000*4', '3000*10 + 4000*5', '25000*2 + 12000*3', '2000*5 + 6000*2 + 6000*2', '15000*3 + 2000*3', '40000*2 + 20000*5', '20000*5 + 35000*4', '110000 + 40000 + 15000*2 + 6000*3 + 10000*3', '40000 + 8000*3', '2000*5 + 10000 + 10000', '60000*2 + 3000*2', '20000*5 + 35000*4', '25000*5 + 5000*5', '12000*3 + 25000*2'];
var itemCost_en; // To be implemented


function getItems(items, prices, isToday) {
    var one_day = 1000 * 60 * 60 * 24;
    var startTime = new Date('4/8/2019');
    var today = new Date();
    var timeDiff = today.getTime() - startTime;
    console.log(timeDiff);

    var daysBetween = Math.floor(timeDiff / one_day) % 28;
    console.log(daysBetween);

    var item_and_price = {};
    if (isToday === true) {
        item_and_price.item = items[daysBetween];
        item_and_price.price = prices[daysBetween];
        return item_and_price;
    }
    else {
        item_and_price.item = items[(daysBetween + 1) % 28];
        item_and_price.price = prices[(daysBetween + 1) % 28];
        return item_and_price;
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
// console.log(getItems(allItems_cn, false));
// console.log(todayis(false));
