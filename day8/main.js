const { createReadStream } = require('fs');
const { createInterface } = require('readline');


const computeEdges = (x, y, grid) => {
  const edges = [
    grid[y].slice(0, x),
    grid.map(row => row[x]).slice(0, y),
    grid[y].slice(x + 1),
    grid.map(row => row[x]).slice(y + 1),
  ];

  return edges;
};

const isVisible = (x, y, grid) => {
  const edges = computeEdges(x, y, grid);
  return edges.some(dir => dir.every(tree => tree < grid[y][x]));
};

const computeScenicScore = (x, y, grid) => {
  const edges = [
    grid[y].slice(0, x).reverse(),
    grid.map(row => row[x]).slice(0, y).reverse(), // can't use compute edges here because of .reverse()
    grid[y].slice(x + 1),
    grid.map(row => row[x]).slice(y + 1),
  ];

  const result = edges.map(edge => {
    const tallerTree = edge.findIndex(tree => tree >= grid[y][x]);
    if (tallerTree === -1) 
      return edge.length;
    return tallerTree + 1;
  });

  return result.reduce((a, b) => a * b)
};

async function process() {
  const fStream = createReadStream('input.txt');
  const rl = createInterface({
    input: fStream,
    crlfDelay: Infinity
  });

  let visibleTrees = 0;
  let grid = [];
  let highestScenicScore = 0;

  for await (const line of rl) {
    const treesForLine = line.split('').map(x => parseInt(x));
    grid.push(treesForLine);
  }

  // note for self
  // i/k == y
  // j/l == x
  for (let i = 0; i < grid.length; i++) {
    const gridLine = grid[i];
    for (let j = 0; j < gridLine.length; j++) {
      if (isVisible(i, j, grid)) visibleTrees++;
      const score = computeScenicScore(i, j, grid);
      highestScenicScore = Math.max(score, highestScenicScore);
    }
  }

  console.log('Visible trees       ', visibleTrees);
  console.log('Highest scenic score', highestScenicScore);
}

process();