interface Vector2 {
  x: number;
  y: number;
}

const quickVec2 = (x: number, y: number): Vector2 => 
  ({ x, y });

const addVec2 = (v1: Vector2, v2: Vector2) =>
  ({ x: v1.x + v2.x, y: v1.y + v2.y });

const subsVec2 = (v1: Vector2, v2: Vector2) =>
  ({ x: v1.x - v2.x, y: v1.y - v2.y });

const mulVec2 = (v1: Vector2, v2: number) =>
  ({ x: v1.x * v2, y: v1.y * v2 });

const clamp = (number: number, min: number, max: number) =>
  Math.max(min, Math.min(number, max));

const oneify = (v: Vector2) => {
  // im tired
  return {
    x: clamp(v.x, -1, 1),
    y: clamp(v.y, -1, 1)
  };
};

let head: Vector2 = { x: 25, y: 5 };
let tails: Array<Vector2> = Array(9).fill(head);
let visitedPositions: Array<Vector2> = [];

const vecUp = quickVec2(0, -1);
const vecDown = quickVec2(0, 1);
const vecLeft = quickVec2(-1, 0);
const vecRight = quickVec2(1, 0);

const shallowEqual = (object1: any, object2: any) => {
  const keys1 = Object.keys(object1);
  const keys2 = Object.keys(object2);
  if (keys1.length !== keys2.length)
    return false;
  for (const key of keys1) {
    if (object1[key] !== object2[key]) {
      return false;
    }
  }
  return true;
}

const moveTail = (tail: Vector2, head: Vector2): Vector2 => {
  if (findDistance(tail, head) > 1.5) {
    const dir = oneify(subsVec2(head, tail));
    tail = addVec2(tail, dir);
    if (!visitedPositions.some(x => x.x == tail.x && x.y == tail.y)) {
      visitedPositions.push(tail);
    }
  }

  return tail;
};

function findDistance(a: Vector2, b: Vector2) {
  const f = a.x - b.x;
  const g = a.y - b.y;  

  return Math.sqrt(f*f + g*g);
}

const visualizeGrid = () => {
  const WIDTH = 50;
  const HEIGHT = 10;

  for (let y = 0; y < HEIGHT; y++) {
    for (let x = 0; x < WIDTH; x++) {
      if (shallowEqual(head, quickVec2(x, y)))
        Deno.writeAllSync(Deno.stdout, new TextEncoder().encode('H'));
      const idx = tails.findIndex(h => shallowEqual(h, quickVec2(x, y)));
      if (idx != -1)
        Deno.writeAllSync(Deno.stdout, new TextEncoder().encode(idx.toString()));
      if (visitedPositions.some(h => shallowEqual(h, quickVec2(x, y))))
        Deno.writeAllSync(Deno.stdout, new TextEncoder().encode('#'));
      else
        Deno.writeAllSync(Deno.stdout, new TextEncoder().encode('.'));
    }
    console.log();
  }
};


const lines = Deno.readTextFileSync("input.txt").split("\r\n");

for (const line of lines) {
  const [dir, amtStr] = line.split(" ");
  const amt = parseInt(amtStr);
  
  visualizeGrid();

  let vecDir = quickVec2(0, 0);
  switch (dir) {
    case 'U':
      vecDir = vecUp;
      break;
    case 'D':
      vecDir = vecDown;
      break;
    case 'R':
      vecDir = vecRight;
      break;
    case 'L':
      vecDir = vecLeft;
      break;
  }

  for (let i = 0; i < amt; i++) {
    let headPrevious: Vector2 = head;
    head = addVec2(head, vecDir);

    // eh it works
    tails[0] = moveTail(tails[0], head);
    tails[1] = moveTail(tails[1], tails[0]);
    tails[2] = moveTail(tails[2], tails[1]);
    tails[3] = moveTail(tails[3], tails[2]); 
    tails[4] = moveTail(tails[4], tails[3]);
    tails[5] = moveTail(tails[5], tails[4]);
    tails[6] = moveTail(tails[6], tails[5]);
    tails[7] = moveTail(tails[7], tails[6]);
    tails[8] = moveTail(tails[8], tails[7]);
  }

  console.log(line, vecDir, amt);
  prompt('press key');
  
  console.clear();
}

visualizeGrid();
console.log('Final grid');
console.log('Visited positions ', visitedPositions.length);

// part 2 ans is 2643

// couldnt bother to solve this though
// was too tired
// better luck tomorrow on day 10