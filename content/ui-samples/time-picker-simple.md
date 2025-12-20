<Path>Components > TimePicker > Simple TimePicker</Path>

timePicker lets users enter a time by typing or select it using a dropdown list. Click the button to see the contained value

time-picker-simple.xml

<view xmlns="http://jmix.io/schema/flowui/view">
    <layout>
        <timePicker id="timePicker" label="TimePicker" datatype="localTime"/>
        <button id="button" text="Show value" icon="CLOCK"/>
    </layout>
</view>




TimePickerSimpleSample.java

package io.jmix.uisamples.view.flowui.components.timepicker.simple;

import com.vaadin.flow.component.ClickEvent;
import io.jmix.flowui.Notifications;
import io.jmix.flowui.component.timepicker.TypedTimePicker;
import io.jmix.flowui.kit.component.button.JmixButton;
import io.jmix.flowui.view.*;
import org.springframework.beans.factory.annotation.Autowired;

import java.time.LocalTime;

@ViewController("time-picker-simple")
@ViewDescriptor("time-picker-simple.xml")
public class TimePickerSimpleSample extends StandardView {

    @ViewComponent
    protected TypedTimePicker<LocalTime> timePicker;

    @Autowired
    protected Notifications notifications;

    @Subscribe("button")
    protected void onButtonClick(ClickEvent<JmixButton> event) {
        notifications.show(String.valueOf(timePicker.getTypedValue()));
    }
}


