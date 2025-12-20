<Path>Add-ons > Calendar > Event creation using selection in Calendar</Path>

This sample demonstrates calendar event creation using selection. selectMirror enables the component to display an event instead of a simple selection.

calendar-select-mirror.xml

<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<view xmlns="http://jmix.io/schema/flowui/view"
      xmlns:calendar="http://jmix.io/schema/fullcalendar/ui">
    <layout>
        <div classNames="border rounded-s p-s">
            <span text="msg://sampleDescription.text"/>
        </div>
        <calendar:calendar id="calendar"
                           initialDisplayMode="TIME_GRID_WEEK"
                           selectionEnabled="true"
                           selectMirror="true"
                           unselectAuto="false"
                           height="100%"
                           width="100%"
                           minHeight="30em"/>
    </layout>
</view>



CalendarSelectMirrorSample.java

package io.jmix.uisamples.view.flowui.calendar.selectmirror;

import io.jmix.flowui.Dialogs;
import io.jmix.flowui.action.DialogAction;
import io.jmix.flowui.app.inputdialog.DialogActions;
import io.jmix.flowui.view.*;
import io.jmix.fullcalendarflowui.component.FullCalendar;
import io.jmix.fullcalendarflowui.component.data.ListCalendarDataProvider;
import io.jmix.fullcalendarflowui.component.data.SimpleCalendarEvent;
import io.jmix.fullcalendarflowui.component.event.SelectEvent;
import org.springframework.beans.factory.annotation.Autowired;

import java.util.Objects;

import static io.jmix.flowui.app.inputdialog.InputParameter.*;

@ViewController("calendar-select-mirror")
@ViewDescriptor("calendar-select-mirror.xml")
public class CalendarSelectMirrorSample extends StandardView {

    @ViewComponent
    private FullCalendar calendar;
    @ViewComponent
    private MessageBundle messageBundle;

    @Autowired
    private Dialogs dialogs;

    @Subscribe
    public void onInit(final InitEvent event) {
        calendar.addDataProvider(new ListCalendarDataProvider("dataProvider"));
    }

    @Subscribe(id = "calendar")
    public void onCalendarSelectEvent(SelectEvent event) {
        showCreatingDialog(event);
    }

    private void showCreatingDialog(SelectEvent event) {
        dialogs.createInputDialog(this)
                .withHeader(messageBundle.getMessage("dialog.header"))
                .withParameters(
                        stringParameter("title")
                                .withLabel(messageBundle.getMessage("dialog.title.label"))
                                .withRequired(true),
                        booleanParameter("allDay")
                                .withLabel(messageBundle.getMessage("dialog.allDay.label"))
                                .withDefaultValue(event.isAllDay()),
                        localDateTimeParameter("startDate")
                                .withLabel(messageBundle.getMessage("dialog.startDate.label"))
                                .withDefaultValue(event.getStartDateTime())
                                .withRequired(true),
                        localDateTimeParameter("endDate")
                                .withLabel(messageBundle.getMessage("dialog.endDate.label"))
                                .withDefaultValue(event.getEndDateTime()))
                .withActions(DialogActions.OK_CANCEL, result -> {
                    if (result.getCloseActionType() == DialogAction.Type.OK) {
                        ListCalendarDataProvider dataProvider = calendar.getDataProvider("dataProvider");
                        Objects.requireNonNull(dataProvider)
                                .addItem(SimpleCalendarEvent.create()
                                        .withTitle(result.getValue("title"))
                                        .withAllDay(result.getValue("allDay"))
                                        .withStartDateTime(result.getValue("startDate"))
                                        .withEndDateTime(result.getValue("endDate"))
                                        .build());
                    }

                    calendar.unselect();
                })
                .open();
    }
}


