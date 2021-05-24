package org.cjoakim.azure.servicebus;

import java.util.concurrent.CompletableFuture;

import com.microsoft.azure.servicebus.ExceptionPhase;
import com.microsoft.azure.servicebus.IMessage;
import com.microsoft.azure.servicebus.IMessageHandler;
import com.microsoft.azure.servicebus.IQueueClient;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

class MessageHandlerImpl implements IMessageHandler {

	// Constants:
	private final static Logger logger = LoggerFactory.getLogger(MessageHandlerImpl.class);
			
	private IQueueClient client;
	
    public MessageHandlerImpl(IQueueClient client) {
    	
    	super();    	
        this.client = client;
    }

    @Override
    public CompletableFuture<Void> onMessageAsync(IMessage msg) {
    	
        logger.warn(String.format("onMessageAsync seq: %d token: %s body: %s", 
        		msg.getSequenceNumber(), msg.getLockToken(), new String(msg.getBody())));
        
        return this.client.completeAsync(msg.getLockToken()).thenRunAsync(() -> {
        	logger.warn(String.format("onMessageAsync completed seq: %d token: %s body: %s", 
        			msg.getSequenceNumber(), msg.getLockToken(), new String(msg.getBody())));
        });
    }

    @Override
    public void notifyException(Throwable throwable, ExceptionPhase exceptionPhase) {
    	
    	logger.warn(exceptionPhase + " - " + throwable.getMessage());
    }
}