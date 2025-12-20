<Path>Components > ComboBox > ComboBox handling user input</Path>

The ComboBox component can handle user input if there is no suitable item in the list. addCustomValueSetListener() method is used for this purpose. In this example, a new value entered by the user is added to the list of items and becomes available for later use.

combobox-user-input.xml

<view xmlns="http://jmix.io/schema/flowui/view">
    <layout>
        <comboBox id="comboBox"
                  label="Magic Box"
                  allowCustomValue="true"
                  helperText="Entered value will be added to the items"/>
    </layout>
</view>




ComboBoxUserInputSample.java

package io.jmix.uisamples.view.flowui.components.combobox.userinput;

import com.google.common.collect.Lists;
import com.vaadin.flow.component.combobox.ComboBox;
import com.vaadin.flow.component.combobox.ComboBoxBase;
import io.jmix.flowui.Notifications;
import io.jmix.flowui.component.combobox.JmixComboBox;
import io.jmix.flowui.view.*;
import org.springframework.beans.factory.annotation.Autowired;

import java.util.List;

@ViewController("combobox-user-input")
@ViewDescriptor("combobox-user-input.xml")
public class ComboBoxUserInputSample extends StandardView {

    @ViewComponent
    protected JmixComboBox<String> comboBox;

    @Autowired
    protected Notifications notifications;

    protected List<String> items = Lists.newArrayList("One", "Two", "Tree");

    @Subscribe
    protected void onInit(InitEvent event) {
        comboBox.setItems(items);
    }

    @Subscribe("comboBox")
    protected void onComboBoxCustomValueSet(ComboBoxBase.CustomValueSetEvent<ComboBox<String>> event) {
        String customValue = event.getDetail();
        items.add(customValue);

        comboBox.setItems(items);
        comboBox.setValue(customValue);

        notifications.show(customValue + " added");
    }
}


