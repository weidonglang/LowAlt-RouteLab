package com.lowalt.routelab.adapter.skygrid;

import com.lowalt.routelab.adapter.algorithm.TimeSlotConvertResult;

import java.util.List;

public interface SkyGridClient {

    ConflictCheckResult checkConflict(List<TimeSlotConvertResult.OccupancyUnit> occupancyUnits);

    SkyGridSubmitResult submitBooking(long taskId, long planId, List<TimeSlotConvertResult.OccupancyUnit> occupancyUnits);

    ConflictCheckResult checkConflict(SkyGridBookingRequest request);

    SkyGridSubmitResult submitBooking(SkyGridBookingRequest request);

    SkyGridBookingStatus getBookingStatus(String bookingId);

    SkyGridOccupancyPreviewResult submitOccupancyPreview(List<TimeSlotConvertResult.OccupancyUnit> occupancyUnits);

    List<ConflictResolutionSuggestion> getConflictResolutionSuggestions(String bookingId);
}

