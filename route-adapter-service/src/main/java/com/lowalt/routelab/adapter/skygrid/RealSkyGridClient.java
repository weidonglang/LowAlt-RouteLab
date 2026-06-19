package com.lowalt.routelab.adapter.skygrid;

import com.lowalt.routelab.adapter.algorithm.TimeSlotConvertResult;
import com.lowalt.routelab.adapter.config.SkyGridProperties;
import org.springframework.http.HttpEntity;
import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpMethod;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.client.ResourceAccessException;
import org.springframework.web.client.RestClientResponseException;
import org.springframework.web.client.RestTemplate;

import java.time.LocalDate;
import java.time.LocalDateTime;
import java.time.LocalTime;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;

public class RealSkyGridClient implements SkyGridClient {

    private final RestTemplate restTemplate;
    private final SkyGridProperties properties;

    public RealSkyGridClient(RestTemplate restTemplate, SkyGridProperties properties) {
        this.restTemplate = restTemplate;
        this.properties = properties;
    }

    @Override
    public ConflictCheckResult checkConflict(List<TimeSlotConvertResult.OccupancyUnit> occupancyUnits) {
        Map<String, Object> request = toBookingRequest("LowAlt conflict preview", 0L, 0L, occupancyUnits);
        return checkConflict(request);
    }

    @Override
    public ConflictCheckResult checkConflict(SkyGridBookingRequest request) {
        return checkConflict(toBookingRequest(request));
    }

    private ConflictCheckResult checkConflict(Map<String, Object> request) {
        Map<String, Object> data = postForData("/api/bookings/pre-check", request);
        List<ConflictCheckResult.ConflictItem> conflicts = toConflictItems(data);
        String status = conflicts.isEmpty()
                ? "NO_CONFLICT"
                : conflicts.stream().anyMatch(item -> "HARD".equalsIgnoreCase(item.conflictType()) || "BLOCKING".equalsIgnoreCase(item.conflictType()))
                ? "HARD_CONFLICT"
                : "RISK_CONFLICT";
        return new ConflictCheckResult(status, conflicts.size(), conflicts);
    }

    @Override
    public SkyGridSubmitResult submitBooking(long taskId, long planId, List<TimeSlotConvertResult.OccupancyUnit> occupancyUnits) {
        Map<String, Object> request = toBookingRequest("LowAlt route task " + taskId, taskId, planId, occupancyUnits);
        return submitBooking(request);
    }

    @Override
    public SkyGridSubmitResult submitBooking(SkyGridBookingRequest request) {
        return submitBooking(toBookingRequest(request));
    }

    private SkyGridSubmitResult submitBooking(Map<String, Object> request) {
        Map<String, Object> data = postForData("/api/bookings", request);
        String bookingId = stringValue(data.get("id"));
        String status = stringValue(data.get("status"));
        return new SkyGridSubmitResult(status == null ? "SUBMITTED" : status, bookingId, "SkyGrid booking submitted through Gateway");
    }

    @Override
    public SkyGridBookingStatus getBookingStatus(String bookingId) {
        Map<String, Object> data = getForData("/api/bookings/" + bookingId);
        return new SkyGridBookingStatus(bookingId, stringValue(data.get("status")), "SkyGrid booking status loaded");
    }

    @Override
    public SkyGridOccupancyPreviewResult submitOccupancyPreview(List<TimeSlotConvertResult.OccupancyUnit> occupancyUnits) {
        ConflictCheckResult result = checkConflict(occupancyUnits);
        return new SkyGridOccupancyPreviewResult(result.conflictStatus(), occupancyUnits.size(), "SkyGrid occupancy preview checked");
    }

    @Override
    public List<ConflictResolutionSuggestion> getConflictResolutionSuggestions(String bookingId) {
        Map<String, Object> data = postForData("/api/conflicts/resolve-suggestions?bookingId=" + bookingId, Map.of());
        Object suggestions = data.get("suggestions");
        if (!(suggestions instanceof List<?> list)) {
            return List.of();
        }
        return list.stream()
                .filter(Map.class::isInstance)
                .map(Map.class::cast)
                .map(item -> new ConflictResolutionSuggestion(
                        stringValue(item.get("conflictId")),
                        stringValue(item.get("conflictType")),
                        stringValue(item.get("gridCode")),
                        stringValue(item.get("levelId")),
                        stringValue(item.get("timeSlotId")),
                        stringValue(item.get("suggestedAction")),
                        stringValue(item.get("suggestion"))
                ))
                .toList();
    }

    private Map<String, Object> toBookingRequest(String taskName, long taskId, long planId, List<TimeSlotConvertResult.OccupancyUnit> units) {
        if (units == null || units.isEmpty()) {
            throw new IllegalArgumentException("occupancySlots must not be empty");
        }
        TimeSlotConvertResult.OccupancyUnit first = units.get(0);
        Map<String, Object> request = new LinkedHashMap<>();
        request.put("taskName", taskName);
        request.put("orgId", properties.normalizedOrgId());
        request.put("applicantUserId", properties.normalizedApplicantUserId());
        request.put("applicantName", properties.normalizedApplicantName());
        request.put("routeTemplateId", properties.normalizedRouteTemplateId());
        request.put("levelId", levelId(first.levelId()));
        request.put("bookingDate", bookingDate(first.slotStart()).toString());
        request.put("timeSlotIds", units.stream().map(this::timeSlotId).distinct().toList());
        request.put("applyReason", "LowAlt-RouteLab real SkyGrid integration");
        request.put("description", "taskId=" + taskId + ", planId=" + planId + ", occupancySlots=" + units.size());
        return request;
    }

    private Map<String, Object> toBookingRequest(SkyGridBookingRequest request) {
        if (request.occupancySlots() == null || request.occupancySlots().isEmpty()) {
            throw new IllegalArgumentException("occupancySlots must not be empty");
        }
        SkyGridOccupancySlot first = request.occupancySlots().get(0);
        Map<String, Object> skyGridRequest = new LinkedHashMap<>();
        skyGridRequest.put("taskName", firstNonBlank(request.taskName(), "LowAlt route task " + request.taskId()));
        skyGridRequest.put("orgId", properties.normalizedOrgId());
        skyGridRequest.put("applicantUserId", properties.normalizedApplicantUserId());
        skyGridRequest.put("applicantName", properties.normalizedApplicantName());
        skyGridRequest.put("routeTemplateId", properties.normalizedRouteTemplateId());
        skyGridRequest.put("levelId", levelId(first.levelId()));
        skyGridRequest.put("bookingDate", bookingDate(first.startTime()).toString());
        skyGridRequest.put("timeSlotIds", request.occupancySlots().stream().map(this::timeSlotId).distinct().toList());
        skyGridRequest.put("applyReason", "LowAlt-RouteLab real SkyGrid integration");
        skyGridRequest.put("description", "taskId=" + request.taskId()
                + ", planId=" + request.planId()
                + ", algorithm=" + request.algorithmType()
                + ", pathLength=" + request.pathLength()
                + ", turnCount=" + request.turnCount()
                + ", riskScore=" + request.riskScore()
                + ", energyCost=" + request.energyCost()
                + ", startGrid=" + request.startGrid()
                + ", endGrid=" + request.endGrid()
                + ", occupancySlots=" + request.occupancySlots().size());
        return skyGridRequest;
    }

    private Long levelId(String level) {
        if (level == null || level.isBlank()) {
            return properties.normalizedDefaultLevelId();
        }
        String normalized = level.trim().toUpperCase();
        if ("L1".equals(normalized)) {
            return 1L;
        }
        if ("L2".equals(normalized)) {
            return 2L;
        }
        if ("L3".equals(normalized)) {
            return 3L;
        }
        String digits = normalized.replaceAll("\\D+", "");
        if (digits.isBlank()) {
            return properties.normalizedDefaultLevelId();
        }
        if ("1".equals(digits) || "2".equals(digits) || "3".equals(digits)) {
            return Long.parseLong(digits);
        }
        if ("90".equals(digits)) {
            return 2L;
        }
        if ("120".equals(digits)) {
            return 2L;
        }
        if ("150".equals(digits)) {
            return 3L;
        }
        return properties.normalizedDefaultLevelId();
    }

    private Long timeSlotId(TimeSlotConvertResult.OccupancyUnit unit) {
        return timeSlotIdByStart(unit.slotStart());
    }

    private Long timeSlotId(SkyGridOccupancySlot slot) {
        if (slot.startTime() != null && !slot.startTime().isBlank()) {
            return timeSlotIdByStart(slot.startTime());
        }
        if (slot.timeSlotId() == null || slot.timeSlotId().isBlank()) {
            return 1L;
        }
        try {
            return Long.parseLong(slot.timeSlotId());
        } catch (NumberFormatException ignored) {
            return 1L;
        }
    }

    private Long timeSlotIdByStart(String slotStart) {
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

    private LocalDate bookingDate(String slotStart) {
        if (slotStart == null || slotStart.isBlank()) {
            return LocalDate.now().plusDays(1);
        }
        return LocalDateTime.parse(slotStart).toLocalDate();
    }

    @SuppressWarnings("unchecked")
    private Map<String, Object> getForData(String path) {
        ResponseEntity<Map> response = exchange(path, HttpMethod.GET, null);
        return requireData(response.getBody(), path);
    }

    @SuppressWarnings("unchecked")
    private Map<String, Object> postForData(String path, Map<String, Object> request) {
        ResponseEntity<Map> response = exchange(path, HttpMethod.POST, request);
        return requireData(response.getBody(), path);
    }

    private ResponseEntity<Map> exchange(String path, HttpMethod method, Map<String, Object> body) {
        HttpHeaders headers = new HttpHeaders();
        headers.setBearerAuth(properties.token().trim());
        HttpEntity<Map<String, Object>> entity = new HttpEntity<>(body, headers);
        try {
            return restTemplate.exchange(properties.normalizedBaseUrl() + path, method, entity, Map.class);
        } catch (ResourceAccessException ex) {
            throw new IllegalStateException("SkyGrid Gateway is unavailable. Start SkyGrid or switch skygrid.mode=mock.", ex);
        } catch (RestClientResponseException ex) {
            if (ex.getStatusCode() == HttpStatus.CONFLICT) {
                throw new IllegalStateException("SkyGrid reports an airspace conflict: " + ex.getResponseBodyAsString(), ex);
            }
            if (ex.getStatusCode().is5xxServerError()) {
                throw new IllegalStateException("SkyGrid platform service error: " + ex.getStatusCode(), ex);
            }
            throw new IllegalStateException("SkyGrid API request failed: HTTP " + ex.getStatusCode() + " " + ex.getResponseBodyAsString(), ex);
        }
    }

    @SuppressWarnings("unchecked")
    private Map<String, Object> requireData(Map body, String path) {
        if (body == null) {
            throw new IllegalStateException("SkyGrid API returned empty response for " + path);
        }
        Object success = body.get("success");
        if (Boolean.FALSE.equals(success)) {
            throw new IllegalStateException("SkyGrid API returned failure for " + path + ": " + body.get("message"));
        }
        Object data = body.get("data");
        if (data instanceof Map<?, ?> map) {
            return (Map<String, Object>) map;
        }
        throw new IllegalStateException("SkyGrid API returned empty data for " + path);
    }

    @SuppressWarnings("unchecked")
    private List<ConflictCheckResult.ConflictItem> toConflictItems(Map<String, Object> data) {
        Object conflicts = data.get("conflicts");
        if (!(conflicts instanceof List<?> list)) {
            return List.of();
        }
        return list.stream()
                .filter(Map.class::isInstance)
                .map(Map.class::cast)
                .map(item -> new ConflictCheckResult.ConflictItem(
                        stringValue(item.get("gridCode")),
                        stringValue(item.get("levelId")),
                        null,
                        null,
                        firstNonBlank(stringValue(item.get("conflictType")), stringValue(item.get("conflictLevel"))),
                        stringValue(item.get("message"))
                ))
                .toList();
    }

    private static String stringValue(Object value) {
        return value == null ? null : String.valueOf(value);
    }

    private static String firstNonBlank(String first, String second) {
        if (first != null && !first.isBlank()) {
            return first;
        }
        return second;
    }
}
