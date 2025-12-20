<Path>Add-ons > Calendar > Calendar display modes</Path>

FullCalendar has a lot of display modes out of the box: day-grid modes - display calendar in a grid format. Each cell in the day-grid represents a single day. time-grid modes - are time-oriented layouts for displaying events across one or more days. list modes - presents events in a straightforward vertical format. multi-month year mode - visualizes several months at once

calendar-calendar-display-modes.xml

<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<view xmlns="http://jmix.io/schema/flowui/view"
      xmlns:calendar="http://jmix.io/schema/fullcalendar/ui">
    <layout>
        <comboBox id="displayModesBox" width="15em" overlayWidth="15em"/>
        <calendar:calendar id="calendar"
                           height="100%"
                           width="100%"
                           minHeight="30em"/>
    </layout>
</view>



CalendarCalendarDisplayModesSample.java

package io.jmix.uisamples.view.flowui.calendar.calendardisplaymodes;

import io.jmix.core.Messages;
import io.jmix.flowui.component.combobox.JmixComboBox;
import io.jmix.flowui.view.*;
import io.jmix.fullcalendarflowui.component.FullCalendar;
import io.jmix.fullcalendarflowui.kit.component.model.CalendarDisplayModes;
import org.springframework.beans.factory.annotation.Autowired;

import static io.jmix.fullcalendarflowui.kit.component.model.CalendarDisplayModes.DAY_GRID_MONTH;

@ViewController("calendar-calendar-display-modes")
@ViewDescriptor("calendar-calendar-display-modes.xml")
public class CalendarCalendarDisplayModesSample extends StandardView {

    @ViewComponent
    private JmixComboBox<CalendarDisplayModes> displayModesBox;
    @ViewComponent
    private FullCalendar calendar;

    @Autowired
    private Messages messages;

    @Subscribe
    public void onInit(final InitEvent event) {
        displayModesBox.setItems(CalendarDisplayModes.values());
        displayModesBox.setItemLabelGenerator(messages::getMessage);
        displayModesBox.setValue(DAY_GRID_MONTH);

        displayModesBox.addValueChangeListener(e ->
                calendar.setCalendarDisplayMode(e.getValue() == null ? DAY_GRID_MONTH : e.getValue()));
    }
}


