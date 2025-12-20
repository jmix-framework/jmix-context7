<Path>Components > TimePicker > TimePicker with custom range</Path>

You can specify available time to select by using max and min attributes. If you set them, all the time that are outside the range will be disabled. The default interval between the items displayed in the overlay is set to one hour. It is possible to set a custom step value.

time-picker-custom-range.xml

<view xmlns="http://jmix.io/schema/flowui/view">
    <layout>
        <timePicker id="timePicker" label="TimePicker" datatype="localTime"
                    step="15m"/>
    </layout>
</view>




TimePickerCustomRange.java

package io.jmix.uisamples.view.flowui.components.timepicker.customrange;

import io.jmix.flowui.component.timepicker.TypedTimePicker;
import io.jmix.flowui.view.*;

import java.time.LocalTime;

@ViewController("time-picker-custom-range")
@ViewDescriptor("time-picker-custom-range.xml")
public class TimePickerCustomRange extends StandardView {

    @ViewComponent
    protected TypedTimePicker<LocalTime> timePicker;

    @Subscribe
    protected void onInit(InitEvent event) {
        timePicker.setMin(LocalTime.of(8, 0));
        timePicker.setMax(LocalTime.of(17, 0));
    }
}


