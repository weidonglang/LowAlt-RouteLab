package com.lowalt.routelab.adapter.skygrid;

import com.lowalt.routelab.adapter.algorithm.TimeSlotConvertResult;
import org.springframework.stereotype.Component;

import java.time.LocalDateTime;
import java.time.LocalTime;
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
                        String.valueOf(timeSlotId(unit.slotStart())),
                        unit.slotStart(),
                        unit.slotEnd()
                ))
                .toList();
    }

    private static long timeSlotId(String slotStart) {
        if (slotStart == null || slotStart.isBlank()) {
            return 1L;
        }
        LocalTime start = LocalDateTime.parse(slotStart).toLocalTime();
        if (start.isBefore(LocalTime.of(10, 0))) {
            return 1L;
        }
        if (start.isBefore(LocalTime.of(12, 0))) {
            return 2L;
        }
        if (start.isBefore(LocalTime.of(16, 0))) {
            return 3L;
        }
        return 4L;
    }
}
