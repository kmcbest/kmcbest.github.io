
bot_star = 5
bot_rank = 4
bot_level = 40


// console.log(fdata[bot_star.toString()][bot_rank.toString()][bot_level - 1]);
const fs = require('fs')

// fs.readFile('forgeData.json', (err, data) => {
//     if (err) throw err;

//     global.forgeData = JSON.parse(data.toString());
//     console.log(global.forgeData["5"]);
// })

var forgeData = JSON.parse(fs.readFileSync('forgeData.json').toString());

currentCoeff = 0.978735143;
function mergeProperty(obj1, obj2) {
    for (var k in obj2) {
        if (k in obj1) {
            obj1[k] += obj2[k];
        } else {
            obj1[k] = obj2[k];
        }
    }
}

function calcGold(botStar, botRank, botLevel, forgeData) {
    var totalGold = 0;
    for (let i = 1; i <= botRank; i++) {
        if (i < botRank) {
            finalLevel = forgeData[botStar.toString()][i.toString()].cost.length;
        } else {
            finalLevel = botLevel;
        }
        for (let j = 0; j < finalLevel; j++) {
            if (forgeData[botStar.toString()][i.toString()].coeff[j] == 1) {
                totalGold += forgeData[botStar.toString()][i.toString()].cost[j] * forgeData[botStar.toString()][i.toString()].coeff[j];
            } else {
                totalGold += forgeData[botStar.toString()][i.toString()].cost[j] * eval(forgeData[botStar.toString()][i.toString()].coeff[j]);
            }
        }
    }
    return totalGold;
}

function calcSparks(botStar, botRank, forgeData) {
    var finalSparks = {};
    for (let i = 1; i <= botRank; i++) {
        mergeProperty(finalSparks, forgeData[botStar.toString()][i.toString()].sparks);
    }
    return finalSparks;
}




var c = calcSparks(4, 5, forgeData);
var d = Math.floor(calcGold(4,5,50,forgeData));
// console.log(c);

console.log(JSON.stringify(c));

console.log(d);



// const fetch = require("node-fetch");

// // console.log(forgeData);
// fetch('forgedData.json')
//   .then(response => response.json())
//   .then(jsonResponse => console.log(jsonResponse))  

