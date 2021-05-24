package org.cjoakim.azure.storage;

import java.io.*;
import java.util.ArrayList;

import com.azure.storage.blob.*;
import com.azure.storage.blob.models.*;


import org.cjoakim.azure.AppConfig;
import org.cjoakim.azure.EnvVarNames;

/**
 * This class implements Azure Storage Blob operations.
 * org.cjoakim.azure.storage.BlobUtil
 * 
 * @author Chris Joakim, Microsoft
 * @date   2020/11/15
 * 
 * @see https://docs.microsoft.com/en-us/azure/storage/blobs/storage-quickstart-blobs-java
 */

//Use the following Java classes to interact with these resources:
//
//BlobServiceClient: The BlobServiceClient class allows you to manipulate Azure Storage resources and blob containers. The storage account provides the top-level namespace for the Blob service.
//BlobServiceClientBuilder: The BlobServiceClientBuilder class provides a fluent builder API to help aid the configuration and instantiation of BlobServiceClient objects.
//BlobContainerClient: The BlobContainerClient class allows you to manipulate Azure Storage containers and their blobs.
//BlobClient: The BlobClient class allows you to manipulate Azure Storage blobs.
//BlobItem: The BlobItem class represents individual blobs returned from a call to listBlobs.

public class BlobUtil implements EnvVarNames {

	// Instance variables:
	private BlobServiceClient blobServiceClient = null;
	
	public BlobUtil() {
		
		super();
		
		String connString = AppConfig.envVar(AZURE_STORAGE_CONNECTION_STRING);
		blobServiceClient = new BlobServiceClientBuilder().connectionString(connString).buildClient();
		System.out.println(blobServiceClient);
	}
	
	public BlobContainerClient createContainer(String cname) {
		
		try {
			return blobServiceClient.createBlobContainer(cname);
		}
		catch (Exception e) {
			e.printStackTrace();
			return null;
		}
	}
	
	public BlobContainerClient getContainerClient(String cname) {
		
		try {
			return blobServiceClient.getBlobContainerClient(cname);
		}
		catch (Exception e) {
			e.printStackTrace();
			return null;
		}
	}
	
	public ArrayList<String> listBlobs(String cname) {
		
		ArrayList<String> list = new ArrayList<String>();

		for (BlobItem blobItem : getContainerClient(cname).listBlobs()) {
			list.add(blobItem.getName());
		}
		return list;
	}
	
	public boolean downloadBlob(String cname, String blobPath, String outfile) {
		
		try {
			BlobContainerClient cc = getContainerClient(cname);
			BlobClient bc = cc.getBlobClient(blobPath);
			bc.downloadToFile(outfile);
			return true;
		}
		catch (Exception e) {
			e.printStackTrace();
			return false;
		}
	}
	
	public boolean uploadBlob(String cname, String infile) {
		
		try {
			BlobContainerClient cc = getContainerClient(cname);
			BlobClient bc = cc.getBlobClient(infile);
			bc.uploadFromFile(infile);
			return true;
		}
		catch (Exception e) {
			e.printStackTrace();
			return false;
		}
	}
	
    public static void main(String[] args) throws Exception {
    
    	
    	BlobUtil bu = new BlobUtil();
    	
    	if (false) {
        	ArrayList<String> blobList = bu.listBlobs("subscription");
    		for (String blobname : blobList) {
    			System.out.println(blobname);
    		}
    	}

		if (true) {
			String outfile = "tmp/cost-" + System.currentTimeMillis() + ".csv";
			String blobPath = "costs/subscriptioncosts/20201001-20201031/subscriptioncosts_d527a1d1-dfbe-4810-adaf-95f2ab0b59c8.csv";
			bu.downloadBlob("subscription", blobPath, outfile);
			System.out.println("blob downloaded to local file " + outfile);
		}
		
		if (true) {
			String infile = "readme.md";
			bu.uploadBlob("test", infile);
			System.out.println("blob uploaded from local file " + infile);
		}
		
		System.exit(0);
    }
}
