<Path>Components > DatePicker > DatePicker with custom range</Path>

You can specify available dates to select by using max and min attributes. If you set them, all the dates that are outside the range will be disabled.

date-picker-custom-range.xml

<view xmlns="http://jmix.io/schema/flowui/view">
    <layout>
        <datePicker id="datePicker" label="DatePicker" datatype="localDate"/>
    </layout>
</view>




DatePickerCustomRange.java

package io.jmix.uisamples.view.flowui.components.datepicker.customrange;

import io.jmix.flowui.component.datepicker.TypedDatePicker;
import io.jmix.flowui.view.*;

import java.time.LocalDate;

@ViewController("date-picker-custom-range")
@ViewDescriptor("date-picker-custom-range.xml")
public class DatePickerCustomRange extends StandardView {

    @ViewComponent
    protected TypedDatePicker<LocalDate> datePicker;

    @Subscribe
    protected void onInit(InitEvent event) {
        datePicker.setMin(LocalDate.now().minusWeeks(1));
        datePicker.setMax(LocalDate.now().plusWeeks(1));
    }
}


