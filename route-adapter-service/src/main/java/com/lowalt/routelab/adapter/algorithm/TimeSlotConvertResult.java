package com.lowalt.routelab.adapter.algorithm;

import java.util.List;

public record TimeSlotConvertResult(
        List<OccupancyUnit> occupancyUnits
) {
    public record OccupancyUnit(
            String gridId,
            String levelId,
            String slotStart,
            String slotEnd,
            int sequenceNo
    ) {
    }
}

