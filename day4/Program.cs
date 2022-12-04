// aoc day 4 in C#

using System;
using System.Linq;
using System.IO;
using System.Collections;
using System.Collections.Generic;

struct Pair<T> {
  public T first;
  public T second;
}

public class Program {
  public static void Main(string[] args) {
    string[] input = File.ReadAllLines("input.txt");
    List<Pair<Pair<int>>> assignments = new();

    foreach (string line in input) {
      Pair<int> firstPair = new();
      Pair<int> secondPair = new();
      string[] splittedLine = line.Split(",");
      string[] firstPairSplit = splittedLine[0].Split("-");
      string[] secondPairSplit = splittedLine[1].Split("-");
      firstPair.first = int.Parse(firstPairSplit[0]);
      firstPair.second = int.Parse(firstPairSplit[1]);

      secondPair.first = int.Parse(secondPairSplit[0]);
      secondPair.second = int.Parse(secondPairSplit[1]);

      Pair<Pair<int>> pairsOfPairs = new(); // dont judge competitive code
      pairsOfPairs.first = firstPair;
      pairsOfPairs.second = secondPair;
      assignments.Add(pairsOfPairs);
    }

    int pairsThatCoverTheOther = 0;
    int overlappingPairs = 0;

    foreach (Pair<Pair<int>> assignment in assignments) {
      Pair<int> firstPair = assignment.first;
      Pair<int> secondPair = assignment.second;
      
      // Part 1

      // Check if a pair is fully inside another

      if (firstPair.first >= secondPair.first && firstPair.second <= secondPair.second) {
        pairsThatCoverTheOther++;
      }
      
      else if (secondPair.first >= firstPair.first && secondPair.second <= firstPair.second) {
        pairsThatCoverTheOther++;
      }

      // Part 2

      // Check if a pair overlaps with another

      if (firstPair.first <= secondPair.first && secondPair.first <= firstPair.second)
        overlappingPairs++;

      else if (secondPair.first <= firstPair.first && firstPair.first <= secondPair.second)
        overlappingPairs++;
    }

    Console.WriteLine("Pairs that cover the other (part 1) : " + pairsThatCoverTheOther);
    Console.WriteLine("Overlapping pairs (part 2)          : " + overlappingPairs);
  }
}