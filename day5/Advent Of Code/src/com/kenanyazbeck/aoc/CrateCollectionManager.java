package com.kenanyazbeck.aoc;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

// does the actual simulating

public class CrateCollectionManager { // Do not judge the naming
	public List<CrateCollection> collections = new ArrayList<CrateCollection>();
	
	public CrateCollectionManager() { }
	
	public void addCollection(CrateCollection collection) {
		this.collections.add(collection);
	}
	
	public void addCrateToCollection(int collectionIndex, String crate) {
		CrateCollection collection = this.collections.get(collectionIndex);
		collection.addCrateToBack(crate);
		this.collections.set(collectionIndex, collection);
	}
	
	public List<String> getTopCrates() {
		List<String> topCrates = new ArrayList<String>();
		for (int i = 0; i < collections.size(); i++) {
			topCrates.add(this.collections.get(i).getTop());
		}
		
		return topCrates;
	}
	
	public void Debug() { // im not removing th
		for (int i = 0; i < collections.size(); i++) {
			System.out.print(Integer.toString(i) + ": ");
			this.collections.get(i).Debug();
		}
	}
	
	public void moveCrate(int howMuch, int from, int to) {
		for (int i = 0; i < howMuch; i++) {
			CrateCollection fromCollection = this.collections.get(from);
			String crate = fromCollection.pop();
			this.collections.set(from, fromCollection);

			CrateCollection toCollection = this.collections.get(to);
			toCollection.addCrate(crate);
			this.collections.set(to, toCollection);
		}
	}
	
	public void moveCratePart2(int howMuch, int from, int to) {
		CrateCollection fromCollection = this.collections.get(from);
		List<String> crates = fromCollection.popN(howMuch);
		Collections.reverse(crates);
		this.collections.set(from, fromCollection);

		CrateCollection toCollection = this.collections.get(to);
		toCollection.addCrates(crates);
		this.collections.set(to, toCollection);
	}
}