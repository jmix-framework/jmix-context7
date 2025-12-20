<Path>Components > Switch > Simple Switch</Path>

The `switch` component is used to select boolean values.

`Switch` is an alternative to the [Checkbox](https://demo.jmix.io/ui-samples/sample/checkbox-simple) component.


switch-simple.xml

<view xmlns="http://jmix.io/schema/flowui/view">
    <layout>
        <switch id="carField" label="I have a car"/>
    </layout>
</view>




SwitchSimpleSample.java

package io.jmix.uisamples.view.flowui.components.switchcomponent.simple;

import com.vaadin.flow.component.AbstractField.ComponentValueChangeEvent;
import io.jmix.flowui.Notifications;
import io.jmix.flowui.component.checkbox.Switch;
import io.jmix.flowui.kit.component.checkbox.JmixSwitch;
import io.jmix.flowui.view.*;
import org.springframework.beans.factory.annotation.Autowired;

@ViewController("switch-simple")
@ViewDescriptor("switch-simple.xml")
public class SwitchSimpleSample extends StandardView {

    @ViewComponent
    private Switch carField;

    @Autowired
    private Notifications notifications;

    @Subscribe
    public void onInit(InitEvent event) {
        carField.setValue(true);
        carField.addValueChangeListener(this::carFieldValueChangeListener);
    }

    private void carFieldValueChangeListener(ComponentValueChangeEvent<JmixSwitch, Boolean> changeEvent) {
        notifications.show(Boolean.TRUE.equals(changeEvent.getValue())
                ? "I have a car"
                : "I don't have a car");
    }
}


