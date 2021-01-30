package org.cjoakim.utils;

import org.cjoakim.azure.AppConfig;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.URL;

/**
 * This class invokes HTTP APIs at api.openweathermap.org using a key specified in
 * an environment variable.
 *
 * TODO - revisit this class
 *
 * @author Chris Joakim, Microsoft
 * @date   2018/05/14
 */

public class WeatherDao {

    // Constants:
    private static final String api_base = "http://api.openweathermap.org/data/2.5";
    private static final Logger logger   = LoggerFactory.getLogger(WeatherDao.class);

    public static synchronized String getWeatherForLocation(double lat, double lng) {

        String key  = AppConfig.getOpenWeatherMapKey();
        String path = "weather";
        String url  = String.format("%s/%s?lat=%s&lon=%s&units=imperial&APPID=%s", api_base, path, lat, lng, key);
        return invokeAPI(url);
    }

    public static synchronized String getForecastForLocation(double lat, double lng) {

        String key  = AppConfig.getOpenWeatherMapKey();
        String path = "forecast";
        String url  = String.format("%s/%s?lat=%s&lon=%s&units=imperial&APPID=%s", api_base, path, lat, lng, key);
        return invokeAPI(url);
    }

    private static String invokeAPI(String url) {

        logger.warn(String.format("invokeAPI; url: %s", url));
        StringBuffer buffer = new StringBuffer();
        String inputLine = null;

        try {
            URL obj = new URL(url);
            HttpURLConnection con = (HttpURLConnection) obj.openConnection();
            con.setRequestMethod("GET");

            int code = con.getResponseCode();
            logger.warn(String.format("invokeAPI; code: %s", code));
            BufferedReader in = new BufferedReader(new InputStreamReader(con.getInputStream()));

            if (code == 200) {
                while ((inputLine = in.readLine()) != null) {
                    buffer.append(inputLine);
                }
            }
            in.close();
        }
        catch (IOException e) {
            logger.warn("invokeAPI " + e.getClass().getName() + ": " + e.getMessage());
        }
        finally {
            return buffer.toString().trim();
        }
    }

}
