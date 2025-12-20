<Path>Components > TextField > TextField with ValueChange listener</Path>

The ValueChangeEvent defines the way the changes are transmitted to the server to cause a server-side event. There are 4 predefined event modes: EAGER - an event is triggered immediately for every change in the text content, typically caused by a key press. The requests are separate and are processed sequentially one after another. Change events are nevertheless communicated asynchronously to the server, so further input can be typed while event requests are being processed. LAZY - an event is triggered when there is a pause in editing the text. The length of the pause can be modified with setValueChangeTimeout(). A text change event is forced before a possible ComponentValueChangeEvent, even if the user did not keep a pause while entering the text. ON_BLUR - an event is triggered when the text field loses focus. TIMEOUT - an event is triggered after a timeout period. If more changes are made during this period, the event sent to the server-side includes the changes made up to the last change. The length of the timeout can be set with setValueChangeTimeout(). ON_CHANGE (default) - an event is triggered when fired client-side changeEvent.

text-field-value-change.xml

<view xmlns="http://jmix.io/schema/flowui/view">
    <layout justifyContent="BETWEEN" classNames="flex-row flex-wrap">
        <details summaryText="Default value change" opened="true" width="AUTO">
            <textField id="textField" placeholder="Start typing"/>
        </details>
        <details summaryText="Custom value change" opened="true" width="50%">
            <vbox padding="false">
                <textField id="valueChangeModeTextField" maxLength="140" helperText="0/140"/>
                <radioButtonGroup id="valueChangeModeRadioButtonGroup" label="ValueChangeMode"/>
            </vbox>
        </details>
    </layout>
</view>




TextFieldValueChangeSample.java

package io.jmix.uisamples.view.flowui.components.textfield.valuechange;

import com.google.common.base.Strings;
import com.vaadin.flow.component.AbstractField.ComponentValueChangeEvent;
import com.vaadin.flow.data.value.ValueChangeMode;
import io.jmix.flowui.Notifications;
import io.jmix.flowui.component.SupportsTypedValue.TypedValueChangeEvent;
import io.jmix.flowui.component.radiobuttongroup.JmixRadioButtonGroup;
import io.jmix.flowui.component.textfield.TypedTextField;
import io.jmix.flowui.kit.component.ComponentUtils;
import io.jmix.flowui.view.*;
import org.springframework.beans.factory.annotation.Autowired;

import java.util.Arrays;
import java.util.Map;
import java.util.function.Function;
import java.util.stream.Collectors;

@ViewController("text-field-value-change")
@ViewDescriptor("text-field-value-change.xml")
public class TextFieldValueChangeSample extends StandardView {

    @ViewComponent
    protected TypedTextField<String> valueChangeModeTextField;
    @ViewComponent
    protected JmixRadioButtonGroup<ValueChangeMode> valueChangeModeRadioButtonGroup;

    @Autowired
    protected Notifications notifications;

    @Subscribe
    protected void onInit(InitEvent event) {
        ComponentUtils.setItemsMap(valueChangeModeRadioButtonGroup, getValueChangeModeItemsMap());
        valueChangeModeRadioButtonGroup.setValue(ValueChangeMode.ON_CHANGE);
    }

    @Subscribe("valueChangeModeRadioButtonGroup")
    protected void onValueChangeModeRadioButtonValueChange(
            ComponentValueChangeEvent<JmixRadioButtonGroup<ValueChangeMode>, ValueChangeMode> event) {
        valueChangeModeTextField.setValueChangeMode(event.getValue());
    }

    @Subscribe("textField")
    protected void onTextFieldValueChange(TypedValueChangeEvent<TypedTextField<String>, String> event) {
        notifications.show("Text Changed: " + event.getValue());
    }

    @Subscribe("valueChangeModeTextField")
    protected void onValueChangeModeTextFieldValueChange(TypedValueChangeEvent<TypedTextField<String>, String> event) {
        TypedTextField<String> sourceTextField = event.getSource();
        sourceTextField.setHelperText(Strings.nullToEmpty(event.getValue()).length() + "/" + sourceTextField.getMaxLength());
    }

    protected Map<ValueChangeMode, String> getValueChangeModeItemsMap() {
        return Arrays.stream(ValueChangeMode.values())
                .collect(Collectors.toMap(Function.identity(), mode -> mode.name().replace('_', ' ')));
    }
}


