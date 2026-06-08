package com.lowalt.routelab.adapter.skygrid;

import com.lowalt.routelab.adapter.algorithm.TimeSlotConvertResult;
import org.springframework.stereotype.Component;

import java.util.List;

@Component
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
}

