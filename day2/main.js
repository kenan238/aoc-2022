// aoc 2022 day 2

const { createReadStream } = require('fs');
const { createInterface } = require('readline');

const opponentChoiceTable = {
  'A': 'rock',
  'B': 'paper',
  'C': 'scissors',
}; // figure out opponent choice

const bestChoiceChoiceTable = {
  'X': 'rock',
  'Y': 'paper',
  'Z': 'scissors',
}; // figure out best response

const awardAmounts = {
  'rock': 1,
  'paper': 2,
  'scissors': 3
}; // award amounts to give

const whatBeatsWhat = {
  'rock': 'scissors',
  'paper': 'rock',
  'scissors': 'paper',
}; // for func getWhoWon

const secondColumnDecrypt = {
  'X': 'lose',
  'Y': 'draw',
  'Z': 'win',
}; // to actually decrypt second column

const bestResponseToLose = {
  'rock': 'scissors',
  'paper': 'rock',
  'scissors': 'paper'
}; // to lose

const bestResponseToWin = {
  'rock': 'paper',
  'paper': 'scissors',
  'scissors': 'rock',
}; // to win

function getWhoWon(opponent, self) {
  if (whatBeatsWhat[opponent] == self)
    return 'opponent';
  if (whatBeatsWhat[self] == opponent)
    return 'self';
  if (opponent == self)
    return 'draw';
}

function getAdditionalAmount(opponent, self) {
  const whoWon = getWhoWon(opponent, self);
  const amountLookup = {
    'opponent': 0,
    'draw': 3,
    'self': 6,
  };

  return amountLookup[whoWon];
}

function figureOutResponse(whatShouldDo, opponent) {
  if (whatShouldDo == 'lose') return bestResponseToLose[opponent];
  if (whatShouldDo == 'draw') return opponent;
  if (whatShouldDo == 'win') return bestResponseToWin[opponent];
}

async function process() {
  const fStream = createReadStream('input.txt');
  const rl = createInterface({
    input: fStream,
    crlfDelay: Infinity
  });

  let score = 0;
  let actualScore = 0;

  for await (const line of rl) {
    const opponent = opponentChoiceTable[line[0]];
    const bestChoice = bestChoiceChoiceTable[line[2]];
    const award = awardAmounts[bestChoice];
    const additional = getAdditionalAmount(opponent, bestChoice);
    score += award + additional;

    // part 2

    const whatShouldDo = secondColumnDecrypt[line[2]];
    const bestResponse = figureOutResponse(whatShouldDo, opponent);
    const award2 = awardAmounts[bestResponse];
    const additional2 = getAdditionalAmount(opponent, bestResponse);
    actualScore += award2 + additional2;
  }

  console.log('Score with our technique       ', score);
  console.log('Score with the proper technique', actualScore);
}

process();