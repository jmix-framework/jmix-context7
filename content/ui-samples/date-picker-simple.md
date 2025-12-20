<Path>Components > DatePicker > Simple DatePicker</Path>

datePicker lets users enter a date by typing or select it using a calendar overlay. Click the button to see the contained value

date-picker-simple.xml

<view xmlns="http://jmix.io/schema/flowui/view">
    <layout>
        <datePicker id="datePicker" label="DatePicker" datatype="localDate"/>
        <button id="button" text="Show value" icon="CALENDAR"/>
    </layout>
</view>




DatePickerSimpleSample.java

package io.jmix.uisamples.view.flowui.components.datepicker.simple;

import com.vaadin.flow.component.ClickEvent;
import io.jmix.flowui.Notifications;
import io.jmix.flowui.component.datepicker.TypedDatePicker;
import io.jmix.flowui.kit.component.button.JmixButton;
import io.jmix.flowui.view.*;
import org.springframework.beans.factory.annotation.Autowired;

import java.time.LocalDate;

@ViewController("date-picker-simple")
@ViewDescriptor("date-picker-simple.xml")
public class DatePickerSimpleSample extends StandardView {

    @ViewComponent
    protected TypedDatePicker<LocalDate> datePicker;

    @Autowired
    protected Notifications notifications;

    @Subscribe("button")
    protected void onButtonClick(ClickEvent<JmixButton> event) {
        notifications.show(String.valueOf(datePicker.getTypedValue()));
    }
}


