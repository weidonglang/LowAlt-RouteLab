package com.lowalt.routelab.adapter.skygrid;

import com.lowalt.routelab.adapter.task.RouteTask;
import org.springframework.stereotype.Component;

@Component
public class RoutePlanToSkyGridBookingMapper {

    private final TimeSlotOccupancyMapper occupancyMapper;

    public RoutePlanToSkyGridBookingMapper(TimeSlotOccupancyMapper occupancyMapper) {
        this.occupancyMapper = occupancyMapper;
    }

    public SkyGridBookingRequest toBookingRequest(RouteTask task) {
        if (task.plan() == null) {
            throw new IllegalStateException("route task has no plan snapshot");
        }
        return new SkyGridBookingRequest(
                task.id(),
                task.plan().id(),
                task.taskName(),
                task.startGrid(),
                task.endGrid(),
                task.startLevel(),
                task.plan().algorithm(),
                task.plan().distance(),
                task.plan().turnCount(),
                task.plan().riskScore(),
                task.plan().estimatedBatteryUsage(),
                occupancyMapper.toSkyGridSlots(task.occupancyUnits())
        );
    }
}
