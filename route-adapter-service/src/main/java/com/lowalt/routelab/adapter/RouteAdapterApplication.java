package com.lowalt.routelab.adapter;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.boot.context.properties.ConfigurationPropertiesScan;

@SpringBootApplication
@ConfigurationPropertiesScan
public class RouteAdapterApplication {

    public static void main(String[] args) {
        SpringApplication.run(RouteAdapterApplication.class, args);
    }
}

