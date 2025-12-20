<Path>Components > ValuePicker > Simple ValuePicker</Path>

valuePicker displays a value of any type. It consists of the text field and the set of buttons defined by actions.

value-picker-simple.xml

<view xmlns="http://jmix.io/schema/flowui/view">
    <layout classNames="flex-row flex-wrap">
        <valuePicker id="valuePicker1" label="Random string">
            <actions>
                <action id="generate" icon="REFRESH" description="Generate value"/>
                <action id="value_clear" type="value_clear"/>
            </actions>
        </valuePicker>
        <valuePicker id="valuePicker2" label="Random string" helperText="With custom value"
                     allowCustomValue="true">
            <actions>
                <action id="generate" icon="REFRESH" description="Generate value"/>
                <action id="value_clear" type="value_clear"/>
            </actions>
        </valuePicker>
    </layout>
</view>




ValuePickerSimpleSample.java

package io.jmix.uisamples.view.flowui.components.valuepicker.simple;

import io.jmix.flowui.component.valuepicker.JmixValuePicker;
import io.jmix.flowui.kit.action.ActionPerformedEvent;
import io.jmix.flowui.kit.component.valuepicker.CustomValueSetEvent;
import io.jmix.flowui.view.*;
import org.apache.commons.lang3.RandomStringUtils;

@ViewController("value-picker-simple")
@ViewDescriptor("value-picker-simple.xml")
public class ValuePickerSimpleSample extends StandardView {

    @ViewComponent
    protected JmixValuePicker<String> valuePicker1;
    @ViewComponent
    protected JmixValuePicker<String> valuePicker2;

    @Subscribe("valuePicker1.generate")
    protected void onValuePicker1GenerateActionPerformed(ActionPerformedEvent event) {
        generateValue(valuePicker1);
    }

    @Subscribe("valuePicker2.generate")
    protected void onValuePicker2GenerateActionPerformed(ActionPerformedEvent event) {
        generateValue(valuePicker2);
    }

    @Subscribe("valuePicker2")
    protected void onValuePicker2CustomValueChange(CustomValueSetEvent<JmixValuePicker<String>, String> event) {
        event.getSource().setValue(event.getText());
    }

    protected void generateValue(JmixValuePicker<String> valuePicker) {
        valuePicker.setValue(RandomStringUtils.secure().nextAlphabetic(5, 10));
    }
}


