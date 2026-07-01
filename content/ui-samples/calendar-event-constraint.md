<Path>Add-ons > Calendar > Calendar with event constraints</Path>

The eventConstraintGroupId property sets the name of the group that should be used as a constraint for dragging and resizing calendar events. This property works across data providers. Another way to specify a constraint is to use the eventConstraintBusinessHoursEnabled property. If this property is enabled, the component will adhere to the specified business hours as a constraint for calendar event. Calendar events that have the same group ID will be moved together.

calendar-event-constraint.xml

<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<view xmlns="http://jmix.io/schema/flowui/view"
      xmlns:calendar="http://jmix.io/schema/fullcalendar/ui">
    <layout>
        <div classNames="rounded-panel">
            <span text="msg://sampleDescription.text"/>
        </div>
        <calendar:calendar id="calendar"
                           eventStartEditable="true"
                           eventConstraintGroupId="workDays"
                           height="100%"
                           width="100%"
                           minHeight="30em"/>
    </layout>
</view>



CalendarEventConstraintSample.java

package io.jmix.uisamples.view.flowui.calendar.eventconstraint;

import io.jmix.flowui.view.*;
import io.jmix.fullcalendarflowui.component.FullCalendar;
import io.jmix.fullcalendarflowui.component.data.ListCalendarDataProvider;

@ViewController("calendar-event-constraint")
@ViewDescriptor("calendar-event-constraint.xml")
public class CalendarEventConstraintSample extends StandardView {

    @ViewComponent
    private FullCalendar calendar;

    @Subscribe
    public void onInit(final InitEvent event) {
        calendar.addDataProvider(new ListCalendarDataProvider(EventsHelper.generateEvents()));
        calendar.addDataProvider(new ListCalendarDataProvider(EventsHelper.generateBackgroundEvents()));
    }
}




EventsHelper.java

package io.jmix.uisamples.view.flowui.calendar.eventconstraint;

import io.jmix.fullcalendarflowui.component.data.CalendarEvent;
import io.jmix.fullcalendarflowui.component.data.SimpleCalendarEvent;
import io.jmix.fullcalendarflowui.component.model.Display;

import java.time.LocalDate;
import java.time.LocalDateTime;
import java.time.LocalTime;
import java.util.List;

public final class EventsHelper {

    public static List<CalendarEvent> generateEvents() {
        return List.of(
                SimpleCalendarEvent.create()
                        .withTitle("Event-1 GP1")
                        .withGroupId("GP1")
                        .withStartDateTime(LocalDateTime.now())
                        .build(),
                SimpleCalendarEvent.create()
                        .withTitle("Event-2 GP1")
                        .withGroupId("GP1")
                        .withStartDateTime(LocalDateTime.now().plusDays(1))
                        .build()
        );
    }

    public static List<CalendarEvent> generateBackgroundEvents() {
        return List.of(
                SimpleCalendarEvent.create()
                        .withTitle("Work days")
                        .withGroupId("workDays")
                        .withAllDay(true)
                        .withDisplay(Display.BACKGROUND)
                        .withStartDateTime(LocalDate.now().minusDays(17), LocalTime.MIDNIGHT)
                        .withEndDateTime(LocalDate.now().minusDays(14), LocalTime.MIDNIGHT)
                        .build(),
                SimpleCalendarEvent.create()
                        .withTitle("Work days")
                        .withGroupId("workDays")
                        .withAllDay(true)
                        .withDisplay(Display.BACKGROUND)
                        .withStartDateTime(LocalDate.now().minusDays(7), LocalTime.MIDNIGHT)
                        .withEndDateTime(LocalDate.now().minusDays(4), LocalTime.MIDNIGHT)
                        .build(),
                SimpleCalendarEvent.create()
                        .withTitle("Work days")
                        .withGroupId("workDays")
                        .withAllDay(true)
                        .withDisplay(Display.BACKGROUND)
                        .withStartDateTime(LocalDate.now().plusDays(4), LocalTime.MIDNIGHT)
                        .withEndDateTime(LocalDate.now().plusDays(7), LocalTime.MIDNIGHT)
                        .build(),
                SimpleCalendarEvent.create()
                        .withTitle("Work days")
                        .withGroupId("workDays")
                        .withAllDay(true)
                        .withDisplay(Display.BACKGROUND)
                        .withStartDateTime(LocalDate.now().plusDays(14), LocalTime.MIDNIGHT)
                        .withEndDateTime(LocalDate.now().plusDays(17), LocalTime.MIDNIGHT)
                        .build()
        );
    }
}


