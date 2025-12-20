<Path>Components > ValuePicker > MultiValuePicker</Path>

The MultiValuePicker component works with a list of values of any type. It consists of the text field and the set of buttons defined by actions. MultiValuePicker is convenient to use if you need to edit the list of values through actions, not in the text field. You can define custom and predefined actions for MultiValuePicker displayed as buttons on the right. The framework provides value_clear and multi_value_select predefined actions. The multi_value_select action sets a value to MultiValuePicker using a value selection dialog. The value selection dialog generates a specific component to select or create a value depending on the passed value type.

value-picker-multi.xml

<view xmlns="http://jmix.io/schema/flowui/view">
    <layout classNames="flex-row flex-wrap">
        <multiValuePicker id="stringsValuePicker" label="Strings">
            <actions>
                <action id="select" type="multi_value_select">
                    <properties>
                        <property name="javaClass" value="java.lang.String"/>
                    </properties>
                </action>
                <action id="value_clear" type="value_clear"/>
            </actions>
        </multiValuePicker>
        <multiValuePicker id="integersValuePicker" label="Integers">
            <actions>
                <action id="select" type="multi_value_select">
                    <properties>
                        <property name="javaClass" value="java.lang.Integer"/>
                    </properties>
                </action>
                <action id="value_clear" type="value_clear"/>
            </actions>
        </multiValuePicker>
    </layout>
</view>




ValuePickerMultiSample.java

package io.jmix.uisamples.view.flowui.components.valuepicker.multi;

import io.jmix.flowui.view.StandardView;
import io.jmix.flowui.view.ViewController;
import io.jmix.flowui.view.ViewDescriptor;

@ViewController("value-picker-multi")
@ViewDescriptor("value-picker-multi.xml")
public class ValuePickerMultiSample extends StandardView {
}


