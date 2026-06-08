package com.lowalt.routelab.adapter.task;

import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import jakarta.validation.constraints.Positive;

import java.time.LocalDateTime;

public record CreateRouteTaskRequest(
        @NotBlank String taskName,
        @NotBlank String taskType,
        String mapId,
        @NotBlank String startGrid,
        @NotBlank String endGrid,
        @NotBlank String startLevel,
        String droneModel,
        String algorithm,
        Boolean avoidRisk,
        Boolean allowDiagonal,
        Boolean connectSkyGrid,
        @NotNull LocalDateTime startTime,
        @Positive Double speedMps,
        @Positive Double gridSizeMeters,
        @Positive Integer slotMinutes
) {
}

