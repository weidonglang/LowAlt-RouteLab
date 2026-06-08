package com.lowalt.routelab.adapter.config;

import org.springframework.boot.context.properties.ConfigurationProperties;

@ConfigurationProperties(prefix = "adapter")
public record AdapterProperties(
        String algorithmServiceBaseUrl,
        String skygridMode
) {
}

