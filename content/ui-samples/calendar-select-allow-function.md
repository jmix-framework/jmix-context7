<Path>Add-ons > Calendar > Calendar with select allow function</Path>

The selection allow function determines the selection of cells in general. This function takes a parameter that contains information about the selection: start - start date with the component's time zone. startStr - start date in string format. end - end date with the component's time zone. endStr - end date in string format. allDay - determines if a cell is a day cell.

calendar-select-allow-function.xml

<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<view xmlns="http://jmix.io/schema/flowui/view"
      xmlns:calendar="http://jmix.io/schema/fullcalendar/ui">
    <layout>
        <div classNames="rounded-panel">
            <span text="msg://sampleDescription.text"/>
        </div>
        <calendar:calendar id="calendar"
                           selectionEnabled="true"
                           height="100%"
                           width="100%"
                           minHeight="30em"/>
    </layout>
</view>



CalendarSelectAllowFunctionSample.java

package io.jmix.uisamples.view.flowui.calendar.selectallowfunction;

import io.jmix.flowui.view.*;
import io.jmix.fullcalendarflowui.component.FullCalendar;
import io.jmix.fullcalendarflowui.kit.component.model.JsFunction;

import java.time.LocalDate;
import java.util.TimeZone;

@ViewController("calendar-select-allow-function")
@ViewDescriptor("calendar-select-allow-function.xml")
public class CalendarSelectAllowFunctionSample extends StandardView {

    @ViewComponent
    private FullCalendar calendar;

    @Subscribe
    public void onInit(final InitEvent event) {
        calendar.setSelectAllowJsFunction(new JsFunction(
                String.format("""
                        function(selectionInfo) {
                        console.log('TAAG');
                           const currentDate = new Date('%s');
                           return currentDate < selectionInfo.start
                                  || currentDate >= selectionInfo.end;
                        }
                        """, convertToStrDate(LocalDate.now()))
        ));
    }

    private String convertToStrDate(LocalDate date) {
        TimeZone timeZone = calendar.getTimeZone() == null
                ? TimeZone.getDefault()
                : calendar.getTimeZone();
        return date.atStartOfDay(timeZone.toZoneId()).toOffsetDateTime().toString();
    }
}


