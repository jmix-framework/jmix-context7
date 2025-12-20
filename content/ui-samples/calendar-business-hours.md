<Path>Add-ons > Calendar > Calendar with business hours</Path>

Business Hours refer to the specific times during which events are considered valid or can be scheduled.

calendar-business-hours.xml

<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<view xmlns="http://jmix.io/schema/flowui/view"
      xmlns:calendar="http://jmix.io/schema/fullcalendar/ui">
    <layout>
        <div classNames="border rounded-s p-s">
            <span text="msg://sampleDescription.text"/>
        </div>
        <tabSheet width="100%" height="100%">
            <tab id="declarativeTab" label="msg://declarativeCalendar.header">
                <calendar:calendar id="declarativeCalendar"
                                   initialDisplayMode="TIME_GRID_WEEK"
                                   eventConstraintBusinessHoursEnabled="true"
                                   eventStartEditable="true"
                                   eventDurationEditable="true"
                                   scrollTime="PT12h"
                                   eventResizableFromStart="true"
                                   height="100%"
                                   width="100%"
                                   minHeight="30em">
                    <calendar:businessHours>
                        <calendar:entry startTime="PT8h"
                                        endTime="PT18h">
                            <calendar:day name="MONDAY"/>
                            <calendar:day name="WEDNESDAY"/>
                            <calendar:day name="FRIDAY"/>
                        </calendar:entry>
                    </calendar:businessHours>

                </calendar:calendar>
            </tab>
            <tab id="programmaticTab" label="msg://programmaticCalendar.header">
                <calendar:calendar id="calendar"
                                   initialDisplayMode="TIME_GRID_WEEK"
                                   eventConstraintBusinessHoursEnabled="true"
                                   eventStartEditable="true"
                                   eventDurationEditable="true"
                                   eventResizableFromStart="true"
                                   scrollTime="PT12h"
                                   height="100%"
                                   width="100%"
                                   minHeight="30em"/>
            </tab>
        </tabSheet>
    </layout>
</view>



CalendarBusinessHoursSample.java

package io.jmix.uisamples.view.flowui.calendar.businesshours;

import io.jmix.flowui.view.*;
import io.jmix.fullcalendarflowui.component.FullCalendar;
import io.jmix.fullcalendarflowui.component.data.ListCalendarDataProvider;
import io.jmix.fullcalendarflowui.component.data.SimpleCalendarEvent;
import io.jmix.fullcalendarflowui.component.model.CalendarBusinessHours;
import io.jmix.fullcalendarflowui.component.model.DayOfWeek;

import java.time.LocalDate;
import java.time.LocalTime;
import java.util.List;

@ViewController("calendar-business-hours")
@ViewDescriptor("calendar-business-hours.xml")
public class CalendarBusinessHoursSample extends StandardView {

    @ViewComponent
    private FullCalendar declarativeCalendar;
    @ViewComponent
    private FullCalendar calendar;

    @Subscribe
    public void onInit(final InitEvent event) {
        declarativeCalendar.addDataProvider(
                new ListCalendarDataProvider(
                        List.of(SimpleCalendarEvent.create()
                                .withTitle("Event")
                                .withStartDateTime(LocalDate.now(), LocalTime.NOON)
                                .build())
                )
        );

        calendar.addDataProvider(
                new ListCalendarDataProvider(
                        List.of(SimpleCalendarEvent.create()
                                .withTitle("Event")
                                .withStartDateTime(LocalDate.now(), LocalTime.NOON)
                                .build())
                )
        );

        setBusinessHoursProgrammatically();
    }

    private void setBusinessHoursProgrammatically() {
        calendar.setBusinessHours(
                List.of(
                        CalendarBusinessHours.of(
                                LocalTime.of(10, 0),
                                LocalTime.of(19, 0),
                                DayOfWeek.TUESDAY),
                        CalendarBusinessHours.of(
                                LocalTime.of(11, 0),
                                LocalTime.of(20, 0),
                                DayOfWeek.THURSDAY)
                )
        );
    }
}


