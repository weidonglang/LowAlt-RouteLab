package com.lowalt.routelab.adapter.algorithm;

import com.lowalt.routelab.adapter.config.AdapterProperties;
import org.springframework.core.ParameterizedTypeReference;
import org.springframework.http.HttpMethod;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Component;
import org.springframework.web.client.RestTemplate;

@Component
public class AlgorithmClient {

    private final RestTemplate restTemplate;
    private final AdapterProperties properties;

    public AlgorithmClient(RestTemplate restTemplate, AdapterProperties properties) {
        this.restTemplate = restTemplate;
        this.properties = properties;
    }

    public AlgorithmPlanResult plan(AlgorithmPlanRequest request) {
        ResponseEntity<AlgorithmApiResponse<AlgorithmPlanResult>> response = restTemplate.exchange(
                properties.algorithmServiceBaseUrl() + "/api/plan",
                HttpMethod.POST,
                new org.springframework.http.HttpEntity<>(request),
                new ParameterizedTypeReference<>() {
                }
        );
        return requireData(response.getBody());
    }

    public TimeSlotConvertResult convertTimeSlot(TimeSlotConvertRequest request) {
        ResponseEntity<AlgorithmApiResponse<TimeSlotConvertResult>> response = restTemplate.exchange(
                properties.algorithmServiceBaseUrl() + "/api/timeslot/convert",
                HttpMethod.POST,
                new org.springframework.http.HttpEntity<>(request),
                new ParameterizedTypeReference<>() {
                }
        );
        return requireData(response.getBody());
    }

    private static <T> T requireData(AlgorithmApiResponse<T> response) {
        if (response == null || response.data() == null) {
            throw new IllegalStateException("algorithm-service returned empty response");
        }
        return response.data();
    }
}

