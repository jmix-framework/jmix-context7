<Path>Add-ons > Calendar > Calendar with GenericCalendarDisplayModes</Path>

The GenericCalendarDisplayModes provides modes that should be used together with setVisibleRange(). It enables displaying custom date range in day-grid, time-grid, list, or multi-month modes.

calendar-generic-calendar-display-modes.xml

<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<view xmlns="http://jmix.io/schema/flowui/view"
      xmlns:calendar="http://jmix.io/schema/fullcalendar/ui">
    <layout>
        <hbox>
            <comboBox id="genericDisplayModesBox" width="15em" overlayWidth="15em"/>
            <datePicker id="startDateField" datatype="localDate"/>
            <datePicker id="endDateField" datatype="localDate"/>
            <button id="setRangeBtn" text="msg://setRangeBtn.text"/>
        </hbox>
        <calendar:calendar id="calendar"
                           initialDisplayMode="DAY_GRID"
                           height="100%"
                           width="100%"
                           minHeight="30em"/>
    </layout>
</view>



CalendarGenericCalendarDisplayModesSample.java

package io.jmix.uisamples.view.flowui.calendar.genericcalendardisplaymodes;

import com.vaadin.flow.component.ClickEvent;
import io.jmix.core.Messages;
import io.jmix.flowui.component.combobox.JmixComboBox;
import io.jmix.flowui.component.datepicker.TypedDatePicker;
import io.jmix.flowui.kit.component.button.JmixButton;
import io.jmix.flowui.view.*;
import io.jmix.fullcalendarflowui.component.FullCalendar;
import io.jmix.fullcalendarflowui.kit.component.model.GenericCalendarDisplayModes;
import org.springframework.beans.factory.annotation.Autowired;

import java.time.LocalDate;

import static io.jmix.fullcalendarflowui.kit.component.model.GenericCalendarDisplayModes.DAY_GRID;

@ViewController("calendar-generic-calendar-display-modes")
@ViewDescriptor("calendar-generic-calendar-display-modes.xml")
public class CalendarGenericCalendarDisplayModesSample extends StandardView {

    @ViewComponent
    private FullCalendar calendar;
    @ViewComponent
    private JmixComboBox<GenericCalendarDisplayModes> genericDisplayModesBox;
    @ViewComponent
    private TypedDatePicker<LocalDate> endDateField;
    @ViewComponent
    private TypedDatePicker<LocalDate> startDateField;

    @Autowired
    private Messages messages;

    @Subscribe
    public void onInit(final InitEvent event) {
        genericDisplayModesBox.setItems(GenericCalendarDisplayModes.values());
        genericDisplayModesBox.setItemLabelGenerator(messages::getMessage);
        genericDisplayModesBox.setValue(DAY_GRID);
        genericDisplayModesBox.addValueChangeListener(e ->
                calendar.setCalendarDisplayMode(e.getValue() == null ? DAY_GRID : e.getValue()));

        startDateField.setValue(LocalDate.now().minusDays(1));
        endDateField.setValue(LocalDate.now().plusDays(1));
        calendar.setVisibleRange(startDateField.getValue(), endDateField.getValue());
    }

    @Subscribe(id = "setRangeBtn", subject = "clickListener")
    public void onSetRangeBtnClick(final ClickEvent<JmixButton> event) {
        if (startDateField.getValue() == null
                || endDateField.getValue() == null
                || startDateField.getValue().isAfter(endDateField.getValue())) {
            return;
        }

        calendar.setVisibleRange(startDateField.getValue(), endDateField.getValue());
    }
}


