<Path>Components > Slider > Simple Slider</Path>

`Slider` lets the user pick a numeric value by dragging a handle along a track. Jmix provides two flavors: `integerSlider` for `Integer` values and `decimalSlider` for `Double` values.

Set the bounds with `min` and `max`, and the increment with `step`. `minMaxVisible` prints the bounds below the track, and `valueAlwaysVisible` keeps the value bubble on view instead of showing it only while the handle is being dragged.


slider-simple.xml

<view xmlns="http://jmix.io/schema/flowui/view">
    <layout>
        <integerSlider id="integerSlider" label="IntegerSlider" width="20em" value="50"/>
        <integerSlider id="stepSlider" label="With min, max and step" width="20em"
                       min="0" max="50" step="5" value="20"
                       minMaxVisible="true"
                       helperText="Values from 0 to 50 with a step of 5"/>
        <decimalSlider id="decimalSlider" label="DecimalSlider" width="20em"
                       min="0" max="1" step="0.1" value="0.5"
                       valueAlwaysVisible="true"
                       helperText="The value bubble is always visible"/>
    </layout>
</view>




SliderSimpleSample.java

package io.jmix.uisamples.view.flowui.components.slider.simple;

import io.jmix.flowui.view.StandardView;
import io.jmix.flowui.view.ViewController;
import io.jmix.flowui.view.ViewDescriptor;

@ViewController("slider-simple")
@ViewDescriptor("slider-simple.xml")
public class SliderSimpleSample extends StandardView {
}


