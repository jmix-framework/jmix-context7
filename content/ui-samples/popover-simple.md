<Path>Components > Popover > Simple Popover</Path>

`Popover` is an overlay anchored to another component, called the target. Unlike a tooltip, it can contain any components and receive focus, so it suits rich, interactive content.

Declare `<popover>` in the descriptor and set the `target` attribute to the id of a component in the same view or fragment. The popover renders nothing in place. By default, it opens on a click on the target and closes on a click outside, on a second click on the target, or on <kbd>Esc</kbd>.

The popover and its content are regular components of the view: inject them with `@ViewComponent` and subscribe to their events. In this sample, the button inside the popover closes it with the `close()` method.


popover-simple.xml

<view xmlns="http://jmix.io/schema/flowui/view">
    <layout>
        <button id="infoButton" text="About Popover" icon="INFO_CIRCLE"/>
        <popover id="infoPopover" target="infoButton" width="20em">
            <vbox padding="false">
                <h4 text="Popover"/>
                <span text="An overlay anchored to its target component. It can contain any components: text, fields, buttons and layouts."/>
                <button id="closeButton" text="Close"/>
            </vbox>
        </popover>
    </layout>
</view>




PopoverSimpleSample.java

package io.jmix.uisamples.view.flowui.components.popover.simple;

import com.vaadin.flow.component.ClickEvent;
import com.vaadin.flow.component.popover.Popover;
import io.jmix.flowui.kit.component.button.JmixButton;
import io.jmix.flowui.view.*;

@ViewController("popover-simple")
@ViewDescriptor("popover-simple.xml")
public class PopoverSimpleSample extends StandardView {

    @ViewComponent
    private Popover infoPopover;

    @Subscribe(id = "closeButton", subject = "clickListener")
    public void onCloseButtonClick(ClickEvent<JmixButton> event) {
        infoPopover.close();
    }
}


