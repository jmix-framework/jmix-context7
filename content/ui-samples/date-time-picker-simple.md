<Path>Components > DateTimePicker > Simple DateTimePicker</Path>

dateTimePicker lets users enter a date and time by typing or select it using a calendar overlay. Click the button to see the contained value

date-time-picker-simple.xml

<view xmlns="http://jmix.io/schema/flowui/view">
    <layout>
        <dateTimePicker id="dateTimePicker" label="DateTimePicker" datatype="localDateTime"/>
        <button id="button" text="Show value" icon="CALENDAR_CLOCK"/>
    </layout>
</view>




DateTimePickerSimpleSample.java

package io.jmix.uisamples.view.flowui.components.datetimepicker.simple;

import com.vaadin.flow.component.ClickEvent;
import io.jmix.flowui.Notifications;
import io.jmix.flowui.component.datetimepicker.TypedDateTimePicker;
import io.jmix.flowui.kit.component.button.JmixButton;
import io.jmix.flowui.view.*;
import org.springframework.beans.factory.annotation.Autowired;

import java.time.LocalDate;

@ViewController("date-time-picker-simple")
@ViewDescriptor("date-time-picker-simple.xml")
public class DateTimePickerSimpleSample extends StandardView {

    @ViewComponent
    protected TypedDateTimePicker<LocalDate> dateTimePicker;

    @Autowired
    protected Notifications notifications;

    @Subscribe("button")
    protected void onButtonClick(ClickEvent<JmixButton> event) {
        notifications.show(String.valueOf(dateTimePicker.getTypedValue()));
    }
}


