package com.lowalt.routelab.adapter;

import com.lowalt.routelab.adapter.algorithm.TimeSlotConvertResult;
import com.lowalt.routelab.adapter.config.SkyGridProperties;
import com.lowalt.routelab.adapter.skygrid.ConflictCheckResult;
import com.lowalt.routelab.adapter.skygrid.RealSkyGridClient;
import com.lowalt.routelab.adapter.skygrid.SkyGridSubmitResult;
import org.junit.jupiter.api.Test;
import org.springframework.http.MediaType;
import org.springframework.test.web.client.MockRestServiceServer;
import org.springframework.web.client.RestTemplate;

import java.util.List;

import static org.assertj.core.api.Assertions.assertThat;
import static org.springframework.test.web.client.match.MockRestRequestMatchers.header;
import static org.springframework.test.web.client.match.MockRestRequestMatchers.jsonPath;
import static org.springframework.test.web.client.match.MockRestRequestMatchers.method;
import static org.springframework.test.web.client.match.MockRestRequestMatchers.requestTo;
import static org.springframework.test.web.client.response.MockRestResponseCreators.withSuccess;
import static org.springframework.http.HttpHeaders.AUTHORIZATION;
import static org.springframework.http.HttpMethod.POST;

class RealSkyGridClientTest {

    @Test
    void checkConflictMapsOccupancyToSkyGridPreCheckRequest() {
        RestTemplate restTemplate = new RestTemplate();
        MockRestServiceServer server = MockRestServiceServer.bindTo(restTemplate).build();
        RealSkyGridClient client = new RealSkyGridClient(restTemplate, properties());
        server.expect(requestTo("http://skygrid.test/api/bookings/pre-check"))
                .andExpect(method(POST))
                .andExpect(header(AUTHORIZATION, "Bearer dev-token"))
                .andExpect(jsonPath("$.taskName").value("LowAlt conflict preview"))
                .andExpect(jsonPath("$.routeTemplateId").value(1))
                .andExpect(jsonPath("$.levelId").value(2))
                .andExpect(jsonPath("$.timeSlotIds[0]").value(1))
                .andRespond(withSuccess("""
                        {
                          "success": true,
                          "code": "OK",
                          "message": "pre-check finished",
                          "data": {
                            "conflicts": [
                              {
                                "gridCode": "G-08-12",
                                "levelId": 1,
                                "conflictType": "HARD",
                                "message": "same grid level time slot"
                              }
                            ]
                          }
                        }
                        """, MediaType.APPLICATION_JSON));

        ConflictCheckResult result = client.checkConflict(List.of(unit()));

        assertThat(result.conflictStatus()).isEqualTo("HARD_CONFLICT");
        assertThat(result.conflictCount()).isEqualTo(1);
        assertThat(result.conflicts().get(0).gridId()).isEqualTo("G-08-12");
        server.verify();
    }

    @Test
    void submitBookingReturnsSkyGridBookingId() {
        RestTemplate restTemplate = new RestTemplate();
        MockRestServiceServer server = MockRestServiceServer.bindTo(restTemplate).build();
        RealSkyGridClient client = new RealSkyGridClient(restTemplate, properties());
        server.expect(requestTo("http://skygrid.test/api/bookings"))
                .andExpect(method(POST))
                .andExpect(jsonPath("$.taskName").value("LowAlt route task 7"))
                .andRespond(withSuccess("""
                        {
                          "success": true,
                          "code": "OK",
                          "message": "booking submitted",
                          "data": {
                            "id": 42,
                            "status": "PENDING"
                          }
                        }
                        """, MediaType.APPLICATION_JSON));

        SkyGridSubmitResult result = client.submitBooking(7L, 3L, List.of(unit()));

        assertThat(result.bookingStatus()).isEqualTo("PENDING");
        assertThat(result.bookingId()).isEqualTo("42");
        server.verify();
    }

    private static SkyGridProperties properties() {
        return new SkyGridProperties(
                "real",
                "http://skygrid.test",
                "dev-token",
                5000,
                1L,
                1L,
                "tester",
                1L,
                1L
        );
    }

    private static TimeSlotConvertResult.OccupancyUnit unit() {
        return new TimeSlotConvertResult.OccupancyUnit(
                "G-08-12",
                "L120",
                "2026-06-15T10:10:00",
                "2026-06-15T10:15:00",
                1
        );
    }
}
