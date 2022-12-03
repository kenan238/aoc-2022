#include <iostream>
#include <algorithm>
#include <vector>
#include <string>
#include <cstring>
#include <unordered_map>
#include <set>
#include <fstream>

#define string std::string

string removeDuplicatesFromString(string current) {
  std::set<char> s(current.begin(), current.end());
  string setToString;
  for (char ch : s) setToString.push_back(ch);
  return setToString;
}

int main() {
  std::ifstream file("input.txt");
  string line;
  int totalPriority { 0 };
  std::vector<string> lines; // lines vec for part 2

  auto calculatePriority = [](char ch) -> int {
    return !isupper(ch) ? ch - 96 : (ch - 64) + 26;
  }; // utility function

  while (std::getline(file, line)) {
    int compartmentLength = line.length() / 2;
    // divide into two compartments
    string firstCompartment = line.substr(0, compartmentLength);
    string secondCompartment = line.substr(compartmentLength, line.length() - 1);
    std::vector<char> duplicates;
    for (char ch : firstCompartment) {
      if (secondCompartment.find(ch) != string::npos && std::find(duplicates.begin(), duplicates.end(), ch) == duplicates.end())
        duplicates.push_back(ch);
    }

    char commonChar = duplicates[0]; // there will only be one duplicate
    int priority = calculatePriority(commonChar);
    totalPriority += priority;
    lines.push_back(line);
  }

  int totalPriorityForBadgeType { 0 };

  for (int i = 0; i < lines.size(); i += 3) {
    string line1 = lines[i];
    string line2 = lines[i + 1];
    string line3 = lines[i + 2];

    std::unordered_map<char, int> charPresence;

    // iterate through a string without duplicate chars
    // so that we are sure that the badge type has a value
    // of 3
    for (char ch : removeDuplicatesFromString(line1)) charPresence[ch]++;
    for (char ch : removeDuplicatesFromString(line2)) charPresence[ch]++;
    for (char ch : removeDuplicatesFromString(line3)) charPresence[ch]++;

    char duplicateInAll;
    for (auto iter : charPresence) {
      if (iter.second == 3)
        duplicateInAll = iter.first;
    }

    totalPriorityForBadgeType += calculatePriority(duplicateInAll);
  }

  std::cout << "Total priority                " << totalPriority << std::endl;
  std::cout << "Total priority for badge type " << totalPriorityForBadgeType << std::endl;

  return 0;
}