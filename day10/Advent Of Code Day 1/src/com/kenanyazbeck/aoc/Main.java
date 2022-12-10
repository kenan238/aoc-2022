package com.kenanyazbeck.aoc;

import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Map.Entry;

public class Main {

	private static int cycleCount = 0;
	private static int xRegister = 1;
	private static int signalStrengths = 0;
	private static int targetCycle = 20;
	
	private static final int WIDTH = 40;
	
	private static int currentPixelX = 1;
	
	private static int lastCycleCount = 0;
	
	public static void drawCycle() {
		currentPixelX++;
		if (currentPixelX % WIDTH == 0) {
			System.out.println();
			currentPixelX = 0;
		}
		
		if (
			currentPixelX == xRegister || 
			currentPixelX == xRegister + 1 || 
			currentPixelX == xRegister - 1
		) {
			System.out.print('#');
		} else {
			System.out.print('.');
		}
	}
	
	public static void main(String[] args) {
		BufferedReader reader;

		try {
			reader = new BufferedReader(new FileReader("input.txt"));
			String line = reader.readLine();
			
			System.out.print("##"); // goofy flextape fix
			
			while (line != null) {
				String[] splittedLine = line.split("\\s+");
				line = reader.readLine();
				String instructionName = splittedLine[0];
				
				if (instructionName.equals("noop")) {
					cycleCount ++;
				} else {
					cycleCount += 2;
				}
				if (cycleCount >= targetCycle) {
					signalStrengths += targetCycle * xRegister;
					targetCycle += 40;
				}
				if (instructionName.equals("addx")) {
					xRegister += Integer.parseInt(splittedLine[1]);
				}
				
				for (int i = lastCycleCount; i < cycleCount; i++) {
					drawCycle();
				}
				
				lastCycleCount = cycleCount;
			}
			
			System.out.println("\nX register is " + xRegister + " last cycle was " + cycleCount + " and signal strengths are " + signalStrengths);
			

			reader.close();
		} catch (IOException e) {
			e.printStackTrace();
		}
	}
}
