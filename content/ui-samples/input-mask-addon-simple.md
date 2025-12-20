<Path>Custom components > Integrating Vaadin add-ons > Simple Input Mask add-on</Path>

You can use any third-party Vaadin add-ons located in the [Vaadin Directory](https://vaadin.com/directory) or elsewhere.\
This example demonstrates the integration of the [Input Mask](https://vaadin.com/directory/component/input-mask-add-on) add-on.

To include the Vaadin add-on in your application, add the Vaadin Add-ons maven repository and the add-on dependency to the project's
`build.gradle`:

```groovy
repositories {
    maven {
        url 'https://maven.vaadin.com/vaadin-addons'
    }
    // ...
}

dependencies {
    implementation 'org.vaadin.addons.componentfactory:vcf-input-mask:2.2.0'
    // ...
}
```

After that, you can use the add-on components programmatically, see for example [InputMaskAddonSimpleSample.java]({currentPath}?tab=InputMaskAddonSimpleSample.java).

The add-on adds the `InputMask` component, based on the [imaskjs](https://imask.js.org/) JavaScript library.\
`InputMask` component allows to add an input mask to a Vaadin Flow component like `TextField` or `DatePicker`.\
More detailed information about mask pattern construction and configuration can be found on the website: [imaskjs :: guide](https://imask.js.org/guide.html#masked-pattern).


input-mask-addon-simple.xml

<view xmlns="http://jmix.io/schema/flowui/view">
    <layout>
        <textField id="phoneNumberField" label="msg://phoneNumberField.label"
                   helperText="msg://phoneNumberField.helperText">
            <suffix>
                <button id="showNumberBtn" icon="PHONE" themeNames="tertiary-inline"/>
            </suffix>
        </textField>
    </layout>
</view>




InputMaskAddonSimpleSample.java

package io.jmix.uisamples.view.flowui.customcomponents.vaadinaddons.inputmasksimple;

import com.vaadin.componentfactory.addons.inputmask.InputMask;
import com.vaadin.componentfactory.addons.inputmask.InputMaskOption;
import com.vaadin.flow.component.ClickEvent;
import io.jmix.flowui.Notifications;
import io.jmix.flowui.component.textfield.TypedTextField;
import io.jmix.flowui.kit.component.button.JmixButton;
import io.jmix.flowui.view.*;
import org.springframework.beans.factory.annotation.Autowired;

@ViewController("input-mask-addon-simple")
@ViewDescriptor("input-mask-addon-simple.xml")
public class InputMaskAddonSimpleSample extends StandardView {

    @ViewComponent
    private TypedTextField<String> phoneNumberField;

    @ViewComponent
    private MessageBundle messageBundle;

    @Autowired
    private Notifications notifications;

    @Subscribe
    public void onInit(InitEvent event) {
        InputMask inputMask = new InputMask(
                "+{1} 000 000-0000",
                InputMaskOption.lazy(false),
                InputMaskOption.overwrite(true)
        );
        inputMask.extend(phoneNumberField);
    }

    @Subscribe("showNumberBtn")
    public void onShowNumberBtnClick(ClickEvent<JmixButton> event) {
        notifications.show(messageBundle.formatMessage("showNumberMessage", phoneNumberField.getValue()));
    }
}


