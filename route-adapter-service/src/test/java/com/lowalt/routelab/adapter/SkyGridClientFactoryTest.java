package com.lowalt.routelab.adapter;

import com.lowalt.routelab.adapter.config.SkyGridProperties;
import com.lowalt.routelab.adapter.skygrid.MockSkyGridClient;
import com.lowalt.routelab.adapter.skygrid.RealSkyGridClient;
import com.lowalt.routelab.adapter.skygrid.SkyGridClient;
import com.lowalt.routelab.adapter.skygrid.SkyGridClientFactory;
import org.junit.jupiter.api.Test;
import org.springframework.boot.web.client.RestTemplateBuilder;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;

class SkyGridClientFactoryTest {

    @Test
    void createsMockClientByDefault() {
        SkyGridClientFactory factory = new SkyGridClientFactory();

        SkyGridClient client = factory.skyGridClient(new RestTemplateBuilder(), properties(null, null));

        assertThat(client).isInstanceOf(MockSkyGridClient.class);
    }

    @Test
    void createsRealClientWhenModeIsReal() {
        SkyGridClientFactory factory = new SkyGridClientFactory();

        SkyGridClient client = factory.skyGridClient(new RestTemplateBuilder(), properties("real", "dev-token"));

        assertThat(client).isInstanceOf(RealSkyGridClient.class);
    }

    @Test
    void rejectsRealModeWithoutToken() {
        SkyGridClientFactory factory = new SkyGridClientFactory();

        assertThatThrownBy(() -> factory.skyGridClient(new RestTemplateBuilder(), properties("real", "")))
                .isInstanceOf(IllegalStateException.class)
                .hasMessageContaining("SkyGrid dev token is missing");
    }

    private static SkyGridProperties properties(String mode, String token) {
        return new SkyGridProperties(
                mode,
                "http://127.0.0.1:8080",
                token,
                5000,
                1L,
                1L,
                "tester",
                1L,
                1L
        );
    }
}
