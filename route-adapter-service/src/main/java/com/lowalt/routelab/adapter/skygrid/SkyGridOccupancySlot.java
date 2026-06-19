package com.lowalt.routelab.adapter.skygrid;

public record SkyGridOccupancySlot(
        String gridId,
        String levelId,
        String timeSlotId,
        String startTime,
        String endTime
) {
}
