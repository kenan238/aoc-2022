// aoc 2022 day 5
// i have only used java 2 times

package com.kenanyazbeck.aoc;

import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;

/*
 * new input.txt format:
 * first line: length
 * N lines: represent the crates without [ and ]
 * add a trailing space to tell the program we finished with the crates
 * instructions seperated by spaces:
 * 		amount from to
 * example:
 * 		1 2 1
 * 		is like
 * 		move 1 from 2 to 1
 * too lazy to properly parse
 * for example check input.txt
 * */

public class Solution {
	private static CrateCollectionManager manager = new CrateCollectionManager();

	public static void main(String[] args) {
		BufferedReader reader;
		
		// TODO to get part 2 behaviour
		// flip this
		Boolean doPart2 = false; 
		try {
			reader = new BufferedReader(new FileReader("input.txt"));
			String line = reader.readLine();
			
			Boolean finishedFetchingSize = false;
			Boolean finishedFetchingStructure = false;
			List<String> instructions = new ArrayList<String>();
			
			while (line != null) {
				if (!finishedFetchingSize) {
					finishedFetchingSize = true;
					int size = Integer.parseInt(line);
					for (int i = 0; i < size; i++) {
						manager.addCollection(new CrateCollection());
					}
				}
				else if (finishedFetchingSize && !finishedFetchingStructure) {
					if (line.equals("")) {
						finishedFetchingStructure = true;
					}
					for (int i = 0; i < line.length(); i++) {
						char character = line.charAt(i);
						if (character == ' ') continue;
						manager.addCrateToCollection(i, Character.toString(character));
					}
				}
				else if (finishedFetchingSize && finishedFetchingStructure) {
					instructions.add(line);
				}
				
				line = reader.readLine();
			}
			
			// finished parsing
			
			manager.Debug();
			
			// simulate instructions
			for (int i = 0; i < instructions.size(); i++) {
				String instruction = instructions.get(i);
				String[] splittedInstruction = instruction.split("\\s+");
				String c1 = splittedInstruction[0];
				String c2 = splittedInstruction[1];
				String c3 = splittedInstruction[2];
				System.out.println(instruction);
				if (!doPart2) {
					manager.moveCrate(
							Integer.parseInt(c1), 
							Integer.parseInt(c2) - 1,
							Integer.parseInt(c3) - 1
						);
				} else {
					manager.moveCratePart2(
						Integer.parseInt(c1), 
						Integer.parseInt(c2) - 1,
						Integer.parseInt(c3) - 1
					);
				}
//				TODO for debugging
//				System.out.println("=======");
//				manager.Debug();
			}
			
//			almost pushed with this in there
//			manager.Debug();
			
			List<String> topCrates = manager.getTopCrates();
			for (int i = 0; i < topCrates.size(); i++) {
				System.out.print(topCrates.get(i) + "");
			}
			
			reader.close();
		} catch (IOException e) {
			System.out.println("im dead");
			e.printStackTrace();
		}
	}
}
