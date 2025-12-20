<Path>Components > DateTimePicker > DateTimePicker with custom range</Path>

You can specify available dates and time to select by using max and min attributes. If you set them, all the dates and time that are outside the range will be disabled.

date-time-picker-custom-range.xml

<view xmlns="http://jmix.io/schema/flowui/view">
    <layout>
        <dateTimePicker id="dateTimePicker" label="DateTimePicker" datatype="localDateTime"/>
    </layout>
</view>




DateTimePickerCustomRange.java

package io.jmix.uisamples.view.flowui.components.datetimepicker.customrange;

import io.jmix.flowui.component.datetimepicker.TypedDateTimePicker;
import io.jmix.flowui.view.*;

import java.time.LocalDateTime;

@ViewController("date-time-picker-custom-range")
@ViewDescriptor("date-time-picker-custom-range.xml")
public class DateTimePickerCustomRange extends StandardView {

    @ViewComponent
    protected TypedDateTimePicker<LocalDateTime> dateTimePicker;

    @Subscribe
    protected void onInit(InitEvent event) {
        dateTimePicker.setMin(LocalDateTime.now().minusWeeks(1));
        dateTimePicker.setMax(LocalDateTime.now().plusWeeks(1));
    }
}


