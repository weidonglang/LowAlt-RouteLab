package com.lowalt.routelab.adapter.task;

import com.lowalt.routelab.adapter.algorithm.AlgorithmPlanResult;

import java.time.LocalDateTime;
import java.util.List;

public record RoutePlanSnapshot(
        long id,
        String algorithm,
        boolean success,
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
        String error,
        LocalDateTime createdAt
) {
    public static RoutePlanSnapshot from(long id, AlgorithmPlanResult result) {
        return new RoutePlanSnapshot(
                id,
                result.algorithm(),
                result.success(),
                result.path() == null ? List.of() : List.copyOf(result.path()),
                result.distance(),
                result.estimatedTimeSeconds(),
                result.turnCount(),
                result.planningTimeMs(),
                result.visitedCount(),
                result.riskScore(),
                result.riskLevel(),
                result.riskFactors() == null ? List.of() : List.copyOf(result.riskFactors()),
                result.estimatedBatteryUsage(),
                result.batteryLimit(),
                result.energySafe(),
                result.error(),
                LocalDateTime.now()
        );
    }
}

