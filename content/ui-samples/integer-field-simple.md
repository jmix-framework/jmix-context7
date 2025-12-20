<Path>Components > IntegerField > Simple IntegerField</Path>

IntegerField is a standard TextField with the Integer format.

integer-field-simple.xml

<view xmlns="http://jmix.io/schema/flowui/view">
    <layout>
        <integerField id="integerField" label="IntegerField"/>
        <integerField id="maxMinIntegerField" label="With max/min" max="100" min="10"
                      helperText="Max value is 100, min value is 10"/>
    </layout>
</view>




IntegerFieldSimpleSample.java

package io.jmix.uisamples.view.flowui.components.integerfield.simple;

import io.jmix.flowui.view.StandardView;
import io.jmix.flowui.view.ViewController;
import io.jmix.flowui.view.ViewDescriptor;

@ViewController("integer-field-simple")
@ViewDescriptor("integer-field-simple.xml")
public class IntegerFieldSimpleSample extends StandardView {
}


