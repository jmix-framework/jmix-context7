<Path>Add-ons > Calendar > Calendar with actions</Path>

The FullCalendar component generates a set of events. There are two events that are generated without specific conditions: DateClickEvent and DatesSetEvent. DateClickEvent - the event is fired when a day cell or time cell is clicked. DatesSetEvent - the event is fired after the calendar date range has been initially set or changed in some way, and the DOM of the component has been updated. The calendar dates can change any time the user does the following: Navigates to next and previous. Switches the display mode. Clicks a navigation link (e.g. week or day).

calendar-actions.xml

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



CalendarActionsSample.java

package io.jmix.uisamples.view.flowui.calendar.actions;

import io.jmix.core.Messages;
import io.jmix.flowui.Notifications;
import io.jmix.flowui.component.combobox.JmixComboBox;
import io.jmix.flowui.view.*;
import io.jmix.fullcalendarflowui.component.FullCalendar;
import io.jmix.fullcalendarflowui.component.event.DateClickEvent;
import io.jmix.fullcalendarflowui.component.event.DatesSetEvent;
import io.jmix.fullcalendarflowui.kit.component.model.CalendarDisplayModes;
import org.springframework.beans.factory.annotation.Autowired;

import static io.jmix.fullcalendarflowui.kit.component.model.CalendarDisplayModes.DAY_GRID_MONTH;

@ViewController("calendar-actions")
@ViewDescriptor("calendar-actions.xml")
public class CalendarActionsSample extends StandardView {

    @ViewComponent
    private JmixComboBox<CalendarDisplayModes> displayModesBox;
    @ViewComponent
    private FullCalendar calendar;

    @Autowired
    private Messages messages;
    @Autowired
    private Notifications notifications;

    @Subscribe
    public void onInit(final InitEvent event) {
        displayModesBox.setItems(CalendarDisplayModes.values());
        displayModesBox.setItemLabelGenerator(messages::getMessage);
        displayModesBox.setValue(DAY_GRID_MONTH);

        displayModesBox.addValueChangeListener(e ->
                calendar.setCalendarDisplayMode(e.getValue() == null ? DAY_GRID_MONTH : e.getValue()));
    }

    @Subscribe("calendar")
    public void onCalendarDatesSet(final DatesSetEvent event) {
        notifications.show("DatesSetEvent",
                "Display mode: " + event.getDisplayModeInfo().getDisplayMode().getId());
    }

    @Subscribe("calendar")
    public void onCalendarDateClick(final DateClickEvent event) {
        notifications.show("DateClickEvent", "Date: " + event.getDateTime());
    }
}


