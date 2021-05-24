package org.cjoakim.utils;

import java.util.ArrayList;
import java.util.StringTokenizer;
import java.util.Vector;

/**
 * This class implements reusable String tokenizing logic for the application.
 * The intent of this class is to eliminate copy-and-paste tokenizing logic.
 *
 * @author Chris Joakim, Microsoft
 * @date   2018/11/03
 */

public class Tokenizer extends Object {

	public Tokenizer() {

		super();
	}

	public String[] tokenize(String string) {
		
		return tokenize(string, null);
	}
	
	public String[] tokenize(String string, String delim) {

		if (string == null) {
			return new String[0];
		}
		ArrayList<String> tokens = new ArrayList<String>();
		StringTokenizer st = null;
		if (delim == null) {
			st = new StringTokenizer(string);
		} else {
			st = new StringTokenizer(string, delim);
		}
		while (st.hasMoreElements()) {
			tokens.add((String) st.nextElement());
		}
		Vector<String> vector = new Vector<String>();
		vector.addAll(tokens);
		String[] array = new String[vector.size()];
		vector.copyInto(array);
		return array;
	}
	
	public ArrayList<String> tokenizeToArrayList(String string, String delim) {
		
		ArrayList<String> list = new ArrayList<String>();
		String[] tokens = tokenize(string, delim);
		for (int i = 0; i < tokens.length; i++) {
			list.add(tokens[i]);
		}
		return list;
	}
}

