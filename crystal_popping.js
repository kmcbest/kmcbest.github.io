'use strict';
var totalCrystals = 0;

var allRewards = new Array();

function getBot(strType) {
    var theBot;
    var list2 = ['碾碎器', '钢锁', '斗擎', '汽车大师', '雷震', '碎骨魔', '阿尔茜', '风刃', '路障', '横炮', '犀牛', '救护车', '幻影', '铁皮', '搅拌者', '战擎', '大黄蜂'];
    var list3 = ['碾碎器', '猩猩队长', '钢锁', '斗擎', '汽车大师', '野牛', '雷震', '探长', '碎骨魔', '漂移', '阿尔茜', '热破', '巨蝎勇士', '风刃', '路障', '横炮', '反冲', '警车', '爵士', '黄豹', '声波', '震荡波', '犀牛', '救护车', '幻影', '录音机', '千斤顶', '爆威', '黄蜂勇士', '铁皮', '喷气机', '惊破天', '搅拌者', '震天尊', '战威', '恐龙勇士', '战擎', '通天晓', '红蜘蛛', '狂飙'];
    var list4 = ['碾碎器', '猩猩队长', '钢锁', '斗擎', '汽车大师', '野牛', '雷震', '探长', '碎骨魔', '漂移', '阿尔茜', '热破', '巨蝎勇士', '风刃', '路障', '横炮', '反冲', '警车', '爵士', '黄豹', '声波', '震荡波', '犀牛', '救护车', '幻影', '录音机', '千斤顶', '爆威', '黄蜂勇士', '铁皮', '喷气机', '惊破天', '搅拌者', '震天尊', '战威', '恐龙勇士', '战擎', '通天晓', '红蜘蛛', '狂飙'];
    var list5 = ['碾碎器', '猩猩队长', '钢锁', '斗擎', '碎骨魔', '漂移', '阿尔茜', '热破', '路障', '反冲', '警车', '黄豹', '声波', '震荡波', '犀牛', '幻影', '爆威', '黄蜂勇士', '惊破天', '搅拌者', '战威', '恐龙勇士', '通天晓', '红蜘蛛'];
    var listBee = ['大黄蜂', '小黄蜂'];
    var listNP = ['暗黑擎天柱'];
    var listTC = ['惊天雷'];
    var listClassSpark = ['T3斗士火种', 'T3战士火种', 'T3侦查火种', 'T3科技火种', 'T3爆破火种', 'T3战术火种'];
    // console.log(nStar);
    // var listT1A = ['T1阿尔法火种'];
    // var listT2A = ['T2阿尔法火种'];
    // var listT3A = ['T3阿尔法火种（精华）'];
    // var listT4B = ['T4基础火种'];
    // var listT3B = ['T3基础火种'];
    // var listT3C = ['T3类别火种'];
    // var list4shards = ['4星机器人水晶碎片（750）'];
    // var list5shards = ['5星机器人水晶碎片（2500）'];
    var listMods = ['伤害加速器', '夜莺模块', '机器人资源', '激光制导模块', '奇怪的折射镜', '安全模块', '修复模块', 'EMI模块', '外部过滤器', '抑制器'];

    switch (strType) {
        case '2 star':
            theBot = list2[Math.floor(Math.random() * list2.length)];
            break;
        case '3 star':
            theBot = list3[Math.floor(Math.random() * list3.length)];
            break;
        case '4 star':
            theBot = list4[Math.floor(Math.random() * list4.length)];
            break;
        case '5 star':
            theBot = list5[Math.floor(Math.random() * list5.length)];
            break;
        case 'Bee':
            theBot = listBee[Math.floor(Math.random() * listBee.length)];
            break;
        case 'NP':
            theBot = listNP[Math.floor(Math.random() * listNP.length)];
            break;
        case 'TC':
            theBot = listTC[Math.floor(Math.random() * listTC.length)];
            break;
        case 'Mods':
            theBot = listMods[Math.floor(Math.random() * listMods.length)];
            break;
        case 't3c':
            theBot = listClassSpark[Math.floor(Math.random() * listClassSpark.length)];
            break;
        default:
            break;
    }
    return theBot;
}

function weightedRand(spec) {
    var i, sum = 0, r = Math.random();
    for (i in spec) {
        sum += spec[i];
        if (r <= sum) return i;
    }
}

function spinCrystal(crystalType, crystalNumber) {
    var botType, botStar, poppedBot;
    var spec_pbc = { 0: 0.01, 1: 0.26, 2: 0.73 }; // Premium bot  4, 3, 2 star
    var spec_monthly = { 0: 0.015, 1: 0.135, 2: 0.85 }; // Monthly featured: 5, 4, 3 star
    var spec_wheel = { 0: 0.01, 1: 0.02, 2: 0.01, 3: 0.12, 4: 0.84 };  // Gold wheel: 5 Bee, 4 Bee, 5, 4, 3, star
    var spec_matrix = { 0: 0.005, 1: 0.015, 2: 0.0025, 3: 0.01, 4: 0.1175, 5:0.85 };  // Dark Matrix: 5 NP, 4 NP, 4 TC, 5, 4, 3, star
    var spec_gag = { 0: 0.0075, 1: 0.0551, 2: 0.0075, 3: 0.2049, 4: 0.725 }; // Good as Gold 4 Bee, 3 Bee, 4, 3, 2 star
    var spec_t3k = { 0: 0.04, 1: 0.1, 2: 0.06, 3: 0.07, 4: 0.3, 5: 0.15, 6: 0.25, 7: 0.03 };  // T3 Knight: 4-Star Bot (4%)     3-Star Bot (10%)     4-Star Mod (6%)     3-Star Mod (7%)     Tier 1 Alpha Spark (30%)     T3 Basic Spark (15%)     750 4-Star Bot Shards (25%)     Tier 2 Alpha Spark (3%) 
    var spec_t4k = { 0: 0.25, 1: 0.25, 2: 0.25, 3: 0.17, 4: 0.03, 5: 0.04, 6: 0.01 } // T4 Knight : T3 Class Spark (25%)     4-Star Bot (25%)     4-Star Mod (25%)     5-Star Bot Crystal Shards  (17%)     5-Star Bot (3%)     Tier 4 Basic Spark (4%)     Tier 3 Alpha Spark Essence (1%) 

    var botArray5 = new Array();
    var botArray4 = new Array();
    var botArray3 = new Array();
    var botArray2 = new Array();
    var modArray3 = new Array();
    var modArray4 = new Array();
    var goodiesArray = new Array();
    for (let index = 0; index < crystalNumber; index++) {
        switch (crystalType) {
            case 'PBC':
                botType = weightedRand(spec_pbc);
                switch (botType) {
                    case '0':
                        botStar = 4;
                        poppedBot = getBot('4 star');
                        break;
                    case '1':
                        botStar = 3;
                        poppedBot = getBot('3 star');
                        break;
                    case '2':
                        botStar = 2;
                        poppedBot = getBot('2 star');
                        break;
                    default:
                        break;
                }
                break;
            case 'Monthly':
                botType = weightedRand(spec_monthly);
                switch (botType) {
                    case '0':
                        botStar = 5;
                        poppedBot = getBot('5 star');
                        break;
                    case '1':
                        botStar = 4;
                        poppedBot = getBot('4 star');
                        break;
                    case '2':
                        botStar = 3;
                        poppedBot = getBot('3 star');
                        break;
                    default:
                        break;
                }
                break;
            case 'Dark Matrix':
                botType = weightedRand(spec_matrix);
                switch (botType) {
                    case '0':
                        botStar = 5;
                        poppedBot = getBot('NP');
                        break;
                    case '1':
                        botStar = 4;
                        poppedBot = getBot('NP');
                        break;
                    case '2':
                        botStar = 4;
                        poppedBot = getBot('TC');
                        break;
                    case '3':
                        botStar = 5;
                        poppedBot = getBot('5 star');
                        break;
                    case '4':
                        botStar = 4;
                        poppedBot = getBot('4 star');
                        break;
                    case '5':
                        botStar = 3;
                        poppedBot = getBot('3 star');
                        break;
                    default:
                        break;
                }
                break;
            case 'Gold Wheel':
                botType = weightedRand(spec_wheel);
                switch (botType) {
                    case '0':
                        botStar = 5;
                        poppedBot = getBot('Bee');
                        break;
                    case '1':
                        botStar = 4;
                        poppedBot = getBot('Bee');
                        break;
                    case '2':
                        botStar = 5;
                        poppedBot = getBot('5 star');
                        break;
                    case '3':
                        botStar = 4;
                        poppedBot = getBot('4 star');
                        break;
                    case '4':
                        botStar = 3;
                        poppedBot = getBot('3 star');
                        break;
                    default:
                        break;
                }
                break;
            case 'Good as Gold':
                botType = weightedRand(spec_gag);
                switch (botType) {
                    case '0':
                        botStar = 4;
                        poppedBot = getBot('Bee');
                        break;
                    case '1':
                        botStar = 3;
                        poppedBot = getBot('Bee');
                        break;
                    case '2':
                        botStar = 4;
                        poppedBot = getBot('4 star');
                        break;
                    case '3':
                        botStar = 3;
                        poppedBot = getBot('3 star');
                        break;
                    case '4':
                        botStar = 2;
                        poppedBot = getBot('2 star');
                        break;
                    default:
                        break;
                }
                break;
            case 'Five Star':
                botStar = 5;
                poppedBot = getBot('5 star');
                break;
            case 'T3 Knight':
                botType = weightedRand(spec_t3k);
                // console.log('here goes: ' + botType);

                switch (botType) {
                    case '0':
                        botStar = 4;
                        poppedBot = getBot('4 star');
                        break;
                    case '1':
                        botStar = 3;
                        poppedBot = getBot('3 star');
                        break;
                    case '2':
                        botStar = '4m';
                        poppedBot = getBot('Mods');
                        break;
                    case '3':
                        botStar = '3m';
                        poppedBot = getBot('Mods');
                        break;
                    case '4':
                        botStar = 'others';
                        poppedBot = 'T1阿尔法火种';
                        break;
                    case '5':
                        botStar = 'others';
                        poppedBot = 'T3基础火种';
                        break;
                    case '6':
                        botStar = 'others';
                        poppedBot = '4星机器人水晶碎片（750）';
                        break;
                    case '7':
                        botStar = 'others';
                        poppedBot = 'T2阿尔法火种';
                        break;
                    default:
                        break;
                }
                break;
            case 'T4 Knight':
                botType = weightedRand(spec_t4k);
                switch (botType) {
                    case '0':
                        botStar = 'others';
                        poppedBot = getBot('t3c');
                        break;
                    case '1':
                        botStar = 4;
                        poppedBot = getBot('4 star');
                        break;
                    case '2':
                        botStar = '4m';
                        poppedBot = getBot('Mods');
                        break;
                    case '3':
                        botStar = 'others';
                        poppedBot = '5星机器人水晶碎片（2500）';
                        break;
                    case '4':
                        botStar = 5;
                        poppedBot = getBot('5 star');
                        break;
                    case '5':
                        botStar = 'others';
                        poppedBot = 'T4基础火种';
                        break;
                    case '6':
                        botStar = 'others';
                        poppedBot = 'T3阿尔法火种（精华）';
                        break;
                    default:
                        break;
                }
                break;
            default:
                break;
        }
        // console.log(botStar);
        // console.log(poppedBot);
        switch (botStar) {
            case 5:
                botArray5.push({ botStar: botStar + '星', bot: poppedBot });
                break;
            case 4:
                botArray4.push({ botStar: botStar + '星', bot: poppedBot });
                break;
            case 3:
                botArray3.push({ botStar: botStar + '星', bot: poppedBot });
                break;
            case 2:
                botArray2.push({ botStar: botStar + '星', bot: poppedBot });
                break;
            case '4m':
                modArray4.push({ botStar: '4星', bot: poppedBot });
                break;
            case '3m':
                modArray3.push({ botStar: '3星', bot: poppedBot });
                break;
            case 'others':
                goodiesArray.push({ botStar: '', bot: poppedBot });
                break;
            default:
                break;
        }
    }
    // console.log(botArray2.length);

    return [botArray5, botArray4, botArray3, botArray2, modArray4, modArray3, goodiesArray];
}

function showBots() {
    var crystalType = document.getElementById("crystal_type").value;
    var crsytalString;
    var nCrystals = 10;
    var botString = "", currentBot = "", complete_report = "";
    if (crystalType.indexOf("高等") > 0) {
        crsytalString = 'PBC';
    }

    if (crystalType.indexOf("土豪") > 0) {
        crsytalString = 'Monthly';
    }
    if (crystalType.indexOf("金轮") > 0) {
        crsytalString = 'Gold Wheel';
    }
    if (crystalType.indexOf("矩阵") > 0) {
        crsytalString = 'Dark Matrix';
    }
    if (crystalType.indexOf("乖巧") > 0) {
        crsytalString = 'Good as Gold';
    }
    if (crystalType.indexOf("5星水晶") > 0) {
        crsytalString = 'Five Star';
        nCrystals = 1;
    }
    if (crystalType.indexOf("三阶骑士") > 0) {
        crsytalString = 'T3 Knight';
    }
    if (crystalType.indexOf("四阶骑士") > 0) {
        crsytalString = 'T4 Knight';
        nCrystals = 1;
    }


    var spinResult = spinCrystal(crsytalString, nCrystals);
    // console.log(spinResult.botStar + '星' + spinResult.bot);
    // console.log(spinResult.length);
 
    for (let index = 0; index < spinResult.length; index++) {
        // console.log(spinResult[index].length);
        for (let jndex = 0; jndex < spinResult[index].length; jndex++) {
            currentBot = spinResult[index][jndex].botStar + spinResult[index][jndex].bot;
            allRewards.push(currentBot)
            botString = botString + currentBot + '<br />';
        }
    }
    document.getElementById("crystal_report").innerHTML = botString;

    totalCrystals += nCrystals;
    document.getElementById("nCrystal").innerHTML = '累计已开 <font color="red">' + totalCrystals + '</font> 个水晶';

    allRewards.sort();
    allRewards.reverse();
    let counts = {};
    allRewards.forEach(function (x) { counts[x] = (counts[x] || 0) + 1; });
    // var keynames = Object.keys(counts)
    // console.log(keynames);

    for (var name in counts) {
        let dummyTag = "";
        dummyTag += "(" + counts[name] + ")" + name + "\n";
        complete_report += dummyTag;
    }
    document.getElementById("complete_report").value = '累计获得：\n'+ complete_report;
}





