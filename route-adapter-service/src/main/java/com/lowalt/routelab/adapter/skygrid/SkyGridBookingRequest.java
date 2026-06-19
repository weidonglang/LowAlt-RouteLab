package com.lowalt.routelab.adapter.skygrid;

import java.util.List;

public record SkyGridBookingRequest(
        long taskId,
        long planId,
        String taskName,
        String startGrid,
        String endGrid,
        String altitudeLevel,
        String algorithmType,
        double pathLength,
        int turnCount,
        double riskScore,
        double energyCost,
        List<SkyGridOccupancySlot> occupancySlots
) {
}
