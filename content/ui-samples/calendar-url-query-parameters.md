<Path>Add-ons > Calendar > Calendar with URL query parameters</Path>

The calendar add-on provides parameters for the UrlQueryParametersFacet. It contains the following parameters: The calendarDisplayMode - sets the display mode of the calendar. Can be changed to any name. The calendarDate - navigate to the specific date. Can be changed to any name.

calendar-url-query-parameters.xml

<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<view xmlns="http://jmix.io/schema/flowui/view"
      xmlns:calendar="http://jmix.io/schema/fullcalendar/ui">
    <facets>
        <urlQueryParameters>
            <calendar:calendarParameters component="calendar"/>
        </urlQueryParameters>
    </facets>
    <layout>
        <div classNames="border rounded-s p-s">
            <span text="msg://sampleDescription.text"/>
        </div>
        <hbox padding="false">
            <comboBox id="displayModesBox" width="15em" overlayWidth="15em"/>
            <button id="prevBtn" icon="ANGLE_LEFT"/>
            <button id="nextBtn" icon="ANGLE_RIGHT"/>
        </hbox>
        <calendar:calendar id="calendar"
                           height="100%"
                           width="100%"
                           minHeight="30em"/>
    </layout>
</view>



CalendarUrlQueryParameters.java

package io.jmix.uisamples.view.flowui.calendar.urlqueryparameters;

import com.vaadin.flow.component.ClickEvent;
import io.jmix.core.Messages;
import io.jmix.flowui.component.combobox.JmixComboBox;
import io.jmix.flowui.kit.component.button.JmixButton;
import io.jmix.flowui.view.*;
import io.jmix.fullcalendarflowui.component.FullCalendar;
import io.jmix.fullcalendarflowui.kit.component.model.CalendarDisplayModes;
import org.springframework.beans.factory.annotation.Autowired;

import static io.jmix.fullcalendarflowui.kit.component.model.CalendarDisplayModes.DAY_GRID_MONTH;

@ViewController("calendar-url-query-parameters")
@ViewDescriptor("calendar-url-query-parameters.xml")
public class CalendarUrlQueryParameters extends StandardView {

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

    @Subscribe(id = "prevBtn", subject = "clickListener")
    public void onPrevBtnClick(final ClickEvent<JmixButton> event) {
        calendar.navigateToPrevious();
    }

    @Subscribe(id = "nextBtn", subject = "clickListener")
    public void onNextBtnClick(final ClickEvent<JmixButton> event) {
        calendar.navigateToNext();
    }
}


