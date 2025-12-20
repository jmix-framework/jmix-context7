<Path>Components > Button > Button with programmatic Action</Path>

Button actions can be created programmatically in the view controller by deriving them from BaseAction class. In this example, the button text is created dynamically by overriding text attribute of the assigned action.

button-programmatic-action.xml

<view xmlns="http://jmix.io/schema/flowui/view">
    <layout>
        <button id="buttonAction"/>
    </layout>
</view>




ButtonProgrammaticActionSample.java

package io.jmix.uisamples.view.flowui.components.button.programmaticaction;

import io.jmix.flowui.Notifications;
import io.jmix.flowui.kit.action.BaseAction;
import io.jmix.flowui.kit.component.button.JmixButton;
import io.jmix.flowui.view.*;
import org.springframework.beans.factory.annotation.Autowired;

@ViewController("button-programmatic-action")
@ViewDescriptor("button-programmatic-action.xml")
public class ButtonProgrammaticActionSample extends StandardView {

    @ViewComponent
    protected JmixButton buttonAction;

    @Autowired
    protected Notifications notifications;

    @Subscribe
    protected void onInit(InitEvent event) {
        buttonAction.setAction(
                new BaseAction("action")
                        .withText("Click me!")
                        .withHandler(actionPerformedEvent -> notifications.show("Action performed"))
        );
    }
}


