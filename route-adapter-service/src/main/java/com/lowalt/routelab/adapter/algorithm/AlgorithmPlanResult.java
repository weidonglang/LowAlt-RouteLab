package com.lowalt.routelab.adapter.algorithm;

import java.util.List;

public record AlgorithmPlanResult(
        boolean success,
        String algorithm,
        List<String> path,
        double distance,
        int estimatedTimeSeconds,
        int turnCount,
        int planningTimeMs,
        int visitedCount,
        double riskScore,
        String riskLevel,
        List<String> riskFactors,
        double estimatedBatteryUsage,
        double batteryLimit,
        boolean energySafe,
        String error
) {
}

