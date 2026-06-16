package com.lowalt.routelab.adapter.skygrid;

import com.lowalt.routelab.adapter.config.SkyGridProperties;
import org.springframework.boot.web.client.RestTemplateBuilder;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

import java.time.Duration;
import java.util.Locale;

@Configuration
public class SkyGridClientFactory {

    @Bean
    public SkyGridClient skyGridClient(RestTemplateBuilder restTemplateBuilder, SkyGridProperties properties) {
        String mode = properties.normalizedMode();
        if ("mock".equals(mode)) {
            return new MockSkyGridClient();
        }
        if ("real".equals(mode)) {
            if (properties.token() == null || properties.token().isBlank()) {
                throw new IllegalStateException("SkyGrid dev token is missing");
            }
            int timeoutMs = properties.normalizedTimeoutMs();
            return new RealSkyGridClient(
                    restTemplateBuilder
                            .setConnectTimeout(Duration.ofMillis(timeoutMs))
                            .setReadTimeout(Duration.ofMillis(timeoutMs))
                            .build(),
                    properties
            );
        }
        throw new IllegalArgumentException("Unsupported skygrid.mode: " + mode.toLowerCase(Locale.ROOT));
    }
}
