package com.lowalt.routelab.adapter;

import com.lowalt.routelab.adapter.algorithm.TimeSlotConvertResult;
import com.lowalt.routelab.adapter.skygrid.ConflictCheckResult;
import com.lowalt.routelab.adapter.skygrid.MockSkyGridClient;
import com.lowalt.routelab.adapter.skygrid.SkyGridSubmitResult;
import org.junit.jupiter.api.Test;

import java.util.List;

import static org.assertj.core.api.Assertions.assertThat;

class MockSkyGridClientTest {

    @Test
    void checkConflictReturnsDemoRiskConflict() {
        MockSkyGridClient client = new MockSkyGridClient();

        ConflictCheckResult result = client.checkConflict(List.of(unit()));

        assertThat(result.conflictStatus()).isEqualTo("RISK_CONFLICT");
        assertThat(result.conflicts()).hasSize(1);
        assertThat(result.conflicts().get(0).conflictType()).isEqualTo("ADJACENT_GRID_RISK");
    }

    @Test
    void submitBookingReturnsMockBookingId() {
        MockSkyGridClient client = new MockSkyGridClient();

        SkyGridSubmitResult result = client.submitBooking(1L, 2L, List.of(unit()));

        assertThat(result.bookingStatus()).isEqualTo("MOCK_SUBMITTED");
        assertThat(result.bookingId()).isEqualTo("MOCK-SG-1-2");
    }

    @Test
    void previewAndStatusRemainAvailableInMockMode() {
        MockSkyGridClient client = new MockSkyGridClient();

        assertThat(client.submitOccupancyPreview(List.of(unit())).previewStatus()).isEqualTo("MOCK_PREVIEW");
        assertThat(client.getBookingStatus("MOCK-SG-1-2").status()).isEqualTo("MOCK_SUBMITTED");
        assertThat(client.getConflictResolutionSuggestions("MOCK-SG-1-2")).hasSize(1);
    }

    private static TimeSlotConvertResult.OccupancyUnit unit() {
        return new TimeSlotConvertResult.OccupancyUnit(
                "G-01-01",
                "L120",
                "2026-06-08T10:00:00",
                "2026-06-08T10:05:00",
                1
        );
    }
}

