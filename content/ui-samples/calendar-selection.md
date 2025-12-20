<Path>Add-ons > Calendar > Calendar with selection</Path>

The selectionEnabled property allows for selection within the component. You can select a date or date-time range using the mouse or programmatically. To handle when a user selects or unselects date range, you can subscribe to the SelectEvent and UnselectEvent

calendar-selection.xml

<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<view xmlns="http://jmix.io/schema/flowui/view"
      xmlns:calendar="http://jmix.io/schema/fullcalendar/ui">
    <layout>
        <hbox width="100%" height="100%" padding="false">
            <calendar:calendar id="calendar"
                               selectionEnabled="true"
                               height="100%"
                               width="100%"
                               minHeight="30em"
                               minWidth="30em"/>
            <vbox id="actionsBox" height="100%" width="30em" padding="false">
                <comboBox id="displayModesBox" width="15em" overlayWidth="15em"/>
                <h5 text="msg://dateSelectionHeader.text"/>
                <hbox width="100%" padding="false">
                    <datePicker id="startDateField" datatype="localDate"/>
                    <datePicker id="endDateField" datatype="localDate"/>
                </hbox>
                <button id="selectDateBtn" text="msg://selectDateBtn.text"/>
                <h5 text="msg://dateTimeSelectionHeader.text"/>
                <vbox width="100%" padding="false">
                    <dateTimePicker id="startDateTimeField" datatype="localDateTime"/>
                    <dateTimePicker id="endDateTimeField" datatype="localDateTime"/>
                </vbox>
                <button id="selectDateTimeBtn" text="msg://selectDateTimeBtn.text"/>
            </vbox>
        </hbox>
    </layout>
</view>



CalendarSelectionSample.java

package io.jmix.uisamples.view.flowui.calendar.selection;

import com.vaadin.flow.component.ClickEvent;
import com.vaadin.flow.component.notification.Notification;
import io.jmix.core.Messages;
import io.jmix.flowui.Notifications;
import io.jmix.flowui.component.combobox.JmixComboBox;
import io.jmix.flowui.component.datepicker.TypedDatePicker;
import io.jmix.flowui.component.datetimepicker.TypedDateTimePicker;
import io.jmix.flowui.kit.component.button.JmixButton;
import io.jmix.flowui.view.*;
import io.jmix.fullcalendarflowui.component.FullCalendar;
import io.jmix.fullcalendarflowui.component.event.SelectEvent;
import io.jmix.fullcalendarflowui.component.event.UnselectEvent;
import io.jmix.fullcalendarflowui.kit.component.model.CalendarDisplayModes;
import org.springframework.beans.factory.annotation.Autowired;

import java.time.LocalDate;
import java.time.LocalDateTime;

import static io.jmix.fullcalendarflowui.kit.component.model.CalendarDisplayModes.DAY_GRID_MONTH;
import static io.jmix.fullcalendarflowui.kit.component.model.CalendarDisplayModes.TIME_GRID_WEEK;

@ViewController("calendar-selection")
@ViewDescriptor("calendar-selection.xml")
public class CalendarSelectionSample extends StandardView {

    @ViewComponent
    private JmixComboBox<CalendarDisplayModes> displayModesBox;
    @ViewComponent
    private FullCalendar calendar;
    @ViewComponent
    private TypedDatePicker<LocalDate> startDateField;
    @ViewComponent
    private TypedDatePicker<LocalDate> endDateField;
    @ViewComponent
    private TypedDateTimePicker<LocalDateTime> startDateTimeField;
    @ViewComponent
    private TypedDateTimePicker<LocalDateTime> endDateTimeField;

    @Autowired
    private Messages messages;
    @Autowired
    private Notifications notifications;

    @Subscribe
    public void onInit(final InitEvent event) {
        displayModesBox.setItems(DAY_GRID_MONTH, TIME_GRID_WEEK);
        displayModesBox.setItemLabelGenerator(messages::getMessage);
        displayModesBox.setValue(DAY_GRID_MONTH);
        displayModesBox.addValueChangeListener(e ->
                calendar.setCalendarDisplayMode(e.getValue() == null ? DAY_GRID_MONTH : e.getValue()));
    }

    @Subscribe(id = "calendar")
    public void onCalendarSelectEvent(SelectEvent event) {
        notifications.create("SelectEvent",
                        String.format("From %s to %s", event.getStartDateTime(), event.getEndDateTime()))
                .withPosition(Notification.Position.BOTTOM_END)
                .show();
    }

    @Subscribe(id = "calendar")
    public void onCalendarUnselectEvent(UnselectEvent event) {
        notifications.create("UnselectEvent")
                .withPosition(Notification.Position.BOTTOM_END)
                .show();
    }

    @Subscribe(id = "selectDateBtn", subject = "clickListener")
    public void onSelectDateBtnClick(final ClickEvent<JmixButton> event) {
        LocalDate start = startDateField.getValue();
        LocalDate end = endDateField.getValue();
        if (start == null || end == null) {
            return;
        }

        calendar.select(start, end);
    }

    @Subscribe(id = "selectDateTimeBtn", subject = "clickListener")
    public void onSelectDateTimeBtnClick(final ClickEvent<JmixButton> event) {
        LocalDateTime start = startDateTimeField.getValue();
        LocalDateTime end = endDateTimeField.getValue();
        if (start == null || end == null) {
            return;
        }

        calendar.select(start, end);
    }
}


