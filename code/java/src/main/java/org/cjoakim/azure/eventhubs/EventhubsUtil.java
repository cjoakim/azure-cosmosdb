package org.cjoakim.azure.eventhubs;

import java.io.IOException;
import java.nio.charset.Charset;
import java.util.List;
import java.util.concurrent.ExecutionException;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.cjoakim.azure.AppConfig;
import org.cjoakim.io.FileUtil;
import com.microsoft.azure.eventhubs.ConnectionStringBuilder;
import com.microsoft.azure.eventhubs.EventData;
import com.microsoft.azure.eventhubs.EventHubClient;
import com.microsoft.azure.eventhubs.EventHubException;

/**
 * This class is used to send messages to Azure Event Hubs.
 * 
 * @see https://github.com/Azure/azure-event-hubs/tree/master/samples/Java/Basic/SimpleSend
 * 
 * @author Chris Joakim, Microsoft
 * @date   2018/05/29
 */

public class EventhubsUtil {
	
	// Constants:
    private static final Logger logger = LoggerFactory.getLogger(EventhubsUtil.class);
    		
	// Instance variables:
	private EventHubClient  client = null;
	private ExecutorService executorService = null;
		
	private EventhubsUtil() throws EventHubException, ExecutionException, InterruptedException, IOException {

		super();
		
		String namespace = AppConfig.envVar(AppConfig.AZURE_EVENTHUB_NAMESPACE);
		String hubName   = AppConfig.envVar(AppConfig.AZURE_EVENTHUB_HUBNAME);
		String keyName   = AppConfig.envVar(AppConfig.AZURE_EVENTHUB_POLICY);
		String keyValue  = AppConfig.envVar(AppConfig.AZURE_EVENTHUB_KEY);

		logger.warn("EventhubsUtil constructor; namespace: " + namespace);
		logger.warn("EventhubsUtil constructor; hubName:   " + hubName);
		logger.warn("EventhubsUtil constructor; keyName:   " + keyName);
		logger.warn("EventhubsUtil constructor; keyValue:  " + keyValue);
		
		ConnectionStringBuilder connStr = new ConnectionStringBuilder()
			.setNamespaceName(namespace)
			.setEventHubName(hubName)
			.setSasKeyName(keyName)
			.setSasKey(keyValue);

		logger.warn("EventhubsUtil constructor; connStr:   " + connStr.toString());
		
		executorService = Executors.newSingleThreadExecutor();
		client = null;  // TODO - revisit.  EventHubClient.createSync(connStr.toString(), executorService);
	}

	public void sendMessage(String msg) throws EventHubException {

        byte[] msgBytes = msg.getBytes(Charset.defaultCharset());
        EventData sendEvent = EventData.create(msgBytes);

        // Send - not tied to any partition, Event Hubs service will round-robin the events
        // across all Event Hubs partitions.
        // This is the recommended & most reliable way to send to Event Hubs.
        client.sendSync(sendEvent);
	}
	
	public static void main(String[] args) throws Exception {
		
		EventhubsUtil ehu = new EventhubsUtil();
		FileUtil fu = new FileUtil();
		List<String> lines = fu.readFileLines("data/private/YFS_WORK_ORDER_PRETTY.json");
		// above json file created with the following command due to invalid characters in the TXT file:
		// cat YFS_WORK_ORDER.TXT | jq . -M > YFS_WORK_ORDER_PRETTY.json
		
		StringBuilder sb = new StringBuilder();
		for (int i = 0; i < lines.size(); i++) {
			sb.append(lines.get(i) + "\n");
		}
		String workOrder = sb.toString();
		logger.warn("workOrder: " + workOrder);
		
		for (int i = 0; i < 50; i++) {
			logger.warn("sending workOrder message " + i);
			ehu.sendMessage(workOrder);
		}
		
//		for (int i = 0; i < 10; i++) {
//			String msg = "message " + i + " at " + new Date().toString();
//			logger.warn("main() send: " + msg);
//			ehu.sendMessage(msg);
//		}
		
	}
	
}
