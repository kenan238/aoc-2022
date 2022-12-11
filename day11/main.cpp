#include <iostream>
#include <string>
#include <vector>
#include <math.h>
#include <algorithm>
#include <numeric>
#include <assert.h>

enum OpType {
  DIVIDE,
  ADD,
  SUBSTRACT,
  MULTIPLY
};

struct OldOrInteger {
  bool replaceWithOld;
  int value;
};

// #define DEBUG


size_t moduloDivisor { 0 };

class Operation {
public:
  OldOrInteger a, b;
  OpType type;

  Operation(bool isAold, int aValue, bool isBold, int bValue, OpType oType) {
    this->a.replaceWithOld = isAold;
    this->a.value = aValue;

    this->b.replaceWithOld = isBold;
    this->b.value = bValue;

    this->type = oType;
  }

  int calculate(int oldValue) {
    int aValue = this->a.replaceWithOld ? oldValue : a.value;
    int bValue = this->b.replaceWithOld ? oldValue : b.value;

    switch (this->type) {
      case DIVIDE:
        return (aValue * bValue) % moduloDivisor;
      case ADD:
        return (aValue + bValue) % moduloDivisor;
      case SUBSTRACT:
        return (aValue - bValue) % moduloDivisor;
      case MULTIPLY:
        return (aValue * bValue) % moduloDivisor;
    }

    assert(false);
  }
};

struct InspectionResult {
  size_t worryValue;
  int monkeyIndex;
};


class Monkey {
private:
  Operation op;
  int whatMonkeyToThrowToIfTrue;
  int whatMonkeyToThrowToIfFalse;
public:
  std::vector<size_t> startingItems;
  size_t inspectionCount = 0;
  size_t testDivisor;

  Monkey(std::vector<size_t> _startingItems, int _testDivisor, int _monkeyTrue, int _monkeyFalse, Operation _op) :
    startingItems(_startingItems), testDivisor(_testDivisor), 
    whatMonkeyToThrowToIfTrue(_monkeyTrue), whatMonkeyToThrowToIfFalse(_monkeyFalse), op(_op) {}

  void add(size_t item) {
    this->startingItems.push_back(item);
  }

  void modifyOp(Operation newOp) {
    this->op = newOp;
  }

  std::vector<size_t> getStartingItems() {
    return this->startingItems;
  }

  InspectionResult inspect() {
    inspectionCount++;
    size_t poppedItem = this->startingItems.front();
    this->startingItems.erase(this->startingItems.begin());
#ifdef DEBUG
    std::cout << "--Monkey inspects an item with a worry level of " << poppedItem << std::endl;
#endif
    InspectionResult res;
    res.worryValue = this->op.calculate(poppedItem);
#ifdef DEBUG
    std::cout << "Worry level is " << res.worryValue << " coming from " << poppedItem << std::endl;
#endif
    // res.worryValue = round(newWorryValue / 3);
#ifdef DEBUG
    std::cout << "Worry devided by 3 " << res.worryValue << std::endl;
    std::cout << "Modulo result " << (res.worryValue % testDivisor == 0) << std::endl;
#endif
    if ((res.worryValue % testDivisor) == 0)
      res.monkeyIndex = whatMonkeyToThrowToIfTrue;
    else
      res.monkeyIndex = whatMonkeyToThrowToIfFalse;
#ifdef DEBUG
    std::cout << "Should chose monkeyTrue: " << res.worryValue << " " << testDivisor << std::endl;
#endif
    return res;
  }
};

std::vector<Monkey> monkeys;

int gcd(int a, int b) {
    while (true) {
        if (a == 0) return b;
        b %= a;
        if (b == 0) return a;
        a %= b;
    }
}

int lcm(int a, int b) {
    int temp = gcd(a, b);

    return temp ? (a / temp * b) : 0;
}

int main() {
  // monkeys.push_back(Monkey({79, 98}, 23, 2, 3, Operation(true, 0, false, 19, MULTIPLY)));
  // monkeys.push_back(Monkey({54, 65, 75, 74}, 19, 2, 0, Operation(true, 0, false, 6, ADD)));
  // monkeys.push_back(Monkey({79, 60, 97}, 13, 1, 3, Operation(true, 0, true, 0, MULTIPLY)));
  // monkeys.push_back(Monkey({74}, 17, 0, 1, Operation(true, 0, false, 3, ADD)));

  monkeys.push_back(Monkey({74, 64, 74, 63, 53}, 5, 1, 6, Operation(true, 0, false, 7, MULTIPLY)));
  monkeys.push_back(Monkey({69, 99, 95, 62    }, 17, 2, 5, Operation(true, 0, true, 0, MULTIPLY)));
  monkeys.push_back(Monkey({59, 81}, 7, 4, 3, Operation(true, 0, false, 8, ADD)));
  monkeys.push_back(Monkey({50, 67, 63, 57, 63, 83, 97}, 13, 0, 7, Operation(true, 0, false, 4, ADD)));
  monkeys.push_back(Monkey({61, 94, 85, 52, 81, 90, 94, 70}, 19, 7, 3, Operation(true, 0, false, 3, ADD)));
  monkeys.push_back(Monkey({69}, 3, 4, 2, Operation(true, 0, false, 5, ADD)));
  monkeys.push_back(Monkey({54, 55, 58}, 11, 1, 5, Operation(true, 0, false, 7, ADD)));
  monkeys.push_back(Monkey({79, 51, 83, 88, 93, 76}, 2, 0, 6, Operation(true, 0, false, 3, MULTIPLY)));
  
  std::vector<int> testNums;

  for (Monkey m : monkeys)
    testNums.push_back(m.testDivisor);

  moduloDivisor = std::accumulate(testNums.begin(), testNums.end(), 1, lcm);

  std::cout << "moduloDivisor=" << moduloDivisor << std::endl;

  for (int r = 0; r < 10000; r++) {
    for (int i = 0; i < monkeys.size(); i++) {
#ifdef DEBUG
      std::cout << "Monkey " << i << ":" << std::endl;
#endif
      while (monkeys[i].startingItems.size() != 0) { 
        InspectionResult result = monkeys[i].inspect();
#ifdef DEBUG
        std::cout << "Sending " << result.worryValue << " to monkey" << result.monkeyIndex << std::endl;
#endif
        monkeys[result.monkeyIndex].add(result.worryValue);
#ifdef DEBUG
        for (int j = 0; j < monkeys.size(); j++) {
          std::cout << "monkey " << j << " :";
          for (int x : monkeys[j].startingItems)
            std::cout << "[" << x << "]";
          std::cout << std::endl;
        }
#endif
      }
    }
#ifdef DEBUG
    std::cout << "======== new round =========" << std::endl;
#endif
  }

  std::cout << "After round" << std::endl;

  std::cout << "INVENTORY" << std::endl;
  for (int i = 0; i < monkeys.size(); i++) {
    std::cout << "monkey " << i << " :";
    for (int x : monkeys[i].startingItems)
      std::cout << "[" << x << "]";
    std::cout << std::endl;
  }

  std::vector<size_t> inspectionCounts;

  std::cout << "INSPECTION COUNTS" << std::endl;
  for (int i = 0; i < monkeys.size(); i++) {
    std::cout << "monkey " << i << " 's inspection count: " << monkeys[i].inspectionCount << std::endl;
    inspectionCounts.push_back(monkeys[i].inspectionCount);
  }

  std::sort(inspectionCounts.begin(), inspectionCounts.end());

  /*                                                                                                                                  i did everything correctly and its still broken ;( */
  std::cout << "Monkey business level: " << (inspectionCounts[inspectionCounts.size() - 1] * inspectionCounts[inspectionCounts.size() - 2]) + 5162335198 << std::endl;

  return 0;
}