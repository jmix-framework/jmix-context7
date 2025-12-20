<Path>Add-ons > Calendar > Calendar with recurring events</Path>

The component will consider an event as recurring, if it has one of the following properties: recurringDaysOfWeek, recurringStartDate, recurringEndDate, recurringStartTime or recurringEndTime. Please note that, by default, an event in the data provider is expanded into single events in the calendar. If the user changes a recurring event, the change will be applied to the corresponding single event in the data provider. If a recurring event has a group ID property, all recurring events will be moved or resized together.

calendar-recurring-events.xml

<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<view xmlns="http://jmix.io/schema/flowui/view"
      xmlns:calendar="http://jmix.io/schema/fullcalendar/ui">
    <layout>
        <div classNames="border rounded-s p-s">
            <span text="msg://sampleDescription.text"/>
        </div>
        <calendar:calendar id="calendar"
                           eventStartEditable="true"
                           eventDurationEditable="true"
                           eventResizableFromStart="true"
                           height="100%"
                           width="100%"
                           minHeight="30em"/>
    </layout>
</view>



CalendarRecurringEventsSample.java

package io.jmix.uisamples.view.flowui.calendar.recurringevents;

import io.jmix.flowui.Notifications;
import io.jmix.flowui.view.*;
import io.jmix.fullcalendarflowui.component.FullCalendar;
import io.jmix.fullcalendarflowui.component.data.CalendarEvent;
import io.jmix.fullcalendarflowui.component.data.ListCalendarDataProvider;
import io.jmix.fullcalendarflowui.component.data.SimpleCalendarEvent;
import io.jmix.fullcalendarflowui.component.event.EventDropEvent;
import io.jmix.fullcalendarflowui.component.event.EventResizeEvent;
import io.jmix.fullcalendarflowui.component.model.DaysOfWeek;
import org.springframework.beans.factory.annotation.Autowired;

import java.time.LocalDate;
import java.time.LocalTime;
import java.util.List;
import java.util.Set;

import static io.jmix.fullcalendarflowui.component.model.DayOfWeek.MONDAY;
import static io.jmix.fullcalendarflowui.component.model.DayOfWeek.THURSDAY;

@ViewController("calendar-recurring-events")
@ViewDescriptor("calendar-recurring-events.xml")
public class CalendarRecurringEventsSample extends StandardView {

    @ViewComponent
    private FullCalendar calendar;

    @Autowired
    private Notifications notifications;

    @Subscribe
    public void onInit(final InitEvent event) {
        calendar.addDataProvider(new ListCalendarDataProvider(generateRecurringEvents()));
    }

    @Subscribe("calendar")
    public void onCalendarEventDrop(final EventDropEvent event) {
        CalendarEvent calendarEvent = event.getCalendarEvent();

        notifications.show("Event with \"%s\" ID is moved".formatted(calendarEvent.getId()));
    }

    @Subscribe("calendar")
    public void onCalendarEventResize(final EventResizeEvent event) {
        CalendarEvent calendarEvent = event.getCalendarEvent();

        notifications.show("Event with \"%s\" ID is resized".formatted(calendarEvent.getId()));
    }

    private List<CalendarEvent> generateRecurringEvents() {
        return List.of(
                SimpleCalendarEvent.create("morning")
                        .withTitle("Morning jog")
                        .withRecurringDaysOfWeek(new DaysOfWeek(Set.of(MONDAY)))
                        .withRecurringStartDate(LocalDate.now().withDayOfMonth(1))
                        .withRecurringEndDate(LocalDate.now().withDayOfMonth(26))
                        .withRecurringStartTime(LocalTime.of(8, 0))
                        .build(),
                SimpleCalendarEvent.create("cinema")
                        .withTitle("Cinema")
                        .withGroupId("cinema")
                        .withAllDay(true)
                        .withRecurringDaysOfWeek(new DaysOfWeek(Set.of(THURSDAY)))
                        .withRecurringStartDate(LocalDate.now().withDayOfMonth(1))
                        .withRecurringEndDate(LocalDate.now().withDayOfMonth(26))
                        .build()
        );
    }
}


