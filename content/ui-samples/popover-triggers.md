<Path>Components > Popover > Popover opening triggers</Path>

A popover can open on a click on the target, when the pointer hovers over it, or when it receives focus. Enable the triggers with the `openOnClick`, `openOnHover` and `openOnFocus` attributes. `openOnClick` is on by default.

- A popover opened on hover closes when the pointer leaves both the target and the popover, so the user can move the pointer into it and click a link. `hoverDelay` and `hideDelay` set the delays in milliseconds before opening and closing.
- A popover opened on focus closes when the focus leaves the target and the popover. `focusDelay` sets the delay before opening.
- With all triggers disabled, the popover opens only from the controller with the `open()` method.

Whatever the trigger, a click outside the popover and the <kbd>Esc</kbd> key close it. To disable this, set `closeOnOutsideClick` and `closeOnEsc` to `false`.


popover-triggers.xml

<view xmlns="http://jmix.io/schema/flowui/view">
    <layout justifyContent="BETWEEN" classNames="horizontal-layout">
        <vbox padding="false" width="AUTO">
            <h4 text="Click"/>
            <button id="clickButton" text="Click me"/>
            <popover target="clickButton" width="16em">
                <span text="Opens on a click on the target. This is the default trigger."/>
            </popover>
        </vbox>
        <vbox padding="false" width="AUTO">
            <h4 text="Hover"/>
            <avatar id="homerAvatar" name="Homer Simpson"/>
            <popover target="homerAvatar" openOnClick="false" openOnHover="true" hoverDelay="300" hideDelay="300">
                <vbox padding="false" spacing="false">
                    <h5 text="Homer Simpson"/>
                    <span text="Safety inspector, Sector 7G"/>
                    <anchor href="mailto:homer@example.com" text="homer@example.com"/>
                </vbox>
            </popover>
        </vbox>
        <vbox padding="false" width="AUTO">
            <h4 text="Focus"/>
            <passwordField id="passwordField" label="Password"/>
            <popover target="passwordField" openOnClick="false" openOnFocus="true">
                <vbox padding="false" spacing="false">
                    <span text="The password must contain:"/>
                    <unorderedList>
                        <listItem text="at least 8 characters"/>
                        <listItem text="a letter and a digit"/>
                    </unorderedList>
                </vbox>
            </popover>
        </vbox>
        <vbox padding="false" width="AUTO">
            <h4 text="Programmatic"/>
            <hbox alignItems="BASELINE">
                <textField id="promoCodeField" label="Promo code"/>
                <button id="promoCodeHintButton" text="Where do I find it?" themeNames="tertiary"/>
            </hbox>
            <popover id="promoCodePopover" target="promoCodeField" openOnClick="false" width="16em">
                <span text="The promo code is printed on the back of your loyalty card."/>
            </popover>
        </vbox>
    </layout>
</view>




PopoverTriggersSample.java

package io.jmix.uisamples.view.flowui.components.popover.triggers;

import com.vaadin.flow.component.ClickEvent;
import com.vaadin.flow.component.popover.Popover;
import io.jmix.flowui.kit.component.button.JmixButton;
import io.jmix.flowui.view.*;

@ViewController("popover-triggers")
@ViewDescriptor("popover-triggers.xml")
public class PopoverTriggersSample extends StandardView {

    @ViewComponent
    private Popover promoCodePopover;

    @Subscribe(id = "promoCodeHintButton", subject = "clickListener")
    public void onPromoCodeHintButtonClick(ClickEvent<JmixButton> event) {
        promoCodePopover.open();
    }
}


