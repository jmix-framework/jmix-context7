<Path>Add-ons > Calendar > Calendar with display modes specific properties</Path>

Every display mode has specific properties that can be configured within the displayModeProperties element. Also, the FullCalendar component allows you to define properties that are not declared in XML elements. These properties override existing configuration from the calendar for a specific display mode. For instance, in this sample, the day-grid month display mode sets visible week numbers. Please note that the property name in the property tag should be defined as specified in the FullCalendar.js documentation.

calendar-display-mode-specific-properties.xml

<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<view xmlns="http://jmix.io/schema/flowui/view"
      xmlns:calendar="http://jmix.io/schema/fullcalendar/ui">
    <layout>
        <comboBox id="displayModesBox" width="15em" overlayWidth="15em"/>
        <calendar:calendar id="calendar"
                           height="100%"
                           width="100%"
                           minHeight="30em">
            <calendar:displayModeProperties>
                <calendar:dayGridMonth showNonCurrentDates="false">
                    <calendar:properties>
                        <calendar:property name="weekNumbers" value="true"/>
                    </calendar:properties>
                </calendar:dayGridMonth>
                <calendar:timeGridWeek allDaySlotVisible="false"/>
            </calendar:displayModeProperties>
        </calendar:calendar>
    </layout>
</view>



CalendarDisplayModeSpecificPropertiesSample.java

package io.jmix.uisamples.view.flowui.calendar.displaymodespecifiproperties;

import io.jmix.core.Messages;
import io.jmix.flowui.component.combobox.JmixComboBox;
import io.jmix.flowui.view.*;
import io.jmix.fullcalendarflowui.component.FullCalendar;
import io.jmix.fullcalendarflowui.kit.component.model.CalendarDisplayModes;
import org.springframework.beans.factory.annotation.Autowired;

import static io.jmix.fullcalendarflowui.kit.component.model.CalendarDisplayModes.DAY_GRID_MONTH;
import static io.jmix.fullcalendarflowui.kit.component.model.CalendarDisplayModes.TIME_GRID_WEEK;

@ViewController("calendar-display-mode-specific-properties")
@ViewDescriptor("calendar-display-mode-specific-properties.xml")
public class CalendarDisplayModeSpecificPropertiesSample extends StandardView {

    @ViewComponent
    private FullCalendar calendar;
    @ViewComponent
    private JmixComboBox<CalendarDisplayModes> displayModesBox;

    @Autowired
    private Messages messages;

    @Subscribe
    public void onInit(final InitEvent event) {
        displayModesBox.setItems(DAY_GRID_MONTH, TIME_GRID_WEEK);
        displayModesBox.setItemLabelGenerator(messages::getMessage);
        displayModesBox.setValue(DAY_GRID_MONTH);
        displayModesBox.addValueChangeListener(e ->
                calendar.setCalendarDisplayMode(e.getValue() == null ? DAY_GRID_MONTH : e.getValue()));
    }
}


