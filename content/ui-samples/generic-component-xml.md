<Path>Custom components > Generic component XML</Path>

The component XML element can be used to create any UI component by FQN. In order to define component properties the nested property elements can be used. This can be convenient if you connect an addon or integrate a JavaScript component. In cases where full integration of a component into the framework is not needed, but you just need to support its use in XML.

generic-component-xml.xml

<view xmlns="http://jmix.io/schema/flowui/view">
    <layout>
        <component id="button" class="io.jmix.flowui.kit.component.button.JmixButton">
            <properties>
                <property name="text" value="Save"/>
                <property name="icon" value="ARCHIVE" type="ICON"/>
            </properties>
        </component>
    </layout>
</view>




GenericComponentXmlSample.java

package io.jmix.uisamples.view.flowui.customcomponents.genericxml;

import com.vaadin.flow.component.ClickEvent;
import io.jmix.flowui.Notifications;
import io.jmix.flowui.kit.component.button.JmixButton;
import io.jmix.flowui.view.StandardView;
import io.jmix.flowui.view.Subscribe;
import io.jmix.flowui.view.ViewController;
import io.jmix.flowui.view.ViewDescriptor;
import org.springframework.beans.factory.annotation.Autowired;

@ViewController("generic-component-xml")
@ViewDescriptor("generic-component-xml.xml")
public class GenericComponentXmlSample extends StandardView {

    @Autowired
    protected Notifications notifications;

    @Subscribe(id = "button", subject = "clickListener")
    public void onButtonClick(ClickEvent<JmixButton> event) {
        notifications.show("Saved!");
    }
}


