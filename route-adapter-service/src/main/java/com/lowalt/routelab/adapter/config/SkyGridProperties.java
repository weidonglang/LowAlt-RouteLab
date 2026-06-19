package com.lowalt.routelab.adapter.config;

import org.springframework.boot.context.properties.ConfigurationProperties;

@ConfigurationProperties(prefix = "skygrid")
public record SkyGridProperties(
        String mode,
        String baseUrl,
        String token,
        Integer timeoutMs,
        Long orgId,
        Long applicantUserId,
        String applicantName,
        Long routeTemplateId,
        Long defaultLevelId
) {
    public String normalizedMode() {
        return mode == null || mode.isBlank() ? "mock" : mode.trim().toLowerCase();
    }

    public String normalizedBaseUrl() {
        return baseUrl == null || baseUrl.isBlank() ? "http://127.0.0.1:8080" : trimTrailingSlash(baseUrl.trim());
    }

    public int normalizedTimeoutMs() {
        return timeoutMs == null || timeoutMs <= 0 ? 5000 : timeoutMs;
    }

    public Long normalizedOrgId() {
        return orgId == null ? 1L : orgId;
    }

    public Long normalizedApplicantUserId() {
        return applicantUserId == null ? 1L : applicantUserId;
    }

    public String normalizedApplicantName() {
        return applicantName == null || applicantName.isBlank() ? "lowalt-route-adapter" : applicantName.trim();
    }

    public Long normalizedRouteTemplateId() {
        return routeTemplateId == null ? 1L : routeTemplateId;
    }

    public Long normalizedDefaultLevelId() {
        return defaultLevelId == null ? 1L : defaultLevelId;
    }

    private static String trimTrailingSlash(String value) {
        while (value.endsWith("/")) {
            value = value.substring(0, value.length() - 1);
        }
        return value;
    }
}
