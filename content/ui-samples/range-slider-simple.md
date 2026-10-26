<Path>Components > RangeSlider > Simple RangeSlider</Path>

`RangeSlider` lets the user pick a range of values with two handles: `integerRangeSlider` for `Integer` bounds and `decimalRangeSlider` for `Double` ones. The initial range is set with `startValue` and `endValue`, the track with `min`, `max` and `step`.

Its value is a record – `IntegerRangeSliderValue` or `DecimalRangeSliderValue` – with `start()` and `end()` accessors. Unlike a plain slider, a range slider cannot be bound to a data container.


range-slider-simple.xml

<view xmlns="http://jmix.io/schema/flowui/view">
    <layout>
        <integerRangeSlider id="integerRangeSlider" label="IntegerRangeSlider" width="20em"
                            startValue="20" endValue="80"
                            accessibleNameStart="Minimum" accessibleNameEnd="Maximum"/>
        <integerRangeSlider id="stepRangeSlider" label="With min, max and step" width="20em"
                            min="0" max="50" step="5"
                            startValue="10" endValue="35"
                            minMaxVisible="true"
                            helperText="Values from 0 to 50 with a step of 5"/>
        <decimalRangeSlider id="decimalRangeSlider" label="DecimalRangeSlider" width="20em"
                            min="0" max="1" step="0.1"
                            startValue="0.2" endValue="0.8"
                            valueAlwaysVisible="true"
                            helperText="The value bubbles are always visible"/>
    </layout>
</view>




RangeSliderSimpleSample.java

package io.jmix.uisamples.view.flowui.components.rangeslider.simple;

import io.jmix.flowui.view.StandardView;
import io.jmix.flowui.view.ViewController;
import io.jmix.flowui.view.ViewDescriptor;

@ViewController("range-slider-simple")
@ViewDescriptor("range-slider-simple.xml")
public class RangeSliderSimpleSample extends StandardView {
}


