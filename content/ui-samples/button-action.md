<Path>Components > Button > Button with Action</Path>

Any action present in the component implementing HasAction interface, or in the view itself, can be assigned to a button. A button gets values of same-name attributes from an assigned action, if these attributes are not defined in the button. In this example, the button takes its text from the action.

button-action.xml

<view xmlns="http://jmix.io/schema/flowui/view">
    <actions>
        <action id="someAction"
                text="Click me!"/>
    </actions>
    <layout>
        <button action="someAction"/>
    </layout>
</view>




ButtonActionSample.java

package io.jmix.uisamples.view.flowui.components.button.action;

import io.jmix.flowui.Notifications;
import io.jmix.flowui.kit.action.ActionPerformedEvent;
import io.jmix.flowui.view.StandardView;
import io.jmix.flowui.view.Subscribe;
import io.jmix.flowui.view.ViewController;
import io.jmix.flowui.view.ViewDescriptor;
import org.springframework.beans.factory.annotation.Autowired;

@ViewController("button-action")
@ViewDescriptor("button-action.xml")
public class ButtonActionSample extends StandardView {

    @Autowired
    protected Notifications notifications;

    @Subscribe("someAction")
    protected void onSomeActionButtonClick(ActionPerformedEvent event) {
        notifications.show("Action performed");
    }
}


