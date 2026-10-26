<Path>Add-ons > AI Chat > AiMessageInput > Simple AiMessageInput</Path>

`aiMessageInput` is the component witch the user writes a message.`aiChat` embeds it and configures it on your behalf.

The text reaches the application through `SubmitEvent`, which carries the submitted text.

The component does not expose the text it holds. There is no `getValue()` or `setValue()`, so the application cannot read what the user is typing, pre-fill the field with a suggested prompt, or clear it early. The text becomes available only when the user submits it.

The field grows with its content up to `maxRows` lines, ten by default, and scrolls internally beyond that. By default *Enter* submits the message and *Shift+Enter* inserts a line break; `enterAction="NEWLINE"` swaps the two, so that *Enter* inserts a line break and *Ctrl/Cmd+Enter* submits. The setting also tells mobile keyboards how to label their action key.

A standalone message input has no width of its own, so give it a width or place it in a container that constrains one.


ai-message-input-simple.xml

<view xmlns="http://jmix.io/schema/flowui/view"
      xmlns:aichat="http://jmix.io/schema/aichat/ui">
    <layout>
        <vbox width="100%" maxWidth="48em" padding="false">
            <aichat:aiMessageInput id="messageInput" width="100%"/>
            <hbox padding="false">
                <span text="msg://lastMessageLabel.text"/>
                <span id="lastMessageSpan"/>
            </hbox>

            <h4 text="msg://maxRowsSection.title"/>
            <aichat:aiMessageInput id="maxRowsInput" width="100%" maxRows="3"/>

            <h4 text="msg://newlineSection.title"/>
            <aichat:aiMessageInput id="newlineInput" width="100%" enterAction="NEWLINE"/>
        </vbox>
    </layout>
</view>




AiMessageInputSimpleSample.java

package io.jmix.uisamples.view.flowui.aichat.messageinput.simple;

import com.vaadin.flow.component.html.Span;
import io.jmix.aichat.component.messageinput.AiMessageInput;
import io.jmix.flowui.view.StandardView;
import io.jmix.flowui.view.Subscribe;
import io.jmix.flowui.view.ViewComponent;
import io.jmix.flowui.view.ViewController;
import io.jmix.flowui.view.ViewDescriptor;

@ViewController("ai-message-input-simple")
@ViewDescriptor("ai-message-input-simple.xml")
public class AiMessageInputSimpleSample extends StandardView {

    @ViewComponent
    private Span lastMessageSpan;

    @Subscribe("messageInput")
    public void onMessageInputSubmit(final AiMessageInput.SubmitEvent event) {
        lastMessageSpan.setText(event.getValue());
    }
}


