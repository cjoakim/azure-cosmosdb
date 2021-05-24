package org.cjoakim.azure.redis;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.cjoakim.azure.AppConfig;
import org.cjoakim.azure.EnvVarNames;

import redis.clients.jedis.Jedis;
import redis.clients.jedis.JedisShardInfo;

/**
 * This class implements Azure Redis Cache operations.
 *
 * @author Chris Joakim, Microsoft
 * @date   2020/11/12
 */

public class RedisUtil implements EnvVarNames {

	// Constants:
	private final static Logger logger = LoggerFactory.getLogger(RedisUtil.class);

	// Instance variables:
	String namespace = null;
	String redisHost = null;
	String redisKey = null;
	JedisShardInfo shardInfo = null;
	Jedis jedis = null;

	/**
	 * Default constructor; config values come from environment variables.
	 */
	public RedisUtil() {

		super();

		namespace = AppConfig.envVar("AZURE_REDISCACHE_NAMESPACE");
		redisHost = String.format("%s.redis.cache.windows.net", namespace);
		redisKey  = AppConfig.envVar("AZURE_REDISCACHE_KEY");

		shardInfo = new JedisShardInfo(redisHost, 6379);
		shardInfo.setPassword(redisKey);
		jedis = new Jedis(shardInfo);
		logger.warn("connected to: " + redisHost);
	}

	public String set(String key, String value) {

		return jedis.set(key, value);
	}

	public String get(String key) {

		return jedis.get(key);
	}

}
