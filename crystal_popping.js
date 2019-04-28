'use strict';




function getBot(nStar) {
    var theBot;
    var list2 = ['碾碎器', '钢锁', '斗擎', '汽车大师', '雷震', '碎骨魔', '阿尔茜', '风刃', '路障', '横炮', '犀牛', '救护车', '幻影', '铁皮', '搅拌者', '战擎', '大黄蜂'];
    var list3 = ['碾碎器', '猩猩队长', '钢锁', '斗擎', '汽车大师', '野牛', '雷震', '探长', '碎骨魔', '漂移', '阿尔茜', '热破', '巨蝎勇士', '风刃', '路障', '横炮', '反冲', '警车', '爵士', '黄豹', '声波', '震荡波', '犀牛', '救护车', '幻影', '录音机', '千斤顶', '爆威', '黄蜂勇士', '铁皮', '喷气机', '惊破天', '搅拌者', '震天尊', '战威', '恐龙勇士', '战擎', '通天晓', '红蜘蛛', '狂飙'];
    var list4 = ['碾碎器', '猩猩队长', '钢锁', '斗擎', '汽车大师', '野牛', '雷震', '探长', '碎骨魔', '漂移', '阿尔茜', '热破', '巨蝎勇士', '风刃', '路障', '横炮', '反冲', '警车', '爵士', '黄豹', '声波', '震荡波', '犀牛', '救护车', '幻影', '录音机', '千斤顶', '爆威', '黄蜂勇士', '铁皮', '喷气机', '惊破天', '搅拌者', '震天尊', '战威', '恐龙勇士', '战擎', '通天晓', '红蜘蛛', '狂飙'];
    var list5 = ['碾碎器', '猩猩队长', '钢锁', '斗擎', '碎骨魔', '漂移', '阿尔茜', '热破', '路障', '反冲', '警车', '黄豹', '声波', '震荡波', '犀牛', '幻影', '爆威', '黄蜂勇士', '惊破天', '搅拌者', '战威', '恐龙勇士', '通天晓', '红蜘蛛'];
    var listBee = ['大黄蜂', '小黄蜂'];
    // console.log(nStar);

    switch (nStar) {
        case 2:
            theBot = list2[Math.floor(Math.random() * list2.length)]

            break;
        case 3:
            theBot = list3[Math.floor(Math.random() * list3.length)]
            break;
        case 4:
            theBot = list4[Math.floor(Math.random() * list2.length)]
            break;
        case 5:
            theBot = list5[Math.floor(Math.random() * list2.length)]
            break;
        case 6:
            theBot = listBee[Math.floor(Math.random() * listBee.length)]
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
    var spec_pbc = { 0: 0.01, 1: 0.26, 2: 0.73 }; // 4, 3, 2 star
    var spec_monthly = { 0: 0.015, 1: 0.135, 2: 0.85 }; // 5, 4, 3 star
    var spec_wheel = { 0: 0.01, 1: 0.02, 2: 0.01, 3: 0.12, 4: 0.84 };  // 5 Bee, 4 Bee, 5, 4, 3, star
    var spec_gag = { 0: 0.0075, 1: 0.0551, 2: 0.0075, 3: 0.2049, 4: 0.725 }; // 4 Bee, 3 Bee, 4, 3, 2 star
    var botArray5 = new Array();
    var botArray4 = new Array();
    var botArray3 = new Array();
    var botArray2 = new Array();

    for (let index = 0; index < crystalNumber; index++) {


        switch (crystalType) {
            case 'PBC':
                botType = weightedRand(spec_pbc);
                switch (botType) {
                    case '0':
                        botStar = 4;
                        poppedBot = getBot(4);
                        break;
                    case '1':
                        botStar = 3;
                        poppedBot = getBot(3);
                        break;
                    case '2':
                        botStar = 2;
                        poppedBot = getBot(2);
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
                        poppedBot = getBot(5);
                        break;
                    case '1':
                        botStar = 4;
                        poppedBot = getBot(4);
                        break;
                    case '2':
                        botStar = 3;
                        poppedBot = getBot(3);
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
                        poppedBot = getBot(6);
                        break;
                    case '1':
                        botStar = 4;
                        poppedBot = getBot(6);
                        break;
                    case '2':
                        botStar = 5;
                        poppedBot = getBot(5);
                        break;
                    case '3':
                        botStar = 4;
                        poppedBot = getBot(4);
                        break;
                    case '4':
                        botStar = 3;
                        poppedBot = getBot(3);
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
                        poppedBot = getBot(6);
                        break;
                    case '1':
                        botStar = 3;
                        poppedBot = getBot(6);
                        break;
                    case '2':
                        botStar = 4;
                        poppedBot = getBot(4);
                        break;
                    case '3':
                        botStar = 3;
                        poppedBot = getBot(3);
                        break;
                    case '4':
                        botStar = 2;
                        poppedBot = getBot(2);
                        break;
                    default:
                        break;
                }
                break;
            case 'Five Star':
                botStar = 5;
                poppedBot = getBot(5);
                break;
            default:
                break;
        }
        // console.log(botStar);
        // console.log(poppedBot);
        switch (botStar) {
            case 5:
                botArray5.push({ botStar: botStar, bot: poppedBot });
                break;
            case 4:
                botArray4.push({ botStar: botStar, bot: poppedBot });
                break;
            case 3:
                botArray3.push({ botStar: botStar, bot: poppedBot });
                break;
            case 2:
                botArray2.push({ botStar: botStar, bot: poppedBot });
                break;
            default:
                break;
        }
    }
    // console.log(botArray2.length);

    return [botArray5, botArray4, botArray3, botArray2];
}

function showBots() {
    var crystalType = document.getElementById("crystal_type").value;
    var crsytalString;
    var nCrystals = 10;
    var botString = "", currentBot = "";
    if (crystalType.indexOf("高等") > 0) {
        crsytalString = 'PBC';
    }

    if (crystalType.indexOf("土豪") > 0) {
        crsytalString = 'Monthly';
    }
    if (crystalType.indexOf("金轮") > 0) {
        crsytalString = 'Gold Wheel';
    }
    if (crystalType.indexOf("乖巧") > 0) {
        crsytalString = 'Good as Gold';
    }
    if (crystalType.indexOf("5星水晶") > 0) {
        crsytalString = 'Five Star';
        nCrystals = 1;
    }

    var spinResult = spinCrystal(crsytalString, nCrystals);
    // console.log(spinResult.botStar + '星' + spinResult.bot);
    // console.log(spinResult.length);

    for (let index = 0; index < spinResult.length; index++) {
        // console.log(spinResult[index].length);
        for (let jndex = 0; jndex < spinResult[index].length; jndex++) {
            currentBot = spinResult[index][jndex].botStar + '星 - ' + spinResult[index][jndex].bot;
            botString = botString + currentBot + '<br />';
        }
    }
    document.getElementById("crystal_report").innerHTML = botString;
}





