<Path>Add-ons > Calendar > Calendar with class names generator</Path>

The class name generator allows you to configure CSS class names depending on the cell.

calendar-class-names-generator.xml

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



CalendarClassNamesGeneratorSample.java

package io.jmix.uisamples.view.flowui.calendar.classnamesgenerator;

import io.jmix.flowui.view.Install;
import io.jmix.flowui.view.StandardView;
import io.jmix.flowui.view.ViewController;
import io.jmix.flowui.view.ViewDescriptor;
import io.jmix.fullcalendarflowui.component.event.DayCellClassNamesContext;
import io.jmix.fullcalendarflowui.component.event.DayHeaderClassNamesContext;
import io.jmix.fullcalendarflowui.component.model.DayOfWeek;

import java.time.LocalDate;
import java.util.ArrayList;
import java.util.List;

@ViewController("calendar-class-names-generator")
@ViewDescriptor("calendar-class-names-generator.xml")
public class CalendarClassNamesGeneratorSample extends StandardView {

    private static final String TODAY_CLASS_NAME = "uisamples-today";
    private static final String WEEKEND_CLASS_NAME = "uisamples-weekend";
    private static final String DAY_HEADER_CLASS_NAME = "uisamples-day-header";

    @Install(to = "calendar", subject = "dayCellClassNamesGenerator")
    private List<String> calendarDayCellClassNamesGenerator(final DayCellClassNamesContext context) {
        List<String> classes = new ArrayList<>(2);

        DayOfWeek dow = context.getDayOfWeek();
        if (dow == DayOfWeek.SATURDAY || dow == DayOfWeek.SUNDAY) {
            classes.add(WEEKEND_CLASS_NAME);
        }
        if (context.getDate().isEqual(LocalDate.now())) {
            classes.add(TODAY_CLASS_NAME);
        }
        return classes;
    }

    @Install(to = "calendar", subject = "dayHeaderClassNamesGenerator")
    private List<String> calendarDayHeaderClassNamesGenerator(final DayHeaderClassNamesContext context) {
        List<String> classes = new ArrayList<>(2);
        classes.add(DAY_HEADER_CLASS_NAME);

        DayOfWeek dow = context.getDayOfWeek();
        if (dow == DayOfWeek.SATURDAY || dow == DayOfWeek.SUNDAY) {
            classes.add(WEEKEND_CLASS_NAME);
        }
        if (dow == DayOfWeek.fromDayOfWeek(LocalDate.now().getDayOfWeek())) {
            classes.add(TODAY_CLASS_NAME);
        }
        return classes;
    }
}




calendar-class-names-generator.css

/*
 * Base color for day headers.
 */
.uisamples-day-header {
    background-color: color-mix(in srgb, var(--aura-accent-color) 10%, transparent);
}

jmix-full-calendar .uisamples-day-header a {
    color: var(--aura-accent-text-color);
}

.uisamples-day-header.uisamples-today {
    background-color: var(--aura-accent-color);
}

jmix-full-calendar .uisamples-day-header.uisamples-today a {
    color: var(--aura-accent-contrast-color);
}

jmix-full-calendar .fc-day.fc-daygrid-day.uisamples-today {
    background-color: inherit;
}

jmix-full-calendar .uisamples-today .fc-daygrid-day-number {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    box-sizing: border-box;
    color: var(--aura-accent-text-color);
    background-color: color-mix(in srgb, var(--aura-accent-color) 10%, transparent);
    border-radius: var(--vaadin-radius-l);
    line-height: 1;
    font-weight: 500;
    min-width: calc(var(--aura-base-line-height) * 1em + 0.45em);
    flex-shrink: 0;
    margin-top: var(--vaadin-padding-xs);
    margin-inline-end: var(--vaadin-padding-xs);
}

/*
 * Weekend header day colors.
 */
.uisamples-day-header.uisamples-weekend {
    background-color: color-mix(in srgb, var(--aura-red) 10%, transparent);
}

jmix-full-calendar .uisamples-day-header.uisamples-weekend a {
    color: var(--aura-red-text);
}

.uisamples-day-header.uisamples-weekend.uisamples-today {
    background-color: var(--aura-red);
}

jmix-full-calendar .uisamples-day-header.uisamples-weekend.uisamples-today a {
    color: var(--aura-accent-contrast-color);
}

jmix-full-calendar .uisamples-weekend.uisamples-today .fc-daygrid-day-number {
    background-color: color-mix(in srgb, var(--aura-red) 10%, transparent);
    color: var(--aura-red-text);
}


