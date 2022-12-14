const fs = require("fs");
const { EOL } = require("os");

function range(from, to) {
  if (!to && to !== 0) return range(0, from);
  [from, to] = [from, to].map((n) => +n);
  return new Array(+to - +from + 1).fill(1).map((_, i) => +from + i);
}

function inputFileToArray(filename, separator = ",", mapFn) {
  const inputString = fs.readFileSync(filename).toString();
  const input = inputString.split(separator);
  return mapFn ? input.map(mapFn) : input;
}

const SAND_SPAWN_POSITION = [500, 0];

console.log("part 1: " + solve());
console.log("part 2: " + solve(true));

function solve(isPart2) {
  const map = inputToMap("input.txt");
  if (isPart2)
    map.push(
      new Array(map[0].length).fill("."),
      new Array(map[0].length).fill("#")
    );

  let unitsThatLanded = 0;
  while (true) {
    const [x, y, landed] = getSandLandingPos(map, SAND_SPAWN_POSITION);
    if (!landed) break;

    map[y][x] = "o";
    unitsThatLanded++;
  }

  return unitsThatLanded;
}

function inputToMap(inputFilename) {
  const rockPathStrings = inputFileToArray(inputFilename, EOL);
  const rockPathsVertices = rockPathStrings.map((path) =>
    path.split(" -> ").map((point) => point.split(",").map(Number))
  );
  const yMax = Math.max(
    ...rockPathsVertices.map((vertices) => vertices.map((v) => v[1])).flat()
  );

  const rockCoords = [];
  for (const vertices of rockPathsVertices) {
    for (let i = 1; i < vertices.length; i++) {
      rockCoords.push(...pointsToLinePoints(vertices[i - 1], vertices[i]));
    }
  }

  const map = new Array(yMax + 1)
    .fill([])
    .map(() => new Array(SAND_SPAWN_POSITION[0] * 2).fill("."));
  rockCoords.forEach(([x, y]) => (map[y][x] = "#"));
  return map;
}

function pointsToLinePoints(p1, p2) {
  const [x1, y1, x2, y2] = [...p1, ...p2];
  if (x1 === x2)
    return range(Math.min(y1, y2), Math.max(y1, y2)).map((y) => [x1, y]);
  if (y1 === y2)
    return range(Math.min(x1, x2), Math.max(x1, x2)).map((x) => [x, y1]);
  return [];
}

function getSandLandingPos(map, spawnPos) {
  let [x, y] = spawnPos;

  if (map[y][x] !== "." || !map[y + 1]) return [null, null, false]; // cant move

  const nextPos = [0, -1, 1] // pos to look at
    .map((dx) => [x + dx, y + 1])
    .find(([px, py]) => map[py][px] === ".");
  return nextPos ? getSandLandingPos(map, nextPos) : [x, y, true]; // use recursion to see next pos
}
