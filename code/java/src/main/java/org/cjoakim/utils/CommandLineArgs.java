package org.cjoakim.utils;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

/**
 * This class is used to parse keyword command line arguments and to cast
 * their values to various datatypes (String, int, long, boolean).
 *
 * @author Chris Joakim, Microsoft
 * @date   2018/11/03
 */

public class CommandLineArgs {
	
	// Class variables:
	private static final Logger logger = LoggerFactory.getLogger(CommandLineArgs.class);	

	// Instance variables:
	private String[] args = null;
	
	public CommandLineArgs(String[] clArgs) {
		
		super();
		if  (clArgs == null) {
			args = new String[0];
		}
		else {
			args = clArgs;
		}
	}

	public int count() {

		return this.args.length;
	}

	public String stringArg(String flag, String defaultValue) {
		
		if ((args.length == 0) || (flag == null) || (flag.trim().length() < 1)) {
			return defaultValue;
		}
		for (int i = 0; i < args.length; i++) {
			if (args[i].equals(flag)) {
				int nextIdx = i + 1;
				if (nextIdx < args.length) {
					return args[nextIdx];
				}
			}
		}
		return defaultValue;		
	}
	
	public int intArg(String flag, int defaultValue) {
		
		if ((args.length == 0) || (flag == null) || (flag.trim().length() < 1)) {
			return defaultValue;
		}
		for (int i = 0; i < args.length; i++) {
			if (args[i].equals(flag)) {
				int nextIdx = i + 1;
				if (nextIdx < args.length) {
					return Integer.parseInt(args[nextIdx]);
				}
			}
		}
		return defaultValue;		
	}
	
	public long longArg(String flag, long defaultValue) {
		
		if ((args.length == 0) || (flag == null) || (flag.trim().length() < 1)) {
			return defaultValue;
		}
		for (int i = 0; i < args.length; i++) {
			if (args[i].equals(flag)) {
				int nextIdx = i + 1;
				if (nextIdx < args.length) {
					return Long.parseLong(args[nextIdx]);
				}
			}
		}
		return defaultValue;		
	}

	public double doubleArg(String flag, double defaultValue) {

		if ((args.length == 0) || (flag == null) || (flag.trim().length() < 1)) {
			return defaultValue;
		}
		for (int i = 0; i < args.length; i++) {
			if (args[i].equals(flag)) {
				int nextIdx = i + 1;
				if (nextIdx < args.length) {
					return Double.parseDouble(args[nextIdx]);
				}
			}
		}
		return defaultValue;
	}

	public boolean booleanArg(String flag, boolean defaultValue) {
		
		if ((args.length == 0) || (flag == null) || (flag.trim().length() < 1)) {
			return defaultValue;
		}
		for (int i = 0; i < args.length; i++) {
			if (args[i].equals(flag)) {
				int nextIdx = i + 1;
				if (nextIdx < args.length) {
					return Boolean.parseBoolean(args[nextIdx]);
				}
			}
		}
		return defaultValue;		
	}	

}
