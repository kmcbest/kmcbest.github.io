'use strict';
var isShark = true;
var isBot = false;
var isFodder = true;
function Level_exp(isShark, nStar, nRank, nLevel, nSig, fBonus) {
    var nExp = 0;
    if (isShark === true) {
        if (nStar === 2) {
            if (nRank === 1) {
                nExp = 62 * nSig + (168 + 18 * (nLevel - 1)) * fBonus;
            }
            else {
                if (nRank === 2) {
                    nExp = 62 * nSig + (283 + 42 * (nLevel - 1)) * fBonus;
                }
                else {
                    nExp = 62 * nSig + (739 + 76 * (nLevel - 1)) * fBonus;
                }
            }
        }
        else {
            if (nStar === 3) {
                if (nRank === 1) {
                    nExp = 440 * nSig + (1144 + 24 * (nLevel - 1)) * fBonus;
                }
                else {
                    if (nRank === 2) {
                        nExp = 440 * nSig + (1350 + 100 * (nLevel - 1)) * fBonus;
                    }
                    else {
                        if (nRank === 3) {
                            nExp = 440 * nSig + (2415 + 140 * (nLevel - 1)) * fBonus;
                        }
                        else {
                            nExp = 440 * nSig + (4683 + 240 * (nLevel - 1)) * fBonus;
                        }
                    }
                }
            }
            else {
                if (nStar === 4) {
                    if (nRank === 1) {
                        nExp = 2200 * nSig + (6880 + 160 * (nLevel - 1)) * fBonus;
                    }
                    else {
                        if (nRank === 2) {
                            nExp = 2200 * nSig + (7834 + 200 * (nLevel - 1)) * fBonus;
                        }
                        else {
                            if (nRank === 3) {
                                nExp = 2200 * nSig + (10144 + 340 * (nLevel - 1)) * fBonus;
                            }
                            else {
                                if (nRank === 4) {
                                    nExp = 2200 * nSig + (15884 + 580 * (nLevel - 1)) * fBonus;
                                }
                                else {
                                    nExp = 2200 * nSig + (29768 + 1504 * (nLevel - 1)) * fBonus;
                                }
                            }
                        }
                    }
                }
            }
        }
    }
    else {
        if (nStar === 1) {
            if (nRank === 1) {
                nExp = (15 + 5 * (nLevel - 1)) * fBonus;
            }
            else {
                if (nRank === 2) {
                    nExp = (67 + 7.5 * (nLevel - 1)) * fBonus;
                }
            }
        }
        else {
            if (nStar === 2) {
                if (nRank === 1) {
                    nExp = 31 * nSig + (159 + 9 * (nLevel - 1)) * fBonus;
                }
                else {
                    if (nRank === 2) {
                        nExp = 31 * nSig + (262 + 21 * (nLevel - 1)) * fBonus;
                    }
                    else {
                        nExp = 31 * nSig + (699 + 38 * (nLevel - 1)) * fBonus;
                    }
                }
            }
            else {
                if (nStar === 3) {
                    if (nRank === 1) {
                        nExp = 220 * nSig + (1132 + 12 * (nLevel - 1)) * fBonus;
                    }
                    else {
                        if (nRank === 2) {
                            nExp = 220 * nSig + (1300 + 50 * (nLevel - 1)) * fBonus;
                        }
                        else {
                            if (nRank === 3) {
                                nExp = 220 * nSig + (2343 + 70 * (nLevel - 1)) * fBonus;
                            }
                            else {
                                nExp = 220 * nSig + (4563 + 120 * (nLevel - 1)) * fBonus;
                            }
                        }
                    }
                }
                else {
                    if (nStar === 4) {
                        if (nRank === 1) {
                            nExp = 1100 * nSig + (6800 + 80 * (nLevel - 1)) * fBonus;
                        }
                        else {
                            if (nRank === 2) {
                                nExp = 1100 * nSig + (7734 + 100 * (nLevel - 1)) * fBonus;
                            }
                            else {
                                if (nRank === 3) {
                                    nExp = 1100 * nSig + (9974 + 170 * (nLevel - 1)) * fBonus;
                                }
                                else {
                                    if (nRank === 4) {
                                        nExp = 1100 * nSig + (15594 + 290 * (nLevel - 1)) * fBonus;
                                    }
                                    else {
                                        nExp = 1100 * nSig + (29016 + 752 * (nLevel - 1)) * fBonus;
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
    }
    return Math.ceil(nExp);
}


// console.log(Level_exp(false, 4, 5, 50, 100, 1));

{
    var arrLevel = Array.from(new Array(101), (val, index) => index);

    var arrPts_2 = [5, 5, 8, 11, 13, 15, 17, 18, 20, 22, 23, 24, 26, 27, 28, 29, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 43, 45, 46, 47, 48, 48, 48, 50, 51, 52, 53, 53, 54, 55, 56, 57, 57, 58, 59, 60, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0];
    var arrCumul_2 = [5, 10, 18, 29, 42, 57, 74, 92, 112, 134, 157, 181, 207, 234, 262, 291, 322, 354, 387, 421, 456, 492, 529, 567, 606, 646, 687, 729, 772, 815, 860, 906, 953, 1001, 1049, 1097, 1147, 1198, 1250, 1303, 1356, 1410, 1465, 1521, 1578, 1635, 1693, 1752, 1812, 1812, 1812, 1812, 1812, 1812, 1812, 1812, 1812, 1812, 1812, 1812, 1812, 1812, 1812, 1812, 1812, 1812, 1812, 1812, 1812, 1812, 1812, 1812, 1812, 1812, 1812, 1812, 1812, 1812, 1812, 1812, 1812, 1812, 1812, 1812, 1812, 1812, 1812, 1812, 1812, 1812, 1812, 1812, 1812, 1812, 1812, 1812, 1812, 1812, 1812, 1812, 1812];

    var arrPts_3 = [42, 42, 64, 81, 97, 111, 124, 136, 147, 158, 168, 178, 188, 197, 206, 215, 223, 232, 240, 248, 255, 263, 270, 278, 285, 292, 299, 306, 313, 319, 326, 332, 339, 345, 351, 357, 364, 370, 376, 381, 387, 393, 399, 405, 410, 416, 421, 427, 432, 438, 443, 448, 453, 459, 464, 469, 474, 479, 484, 489, 494, 499, 504, 509, 514, 519, 523, 528, 533, 537, 542, 547, 551, 556, 561, 565, 570, 574, 579, 583, 587, 592, 596, 600, 605, 609, 613, 618, 622, 626, 630, 635, 639, 643, 647, 651, 655, 659, 663, 668, 672];
    var arrCumul_3 = [42, 84, 148, 229, 326, 437, 561, 697, 844, 1002, 1170, 1348, 1536, 1733, 1939, 2154, 2377, 2609, 2849, 3097, 3352, 3615, 3885, 4163, 4448, 4740, 5039, 5345, 5658, 5977, 6303, 6635, 6974, 7319, 7670, 8027, 8391, 8761, 9137, 9518, 9905, 10298, 10697, 11102, 11512, 11928, 12349, 12776, 13208, 13646, 14089, 14537, 14990, 15449, 15913, 16382, 16856, 17335, 17819, 18308, 18802, 19301, 19805, 20314, 20828, 21347, 21870, 22398, 22931, 23468, 24010, 24557, 25108, 25664, 26225, 26790, 27360, 27934, 28513, 29096, 29683, 30275, 30871, 31471, 32076, 32685, 33298, 33916, 34538, 35164, 35794, 36429, 37068, 37711, 38358, 39009, 39664, 40323, 40986, 41654, 42326];

    var arrPts_4 = [254, 254, 385, 492, 584, 668, 745, 818, 886, 951, 1013, 1072, 1130, 1185, 1239, 1292, 1343, 1393, 1441, 1489, 1535, 1581, 1626, 1670, 1713, 1755, 1797, 1838, 1879, 1919, 1958, 1997, 2036, 2074, 2111, 2148, 2185, 2221, 2257, 2292, 2327, 2362, 2396, 2431, 2464, 2498, 2531, 2564, 2596, 2629, 2661, 2693, 2724, 2755, 2787, 2817, 2848, 2878, 2909, 2939, 2968, 2998, 3027, 3057, 3086, 3114, 3143, 3172, 3200, 3228, 3256, 3284, 3312, 3339, 3367, 3394, 3421, 3448, 3475, 3501, 3528, 3554, 3580, 3607, 3633, 3658, 3684, 3710, 3735, 3761, 3786, 3811, 3836, 3861, 3886, 3911, 3936, 3960, 3985, 4009, 4033];
    var arrCumul_4 = [254, 508, 893, 1385, 1969, 2637, 3382, 4200, 5086, 6037, 7050, 8122, 9252, 10437, 11676, 12968, 14311, 15704, 17145, 18634, 20169, 21750, 23376, 25046, 26759, 28514, 30311, 32149, 34028, 35947, 37905, 39902, 41938, 44012, 46123, 48271, 50456, 52677, 54934, 57226, 59553, 61915, 64311, 66742, 69206, 71704, 74235, 76799, 79395, 82024, 84685, 87378, 90102, 92857, 95644, 98461, 101309, 104187, 107096, 110035, 113003, 116001, 119028, 122085, 125171, 128285, 131428, 134600, 137800, 141028, 144284, 147568, 150880, 154219, 157586, 160980, 164401, 167849, 171324, 174825, 178353, 181907, 185487, 189094, 192727, 196385, 200069, 203779, 207514, 211275, 215061, 218872, 222708, 226569, 230455, 234366, 238302, 242262, 246247, 250256, 254289];

    var arrPts_5 = [1928, 1928, 2923, 3728, 4431, 5066, 5651, 6199, 6716, 7208, 7678, 8130, 8566, 8987, 9396, 9793, 10180, 10557, 10925, 11286, 11638, 11984, 12323, 12656, 12984, 13306, 13623, 13935, 14242, 14545, 14844, 15139, 15430, 15718, 16002, 16282, 16560, 16834, 17106, 17375, 17641, 17904, 18165, 18423, 18679, 18932, 19184, 19433, 19680, 19925, 20168, 20409, 20648, 20886, 21121, 21355, 21587, 21818, 22046, 22274, 22499, 22724, 22946, 23168, 23388, 23606, 23824, 24040, 24254, 24468, 24680, 24891, 25100, 25309, 25517, 25723, 25928, 26132, 26355, 26537, 26738, 26939, 27318, 27336, 27533, 27729, 27924, 28119, 28312, 28505, 28696, 28887, 29077, 29267, 29455, 29643, 29830, 30016, 30201, 30385, 30569];
    var arrCumul_5 = [1928, 3856, 6779, 10507, 14938, 20004, 25655, 31854, 38570, 45778, 53456, 61586, 70152, 79139, 88535, 98328, 108508, 119065, 129990, 141276, 152914, 164898, 177221, 189877, 202861, 216167, 229790, 243725, 257967, 272512, 287356, 302495, 317925, 333643, 349645, 365927, 382487, 399321, 416427, 433802, 451443, 469347, 487512, 505935, 524614, 543546, 562730, 582163, 601843, 621768, 641936, 662345, 682993, 703879, 725000, 746355, 767942, 789760, 811806, 834080, 856579, 879303, 902249, 925417, 948805, 972411, 996235, 1020275, 1044529, 1068997, 1093677, 1118568, 1143668, 1168977, 1194494, 1220217, 1246145, 1272277, 1298632, 1325169, 1351907, 1378846, 1406164, 1433500, 1461033, 1488762, 1516686, 1544805, 1573117, 1601622, 1630318, 1659205, 1688282, 1717549, 1747004, 1776647, 1806477, 1836493, 1866694, 1897079, 1927648];


    var fd2 = {
        tier: 2,
        level: arrLevel,
        pts: arrPts_2,
        cumul: arrCumul_2
    };
    var fd3 = {
        tier: 3,
        level: arrLevel,
        pts: arrPts_3,
        cumul: arrCumul_3
    };
    var fd4 = {
        tier: 4,
        level: arrLevel,
        pts: arrPts_4,
        cumul: arrCumul_4
    };
    var fd5 = {
        tier: 5,
        level: arrLevel,
        pts: arrPts_5,
        cumul: arrCumul_5
    };
    var fd = [fd2, fd3, fd4, fd5];
}
// console.log(fd[3].cumul[40]);

function Forge_Remain_exp(nTier, nForge, nRemain, isFodder) {
    var nExp = 0;
    if (nForge > 0) {
        if (isFodder === true) { // If the bot serves as fodder, the pts from level 0 should be removed.
            nExp = fd[nTier - 2].cumul[nForge - 1] + nRemain - fd[nTier - 2].pts[0];
        } else {
            nExp = fd[nTier - 2].cumul[nForge - 1] + nRemain; //otherwise it's calculated directly through the cumulative value.
        }
    } else {
        nExp = nRemain;
    }
    return nExp;
}
function Forge_Result(nTier, nExp) {
    var nLevel = 0;
    var currentExp = 0;
    if (nExp < fd[nTier - 2].pts[0]) {
        var result = {
            targetLevel: 0,
            remainingExp: nExp
        };
    }
    else {
        while (nExp > currentExp) {
            nLevel = nLevel + 1;
            currentExp = fd[nTier - 2].cumul[nLevel];
            // console.log(currentExp);
        }
        var result = {
            targetLevel: nLevel,
            remainingExp: nExp - fd[nTier - 2].cumul[nLevel - 1]
        };
    }
    return result;
}

function Forge_shards(isShark, nTier, nRank, nLevel, nSig) {
    var nShards;

    if (isShark === true) {
        if (nRank < 4) {
            nShards = 300 + nRank * 100 + nLevel + nSig * 80;
        } else {
            if (nRank === 4) {
                nShards = 600 + nRank * 100 + nLevel + nSig * 80;
            }
            else {
                if (nRank === 5) {
                    nShards = 1100 + nRank * 100 + nLevel + nSig * 80;
                }
            }
        }

    } else {
        nShards = (2 * nTier * nTier - 10 * nTier + 13) * (7.5 * nRank * nRank - 12.5 * nRank + 25 + 1 * nLevel + 11 * nSig);

    }
    return nShards;
}


function check() {
    var isShark;
    var strShark;
    var strReport = "";
    var nFodderName = document.getElementById("fodder_name").value;
    var nReceiverName = document.getElementById("receiver_name").value;
    var bonus = 1.0;
    var strBonus = "";
    if (nFodderName.indexOf("饿鲨") > 0) {
        isShark = true;
        strShark = "饿鲨碎片";
    } else {
        isShark = false;
        strShark = "机器人碎片";
    }
    if (nFodderName.substring(0, 2) === nReceiverName.substring(0, 2)) {
        bonus = 1.1;
        strBonus = `（享受同类别加成${bonus}）`;
    }
    if (nFodderName === nReceiverName) {
        bonus = 1.2;
        strBonus = `（享受同人物加成${bonus}）`;
    }


    var nFodderStar = Number(document.getElementById("fodder_star").value);
    var nFodderRank = Number(document.getElementById("fodder_rank").value);
    var nFodderLevel = Number(document.getElementById("fodder_level").value);

    var nFodderSig = Number(document.getElementById("fodder_sig").value);
    var nFodderForge = Number(document.getElementById("fodder_forgelevel").value);
    var nFodderRemainExp = Number(document.getElementById("fodder_remain_exp").value);

    var nReceiverStar = Number(document.getElementById("receiver_star").value);
    var nReceiverForge = Number(document.getElementById("receiver_forge").value);
    var nReceiverRemain = Number(document.getElementById("receiver_remain_exp").value);

    // alert(Level_exp(isShark,nFodderStar,nFodderRank,nFodderLevel, nFodderSig, bonus));
    // var result=Level_exp(false,nFodderStar,nFodderRank,nFodderLevel, nFodderSig, bonus);
    // console.log(Level_exp(isShark, nFodderStar, nFodderRank, nFodderLevel, nFodderSig, 1));
    var fodderFinalExp = Level_exp(isShark, nFodderStar, nFodderRank, nFodderLevel, nFodderSig, bonus) + Forge_Remain_exp(nFodderStar, nFodderForge, nFodderRemainExp, isFodder);
    var receiverInitialExp = Forge_Remain_exp(nReceiverStar, nReceiverForge, nReceiverRemain, isBot);
    var new_exp = receiverInitialExp + fodderFinalExp;
    var result = Forge_Result(nReceiverStar, new_exp);

    var shards = Forge_shards(isShark, nFodderStar, nFodderRank, nFodderLevel, nFodderSig);
    strReport = `接受锻造者<strong>${nReceiverStar}星${nReceiverName}</strong>初始锻造经验为：${receiverInitialExp}<br />锻造狗粮<strong>${nFodderStar}星${nFodderName}</strong>产生${fodderFinalExp}点经验${strBonus}，最终总经验为：${new_exp}<br />接受锻造者变为<br />锻造等级：${result.targetLevel}<br />剩余经验：${result.remainingExp}<br />碎片奖励：${shards} ${nFodderStar + 1}星${strShark}。`
    if (nFodderRank > nFodderStar + 1) {
        strReport = `错误：${nFodderStar}星机器人不可能达到${nFodderRank}阶！`;
    }
    if (nFodderLevel > nFodderRank * 10) {
        strReport = `错误：${nFodderRank}阶最大等级为${nFodderRank * 10}！`;
    }
    if (nFodderStar>nReceiverStar-1){
        strReport = `错误：不能用${nFodderStar}星机器人喂给${nReceiverStar}星！`;
    }
    document.getElementById("forge_report").innerHTML = strReport;
    // console.log(Level_exp(isShark, nFodderStar, nFodderRank, nFodderLevel, nFodderSig, 1));
    // console.log(shards);
}

// console.log(Level_exp(false, 2, 1, 1, 0, 1));
// var new_exp = Level_exp(isShark, 3, 4, 40, 100, 1.0) + Forge_Remain_exp(3, 0, 15, isFodder) + Forge_Remain_exp(5, 0, 0, isBot);
// console.log(new_exp);
// var result = Forge_Result(5, new_exp);

// console.log('Final level: ' + result.targeLevel);
// console.log('Remaining Exp: ' + result.remainingExp);




