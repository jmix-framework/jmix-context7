<Path>Add-ons > Calendar > Calendar with CustomCalendarDisplayMode</Path>

The sample demonstrates how to configure a custom calendar display mode declaratively and programmatically.

calendar-custom-calendar-display-mode.xml

<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<view xmlns="http://jmix.io/schema/flowui/view"
      xmlns:calendar="http://jmix.io/schema/fullcalendar/ui">
    <layout>
        <comboBox id="displayModesBox"/>
        <calendar:calendar id="calendar"
                           initialDisplayMode="twoMonths"
                           height="100%"
                           width="100%"
                           minHeight="30em">
            <calendar:customDisplayModes>
                <calendar:displayMode id="twoMonths" type="MULTI_MONTH">
                    <calendar:duration months="2"/>
                </calendar:displayMode>
            </calendar:customDisplayModes>
        </calendar:calendar>
    </layout>
</view>



CalendarCustomCalendarDisplayModeSample.java

package io.jmix.uisamples.view.flowui.calendar.customcalendardisplaymode;

import io.jmix.core.Messages;
import io.jmix.flowui.component.combobox.JmixComboBox;
import io.jmix.flowui.view.*;
import io.jmix.fullcalendarflowui.component.FullCalendar;
import io.jmix.fullcalendarflowui.kit.component.model.CustomCalendarDisplayMode;
import org.springframework.beans.factory.annotation.Autowired;

import static io.jmix.fullcalendarflowui.kit.component.model.GenericCalendarDisplayModes.TIME_GRID;
import static io.jmix.uisamples.view.flowui.calendar.customcalendardisplaymode.CustomCalendarDisplayModes.THREE_DAYS;
import static io.jmix.uisamples.view.flowui.calendar.customcalendardisplaymode.CustomCalendarDisplayModes.TWO_MONTHS;

@ViewController("calendar-custom-calendar-display-mode")
@ViewDescriptor("calendar-custom-calendar-display-mode.xml")
public class CalendarCustomCalendarDisplayModeSample extends StandardView {

    @ViewComponent
    private FullCalendar calendar;
    @ViewComponent
    private JmixComboBox<CustomCalendarDisplayModes> displayModesBox;

    @Autowired
    private Messages messages;

    @Subscribe
    public void onInit(final InitEvent event) {
        displayModesBox.setItems(CustomCalendarDisplayModes.values());
        displayModesBox.setItemLabelGenerator(messages::getMessage);
        displayModesBox.setValue(TWO_MONTHS);
        displayModesBox.addValueChangeListener(e ->
                calendar.setCalendarDisplayMode(e.getValue() == null ? TWO_MONTHS : e.getValue()));

        calendar.addCustomCalendarDisplayMode(
                new CustomCalendarDisplayMode(THREE_DAYS.getId(), TIME_GRID)
                        .withDayCount(3));
    }
}




CustomCalendarDisplayModes.java

null

