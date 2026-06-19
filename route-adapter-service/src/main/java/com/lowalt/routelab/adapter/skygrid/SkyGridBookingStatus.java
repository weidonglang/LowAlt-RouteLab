package com.lowalt.routelab.adapter.skygrid;

public record SkyGridBookingStatus(
        String bookingId,
        String status,
        String message
) {
}
