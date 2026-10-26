<Path>Add-ons > AI Chat > AiMessageInput > AiMessageInput slots and bands</Path>

The `prefix` and `suffix` elements put application controls inside the input box, before and after the field. A component declared in either element is injectable by id, exactly like a top-level component of the view.

Two theme variants change the layout. `no-header-footer-gap` removes the gap that separates a band from the box, so the band reads as a continuation of the field; it affects both bands at once and leaves the spacing inside the box untouched.

`fixed-toolbar` keeps the toolbar layout at all times. Without it the message input keeps its controls on one row while the text fits a single line, and reflows them into a row of their own once the text grows past it.


ai-message-input-slots.xml

<view xmlns="http://jmix.io/schema/flowui/view"
      xmlns:aichat="http://jmix.io/schema/aichat/ui">
    <layout>
        <vbox width="100%" maxWidth="48em" padding="false">
            <h4 text="msg://slotsSection.title"/>
            <aichat:aiMessageInput id="slotsInput" width="100%">
                <aichat:prefix>
                    <button id="promptLibraryButton"
                            icon="PLUS"
                            themeNames="tertiary"
                            title="msg://promptLibraryButton.title"/>
                </aichat:prefix>
                <aichat:suffix>
                    <button id="dictateButton"
                            icon="MICROPHONE"
                            themeNames="tertiary"
                            title="msg://dictateButton.title"/>
                </aichat:suffix>
            </aichat:aiMessageInput>

            <h4 text="msg://bandsSection.title"/>
            <aichat:aiMessageInput id="bandsInput" width="100%">
                <aichat:header>
                    <span text="msg://contextSpan.text"/>
                </aichat:header>
                <aichat:footer>
                    <span text="msg://disclaimer.text"/>
                </aichat:footer>
            </aichat:aiMessageInput>

            <h4 text="msg://noGapSection.title"/>
            <aichat:aiMessageInput id="noGapInput"
                                   width="100%"
                                   themeNames="no-header-footer-gap">
                <aichat:footer>
                    <span text="msg://disclaimer.text"/>
                </aichat:footer>
            </aichat:aiMessageInput>

            <h4 text="msg://fixedToolbarSection.title"/>
            <aichat:aiMessageInput id="fixedToolbarInput"
                                   width="100%"
                                   themeNames="fixed-toolbar">
                <aichat:prefix>
                    <button id="modelButton" text="msg://modelButton.text" themeNames="tertiary"/>
                </aichat:prefix>
            </aichat:aiMessageInput>
        </vbox>
    </layout>
</view>




AiMessageInputSlotsSample.java

package io.jmix.uisamples.view.flowui.aichat.messageinput.slots;

import com.vaadin.flow.component.ClickEvent;
import com.vaadin.flow.component.notification.Notification;
import io.jmix.flowui.Notifications;
import io.jmix.flowui.kit.component.button.JmixButton;
import io.jmix.flowui.view.MessageBundle;
import io.jmix.flowui.view.StandardView;
import io.jmix.flowui.view.Subscribe;
import io.jmix.flowui.view.ViewComponent;
import io.jmix.flowui.view.ViewController;
import io.jmix.flowui.view.ViewDescriptor;
import org.springframework.beans.factory.annotation.Autowired;

@ViewController("ai-message-input-slots")
@ViewDescriptor("ai-message-input-slots.xml")
public class AiMessageInputSlotsSample extends StandardView {

    @ViewComponent
    private MessageBundle messageBundle;

    @Autowired
    private Notifications notifications;

    @Subscribe("promptLibraryButton")
    public void onPromptLibraryButtonClick(final ClickEvent<JmixButton> event) {
        notifications.create(messageBundle.getMessage("promptLibraryButton.notification"))
                .withPosition(Notification.Position.BOTTOM_END)
                .show();
    }

    @Subscribe("dictateButton")
    public void onDictateButtonClick(final ClickEvent<JmixButton> event) {
        notifications.create(messageBundle.getMessage("dictateButton.notification"))
                .withPosition(Notification.Position.BOTTOM_END)
                .show();
    }
}


