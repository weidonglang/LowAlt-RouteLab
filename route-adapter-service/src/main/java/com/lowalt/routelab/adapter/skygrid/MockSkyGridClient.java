package com.lowalt.routelab.adapter.skygrid;

import com.lowalt.routelab.adapter.algorithm.TimeSlotConvertResult;

import java.util.List;

public class MockSkyGridClient implements SkyGridClient {

    @Override
    public ConflictCheckResult checkConflict(List<TimeSlotConvertResult.OccupancyUnit> occupancyUnits) {
        return new ConflictCheckResult(
                "RISK_CONFLICT",
                1,
                List.of(new ConflictCheckResult.ConflictItem(
                        "G-05-07",
                        "L120",
                        "2026-06-08T10:10:00",
                        "2026-06-08T10:15:00",
                        "ADJACENT_GRID_RISK",
                        "Adjacent grid has a simulated task, manual review is suggested"
                ))
        );
    }

    @Override
    public SkyGridSubmitResult submitBooking(
            long taskId,
            long planId,
            List<TimeSlotConvertResult.OccupancyUnit> occupancyUnits
    ) {
        return new SkyGridSubmitResult(
                "MOCK_SUBMITTED",
                "MOCK-SG-" + taskId + "-" + planId,
                "Mock SkyGrid booking submitted"
        );
    }

    @Override
    public ConflictCheckResult checkConflict(SkyGridBookingRequest request) {
        return checkConflict(List.of());
    }

    @Override
    public SkyGridSubmitResult submitBooking(SkyGridBookingRequest request) {
        return submitBooking(request.taskId(), request.planId(), List.of());
    }

    @Override
    public SkyGridBookingStatus getBookingStatus(String bookingId) {
        return new SkyGridBookingStatus(bookingId, "MOCK_SUBMITTED", "Mock SkyGrid booking status");
    }

    @Override
    public SkyGridOccupancyPreviewResult submitOccupancyPreview(List<TimeSlotConvertResult.OccupancyUnit> occupancyUnits) {
        return new SkyGridOccupancyPreviewResult("MOCK_PREVIEW", occupancyUnits.size(), "Mock occupancy preview accepted");
    }

    @Override
    public List<ConflictResolutionSuggestion> getConflictResolutionSuggestions(String bookingId) {
        return List.of(new ConflictResolutionSuggestion(
                "MOCK-CONFLICT-1",
                "RISK_CONFLICT",
                "G-05-07",
                "L120",
                "1",
                "MANUAL_REVIEW_OR_ADJACENT_GRID",
                "Mock suggestion: route through adjacent grid or submit to manual review"
        ));
    }
}

