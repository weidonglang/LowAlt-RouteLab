package com.lowalt.routelab.adapter;

import com.lowalt.routelab.adapter.config.SkyGridProperties;
import org.junit.jupiter.api.Test;

import static org.assertj.core.api.Assertions.assertThat;

class RealSkyGridClientConfigTest {

    @Test
    void normalizesDefaults() {
        SkyGridProperties properties = new SkyGridProperties(
                null,
                "http://127.0.0.1:8080/",
                "dev-token",
                null,
                null,
                null,
                null,
                null,
                null
        );

        assertThat(properties.normalizedMode()).isEqualTo("mock");
        assertThat(properties.normalizedBaseUrl()).isEqualTo("http://127.0.0.1:8080");
        assertThat(properties.normalizedTimeoutMs()).isEqualTo(5000);
        assertThat(properties.normalizedOrgId()).isEqualTo(1L);
        assertThat(properties.normalizedApplicantName()).isEqualTo("lowalt-route-adapter");
        assertThat(properties.normalizedRouteTemplateId()).isEqualTo(1L);
    }
}
