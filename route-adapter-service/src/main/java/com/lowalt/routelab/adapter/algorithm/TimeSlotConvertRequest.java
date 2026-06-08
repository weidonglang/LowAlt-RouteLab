package com.lowalt.routelab.adapter.algorithm;

import java.util.List;

public record TimeSlotConvertRequest(
        List<String> path,
        String level,
        String startTime,
        double speed,
        double gridSizeMeters,
        int slotMinutes
) {
}

