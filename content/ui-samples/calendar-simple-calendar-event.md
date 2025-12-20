<Path>Add-ons > Calendar > Calendar with SimpleCalendarEvent</Path>

The SimpleCalendarEvent is the easiest way to create an event. It can be used as an alternative to DTOs in services.

calendar-simple-calendar-event.xml

<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<view xmlns="http://jmix.io/schema/flowui/view"
      xmlns:calendar="http://jmix.io/schema/fullcalendar/ui">
    <layout>
        <calendar:calendar id="calendar"
                           height="100%"
                           width="100%"
                           minHeight="30em"/>
    </layout>
</view>



CalendarSimpleCalendarEventSample.java

package io.jmix.uisamples.view.flowui.calendar.simplecalendarevent;

import io.jmix.flowui.view.*;
import io.jmix.fullcalendarflowui.component.FullCalendar;
import io.jmix.fullcalendarflowui.component.data.ListCalendarDataProvider;
import io.jmix.fullcalendarflowui.component.data.SimpleCalendarEvent;

import java.time.LocalDate;
import java.time.LocalTime;
import java.util.List;

@ViewController("calendar-simple-calendar-event")
@ViewDescriptor("calendar-simple-calendar-event.xml")
public class CalendarSimpleCalendarEventSample extends StandardView {

    @ViewComponent
    private FullCalendar calendar;

    @Subscribe
    public void onInit(final InitEvent event) {
        SimpleCalendarEvent calendarEvent = SimpleCalendarEvent.create()
                .withTitle("Meeting")
                .withStartDateTime(LocalDate.now().withDayOfMonth(10), LocalTime.of(15, 0))
                .build();

        calendar.addDataProvider(new ListCalendarDataProvider(List.of(calendarEvent)));
    }
}


