<Path>Components > NumberField > Simple NumberField</Path>

NumberField is a standard TextField with the numeric input.

number-field-simple.xml

<view xmlns="http://jmix.io/schema/flowui/view">
    <layout>
        <numberField id="numberField" label="NumberField"/>
        <numberField id="maxMinNumberField" label="With max/min" max="100" min="10"
                      helperText="Max value is 100, min value is 10"/>
    </layout>
</view>




NumberFieldSimpleSample.java

package io.jmix.uisamples.view.flowui.components.numberfield.simple;

import io.jmix.flowui.view.StandardView;
import io.jmix.flowui.view.ViewController;
import io.jmix.flowui.view.ViewDescriptor;

@ViewController("number-field-simple")
@ViewDescriptor("number-field-simple.xml")
public class NumberFieldSimpleSample extends StandardView {
}


