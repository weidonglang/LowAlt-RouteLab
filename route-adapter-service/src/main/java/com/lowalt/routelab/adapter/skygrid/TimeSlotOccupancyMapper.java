package com.lowalt.routelab.adapter.skygrid;

import com.lowalt.routelab.adapter.algorithm.TimeSlotConvertResult;
import org.springframework.stereotype.Component;

import java.util.List;

@Component
public class TimeSlotOccupancyMapper {

    public List<SkyGridOccupancySlot> toSkyGridSlots(List<TimeSlotConvertResult.OccupancyUnit> units) {
        if (units == null || units.isEmpty()) {
            return List.of();
        }
        return units.stream()
                .map(unit -> new SkyGridOccupancySlot(
                        unit.gridId(),
                        unit.levelId(),
                        String.valueOf(unit.sequenceNo()),
                        unit.slotStart(),
                        unit.slotEnd()
                ))
                .toList();
    }
}
