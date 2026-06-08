package com.lowalt.routelab.adapter.algorithm;

public record AlgorithmPlanRequest(
        String mapId,
        String taskType,
        String startGrid,
        String endGrid,
        String level,
        String algorithm,
        boolean avoidRisk,
        boolean allowDiagonal
) {
}

