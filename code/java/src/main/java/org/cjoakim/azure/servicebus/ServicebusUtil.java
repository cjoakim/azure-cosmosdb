package org.cjoakim.azure.servicebus;

import java.time.Duration;
import java.util.Date;

import org.cjoakim.azure.AppConfig;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import com.microsoft.azure.servicebus.IMessageReceiver;
import com.microsoft.azure.servicebus.IMessageSender;
import com.microsoft.azure.servicebus.Message;
import com.microsoft.azure.servicebus.MessageHandlerOptions;
import com.microsoft.azure.servicebus.QueueClient;
import com.microsoft.azure.servicebus.ReceiveMode;
import com.microsoft.azure.servicebus.primitives.ConnectionStringBuilder;
import com.microsoft.azure.servicebus.primitives.ServiceBusException;

/**
 * This class is used to send and receive messages from Azure Service Bus.
 *
 * @author Chris Joakim, Microsoft
 * @date   2018/05/29
 */

public class ServicebusUtil {

	// Constants:
	public static final int SENDER   = 0;
	public static final int RECEIVER = 1;
	
    private static final Logger logger = LoggerFactory.getLogger(ServicebusUtil.class);

    // Instance variables:
    private String connString = null;
    private String queueName  = null;
    private QueueClient queueClient;
    private IMessageSender sender = null;
    private IMessageReceiver receiver = null;

	/**
	 * Default constructor; do not use.
	 */
	private ServicebusUtil() {
		
		super();
	}
	
	/**
	 *Constructor; connection string value comes from an environment variable.
	 */
	public ServicebusUtil(String qname, int mode) throws InterruptedException, ServiceBusException {

	    this.connString = AppConfig.envVar(AppConfig.AZURE_SERVICEBUS_CONN_STRING);
	    this.queueName  = qname;
        logger.warn("constructor; connString: " + this.connString);
        logger.warn("constructor; queueName:  " + this.queueName);
        
	    queueClient = new QueueClient(
	    		new ConnectionStringBuilder(connString, queueName),
	    		ReceiveMode.PEEKLOCK);
	    
	    if (mode == RECEIVER) {
	    	logger.warn("registerMessageHandler");
		    queueClient.registerMessageHandler(
		    		new MessageHandlerImpl(queueClient), 
		    		new MessageHandlerOptions(1, false, Duration.ofMinutes(1)));
	    }
	    logger.warn("constructor completed: " + this.queueClient);
    }

    public void sendMessageSynch(String messageText) throws ServiceBusException, InterruptedException {

	    Message msg = new Message(messageText);
	    this.queueClient.send(msg);
    }

    public void sendMessageAsynch(final String messageText) {

        Message msg = new Message(messageText);
        logger.warn("sendMessageAsynch - send: " + messageText);
        
        this.queueClient.sendAsync(msg).thenRunAsync(() -> {
            logger.warn("sendMessageAsynch - sent: " + messageText);
        });
    }
    
    public void close(long msPause) throws ServiceBusException {

    	logger.warn("close - closing...");
    	pause(msPause);
    	queueClient.close();
	    logger.warn("close - closed");
    }

	protected void pause(long ms) {

		try {
			Thread.sleep(Math.abs(ms));
		} catch (Exception e) {
			e.printStackTrace();
		}
	}
	
    public static void main(String[] args) {

    	try {
    		String qname = "test";
    		long msPause = 3000;
    		ServicebusUtil util1 = null;
    		ServicebusUtil util2 = null;
    		
    		util1 = new ServicebusUtil(qname, ServicebusUtil.SENDER);
    		util1.pause(msPause);
    		int count = 10;
    		
    		for (int i = 0; i < count; i++) {
    			String msg = String.format("elsa %s at %s", i, new Date().toString());
    			logger.warn("main: " + msg);
    			util1.sendMessageAsynch(msg);
    			
    			if (i == (count - 1)) {
    				util1.close(msPause);
    				
    	    		util2 = new ServicebusUtil(qname, ServicebusUtil.RECEIVER);
    	    		util2.close(msPause * 2);
    			}
    		}
		}
    	catch (Exception e) {
			e.printStackTrace();
		}
    }
}
