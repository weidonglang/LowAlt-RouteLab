package com.lowalt.routelab.adapter.task;

import com.lowalt.routelab.adapter.algorithm.TimeSlotConvertResult;
import com.lowalt.routelab.adapter.skygrid.ConflictCheckResult;
import com.lowalt.routelab.adapter.skygrid.SkyGridSubmitResult;

import java.time.LocalDateTime;
import java.util.List;

public record RouteTaskResponse(
        long id,
        String taskName,
        String taskType,
        String mapId,
        String startGrid,
        String endGrid,
        String startLevel,
        String droneModel,
        String algorithm,
        boolean avoidRisk,
        boolean allowDiagonal,
        boolean connectSkyGrid,
        LocalDateTime startTime,
        double speedMps,
        double gridSizeMeters,
        int slotMinutes,
        String status,
        RoutePlanSnapshot plan,
        List<TimeSlotConvertResult.OccupancyUnit> occupancyUnits,
        ConflictCheckResult conflictCheck,
        SkyGridSubmitResult skyGridSubmit,
        LocalDateTime createdAt,
        LocalDateTime updatedAt
) {
    public static RouteTaskResponse from(RouteTask task) {
        return new RouteTaskResponse(
                task.id(),
                task.taskName(),
                task.taskType(),
                task.mapId(),
                task.startGrid(),
                task.endGrid(),
                task.startLevel(),
                task.droneModel(),
                task.algorithm(),
                task.avoidRisk(),
                task.allowDiagonal(),
                task.connectSkyGrid(),
                task.startTime(),
                task.speedMps(),
                task.gridSizeMeters(),
                task.slotMinutes(),
                task.status(),
                task.plan(),
                task.occupancyUnits(),
                task.conflictCheck(),
                task.skyGridSubmit(),
                task.createdAt(),
                task.updatedAt()
        );
    }
}

