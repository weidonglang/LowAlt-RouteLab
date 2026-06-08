package com.lowalt.routelab.adapter.skygrid;

import com.lowalt.routelab.adapter.algorithm.TimeSlotConvertResult;

import java.util.List;

public interface SkyGridClient {

    ConflictCheckResult checkConflict(List<TimeSlotConvertResult.OccupancyUnit> occupancyUnits);

    SkyGridSubmitResult submitBooking(long taskId, long planId, List<TimeSlotConvertResult.OccupancyUnit> occupancyUnits);
}

