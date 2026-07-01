<Path>Add-ons > Calendar > Calendar with select overlap function</Path>

The select overlap function determines the selection of cells with events. The function is invoked for every event in a cell, and if the function returns false the cell won't be selected. There is also the selectOverlap property. If it is disabled, selection won't occupy cells with events.

calendar-select-overlap-function.xml

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



CalendarSelectOverlapFunctionSample.java

package io.jmix.uisamples.view.flowui.calendar.selectoverlapfunction;

import io.jmix.flowui.view.*;
import io.jmix.fullcalendarflowui.component.FullCalendar;
import io.jmix.fullcalendarflowui.component.data.ListCalendarDataProvider;
import io.jmix.fullcalendarflowui.kit.component.model.JsFunction;

@ViewController("calendar-select-overlap-function")
@ViewDescriptor("calendar-select-overlap-function.xml")
public class CalendarSelectOverlapFunctionSample extends StandardView {

    @ViewComponent
    private FullCalendar calendar;

    @Subscribe
    public void onInit(final InitEvent event) {
        calendar.addDataProvider(new ListCalendarDataProvider(EventsHelper.generateEvents()));
        calendar.setSelectOverlapJsFunction(new JsFunction("""
                function(event) {
                   return event.groupId !== "holiday";
                }
                """));
    }
}


