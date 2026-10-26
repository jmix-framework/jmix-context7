<Path>Add-ons > AI Chat > AiMessageList > AiMessageList with custom thinking indicator</Path>

While the list is generating and the answer is still empty, it shows an animated indicator of three pulsing dots, with a label beside it.

The `thinkingIndicator` element replaces the animation with any component, here an `image`. Only the animation is replaced, the label beside it stays.

The label is defined by `thinkingStages`: each stage sets the delay after which its text replaces the previous one.

The indicator is attached to the message being generated. A list switched to `GENERATING` while its last message is a user message shows nothing at all, so the button above adds an empty assistant message first.


ai-message-list-thinking-indicator.xml

<view xmlns="http://jmix.io/schema/flowui/view"
      xmlns:aichat="http://jmix.io/schema/aichat/ui">
    <layout expand="messageList">
        <hbox id="buttonsPanel" padding="false">
            <button id="toggleButton" text="msg://toggleButton.text"/>
        </hbox>
        <aichat:aiMessageList id="messageList" width="100%" height="100%">
            <aichat:thinkingIndicator>
                <image id="customIndicator"
                       resource="icons/jmix-icon.png"
                       alternateText="msg://customIndicator.alternateText"
                       width="1.75em"
                       height="1.75em"/>
            </aichat:thinkingIndicator>
            <aichat:thinkingStages>
                <aichat:thinkingStage delayMillis="600" text="msg://thinkingStage.thinking"/>
                <aichat:thinkingStage delayMillis="4000" text="msg://thinkingStage.stillThinking"/>
            </aichat:thinkingStages>
        </aichat:aiMessageList>
    </layout>
</view>




AiMessageListThinkingIndicatorSample.java

package io.jmix.uisamples.view.flowui.aichat.messagelist.thinkingindicator;

import com.vaadin.flow.component.ClickEvent;
import io.jmix.aichat.component.messagelist.AiMessageList;
import io.jmix.aichat.component.messagelist.AiMessageListItem;
import io.jmix.aichat.component.messagelist.GenerationState;
import io.jmix.flowui.kit.component.button.JmixButton;
import io.jmix.flowui.view.MessageBundle;
import io.jmix.flowui.view.StandardView;
import io.jmix.flowui.view.Subscribe;
import io.jmix.flowui.view.ViewComponent;
import io.jmix.flowui.view.ViewController;
import io.jmix.flowui.view.ViewDescriptor;

@ViewController("ai-message-list-thinking-indicator")
@ViewDescriptor("ai-message-list-thinking-indicator.xml")
public class AiMessageListThinkingIndicatorSample extends StandardView {

    @ViewComponent
    private AiMessageList messageList;
    @ViewComponent
    private MessageBundle messageBundle;

    @Subscribe("toggleButton")
    public void onToggleButtonClick(final ClickEvent<JmixButton> event) {
        if (messageList.getState() == GenerationState.GENERATING) {
            messageList.setState(GenerationState.IDLE);
            return;
        }

        // The indicator is attached to the message being generated, so the list needs a
        // trailing assistant message for it to appear on
        messageList.setItems(
                AiMessageListItem.user(messageBundle.getMessage("question.text")),
                AiMessageListItem.assistant(""));
        messageList.setState(GenerationState.GENERATING);
    }
}


