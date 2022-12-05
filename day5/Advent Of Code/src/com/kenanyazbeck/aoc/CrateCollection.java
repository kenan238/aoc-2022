package com.kenanyazbeck.aoc;

import java.util.ArrayList;
import java.util.List;

// contains a crate column

public class CrateCollection {
	public List<String> crates = new ArrayList<String>();
	
	public CrateCollection() {}
	
	public void addCrate(String crate) {
		this.crates.add(crate);
	}
	
	public void addCrates(List<String> crates) {
		this.crates.addAll(crates);
	}
	
	public void addCrateToBack(String crate) {
		this.crates.add(0, crate);
	}
	
	public void Debug() {
		for (int i = 0; i < crates.size(); i++) {
			System.out.print(crates.get(i));
		}
		
		System.out.println();
	}
	
	public String getTop() {
		return this.crates.get(this.crates.size() - 1);
	}
	
	public String pop() {
		return this.crates.remove(this.crates.size() - 1);
	}
	
	public List<String> popN(int howMuch) {
		List<String> crates = new ArrayList<String>();
		for (int i = 0; i < howMuch; i++) {
			crates.add(this.pop());
		}
		
		return crates;
	}
}
