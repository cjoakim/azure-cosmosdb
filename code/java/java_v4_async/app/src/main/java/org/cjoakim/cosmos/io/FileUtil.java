package org.cjoakim.cosmos.io;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.SerializationFeature;
import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;

import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.Scanner;

/**
 * Utility class for FileIO operations.
 *
 * Chris Joakim, Microsoft
 */

public class FileUtil {

    // Class variables
    private static Logger logger = LogManager.getLogger(FileUtil.class);

    public FileUtil() {

        super();
    }

    public List<String> readLines(String infile) throws IOException {

        List<String> lines = new ArrayList<String>();
        File file = new File(infile);
        Scanner sc = new Scanner(file);
        while (sc.hasNextLine()) {
            lines.add(sc.nextLine().trim());
        }
        return lines;
    }

    public List<File> listFilesMatching(String directory, String pattern, String suffix) throws IOException {

        List<File> selectedFiles = new ArrayList<File>();

        File dir = new File(directory);
        File[] files = dir.listFiles();
        for (int i = 0; i < files.length; i++) {
            File f = files[i];
            if (f.getName().contains(pattern)) {
                if (f.getName().endsWith(suffix)) {
                    selectedFiles.add(f);
                }
            }
        }
        return selectedFiles;
    }

    public Map<String, Object> readJsonMap(String infile) throws Exception {

        ObjectMapper mapper = new ObjectMapper();
        return mapper.readValue(Paths.get(infile).toFile(), Map.class);
    }

    public void writeJson(Object obj, String outfile, boolean pretty, boolean verbose) throws Exception {

        ObjectMapper mapper = new ObjectMapper();
        mapper.enable(SerializationFeature.INDENT_OUTPUT);

        String json = null;
        if (pretty) {
            json = mapper.writeValueAsString(obj);
            writeTextFile(outfile, json, verbose);
        }
        else {
            json = mapper.writeValueAsString(obj);
            writeTextFile(outfile, json, verbose);
        }
    }

    public void writeTextFile(String outfile, String text, boolean verbose) throws Exception {

        FileWriter fw = null;

        try {
            fw = new FileWriter(outfile);
            fw.write(text);
            if (verbose) {
                logger.warn("file written: " + outfile);
            }
        }
        catch (IOException e) {
            e.printStackTrace();
            throw e;
        }
        finally {
            if (fw != null) {
                fw.close();
            }
        }
    }
}
