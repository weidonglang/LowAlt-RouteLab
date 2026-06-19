package com.lowalt.routelab.adapter;

import com.lowalt.routelab.adapter.algorithm.AlgorithmPlanResult;
import com.lowalt.routelab.adapter.algorithm.TimeSlotConvertResult;
import com.lowalt.routelab.adapter.skygrid.RoutePlanToSkyGridBookingMapper;
import com.lowalt.routelab.adapter.skygrid.SkyGridBookingRequest;
import com.lowalt.routelab.adapter.skygrid.TimeSlotOccupancyMapper;
import com.lowalt.routelab.adapter.task.CreateRouteTaskRequest;
import com.lowalt.routelab.adapter.task.RoutePlanSnapshot;
import com.lowalt.routelab.adapter.task.RouteTask;
import org.junit.jupiter.api.Test;

import java.time.LocalDateTime;
import java.util.List;

import static org.assertj.core.api.Assertions.assertThat;

class SkyGridIntegrationMappingTest {

    @Test
    void mapsRoutePlanToSkyGridBookingRequest() {
        RouteTask task = new RouteTask(9L, request());
        task.markPlanned(RoutePlanSnapshot.from(3L, planResult()), List.of(unit()));
        RoutePlanToSkyGridBookingMapper mapper = new RoutePlanToSkyGridBookingMapper(new TimeSlotOccupancyMapper());

        SkyGridBookingRequest mapped = mapper.toBookingRequest(task);

        assertThat(mapped.taskId()).isEqualTo(9L);
        assertThat(mapped.planId()).isEqualTo(3L);
        assertThat(mapped.taskName()).isEqualTo("East district inspection");
        assertThat(mapped.startGrid()).isEqualTo("G-02-03");
        assertThat(mapped.endGrid()).isEqualTo("G-16-14");
        assertThat(mapped.altitudeLevel()).isEqualTo("L120");
        assertThat(mapped.algorithmType()).isEqualTo("A_STAR");
        assertThat(mapped.pathLength()).isEqualTo(420.0);
        assertThat(mapped.turnCount()).isEqualTo(4);
        assertThat(mapped.riskScore()).isEqualTo(0.28);
        assertThat(mapped.energyCost()).isEqualTo(7.5);
        assertThat(mapped.occupancySlots()).hasSize(1);
        assertThat(mapped.occupancySlots().get(0).gridId()).isEqualTo("G-02-03");
        assertThat(mapped.occupancySlots().get(0).timeSlotId()).isEqualTo("2");
    }

    private static CreateRouteTaskRequest request() {
        return new CreateRouteTaskRequest(
                "East district inspection",
                "POWER_LINE_INSPECTION",
                "demo-city-20x20",
                "G-02-03",
                "G-16-14",
                "L120",
                "M30",
                "A_STAR",
                true,
                true,
                true,
                LocalDateTime.of(2026, 6, 20, 10, 0),
                10.0,
                100.0,
                5
        );
    }

    private static AlgorithmPlanResult planResult() {
        return new AlgorithmPlanResult(
                true,
                "A_STAR",
                List.of("G-02-03", "G-02-04", "G-03-04"),
                420.0,
                120,
                4,
                18,
                33,
                0.28,
                "LOW",
                List.of("risk-zone bypassed"),
                7.5,
                80.0,
                true,
                null
        );
    }

    private static TimeSlotConvertResult.OccupancyUnit unit() {
        return new TimeSlotConvertResult.OccupancyUnit(
                "G-02-03",
                "L120",
                "2026-06-20T10:00:00",
                "2026-06-20T10:05:00",
                1
        );
    }
}
