<Path>Components > Button > Simple Button</Path>

A button can contain a text, an icon, or both. The icon attribute defines an icon. A tooltip can be set using the title attribute.

button-simple.xml

<view xmlns="http://jmix.io/schema/flowui/view">
    <layout classNames="horizontal-layout">
        <button id="helloButton"
                text="Say hello!"
                title="Click me!"/>
        <button id="saveButton1"
                text="Save"
                icon="ARCHIVE"/>
        <button id="saveButton2"
                title="Save"
                icon="ARCHIVE"/>
    </layout>
</view>




ButtonSimpleSample.java

package io.jmix.uisamples.view.flowui.components.button.simple;

import com.vaadin.flow.component.ClickEvent;
import com.vaadin.flow.component.button.Button;
import io.jmix.flowui.Notifications;
import io.jmix.flowui.view.StandardView;
import io.jmix.flowui.view.Subscribe;
import io.jmix.flowui.view.ViewController;
import io.jmix.flowui.view.ViewDescriptor;
import org.springframework.beans.factory.annotation.Autowired;

@ViewController("button-simple")
@ViewDescriptor("button-simple.xml")
public class ButtonSimpleSample extends StandardView {

    @Autowired
    protected Notifications notifications;

    @Subscribe("helloButton")
    protected void onHelloButtonClick(ClickEvent<Button> event) {
        notifications.show("Hello, world!");
    }

    @Subscribe("saveButton1")
    protected void onSaveButton1Click(ClickEvent<Button> event) {
        event.getSource().getId()
                .ifPresent(this::save);
    }

    @Subscribe("saveButton2")
    protected void onSaveButton2Click(ClickEvent<Button> event) {
        event.getSource().getId()
                .ifPresent(this::save);
    }

    protected void save(String id) {
        notifications.show("Save called from " + id);
    }
}


