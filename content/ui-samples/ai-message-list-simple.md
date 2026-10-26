<Path>Add-ons > AI Chat > AiMessageList > Simple AiMessageList</Path>

`aiMessageList` shows the conversation of a chat. `aiChat` embeds it and drives it for you; used on its own it displays a stored conversation, or a conversation the application drives itself.

Messages are items built with the `AiMessageListItem` factory methods. An item instance belongs to one list and may appear in it only once.

An assistant message is rendered as Markdown. A fenced code block becomes a real `aiCodeBlock`, with its language label, highlighting, and its own copy and wrap actions. A user message is rendered as plain text in a bubble, so Markdown in a user message is shown as typed.

A long user message is collapsed to a fixed height with a fade and a *Show more* toggle, as the last message here shows.


ai-message-list-simple.xml

<view xmlns="http://jmix.io/schema/flowui/view"
      xmlns:aichat="http://jmix.io/schema/aichat/ui">
    <layout expand="messageList">
        <aichat:aiMessageList id="messageList" width="100%" height="100%"/>
    </layout>
</view>




AiMessageListSimpleSample.java

package io.jmix.uisamples.view.flowui.aichat.messagelist.simple;

import io.jmix.aichat.component.messagelist.AiMessageList;
import io.jmix.aichat.component.messagelist.AiMessageListItem;
import io.jmix.flowui.view.MessageBundle;
import io.jmix.flowui.view.StandardView;
import io.jmix.flowui.view.Subscribe;
import io.jmix.flowui.view.ViewComponent;
import io.jmix.flowui.view.ViewController;
import io.jmix.flowui.view.ViewDescriptor;

@ViewController("ai-message-list-simple")
@ViewDescriptor("ai-message-list-simple.xml")
public class AiMessageListSimpleSample extends StandardView {

    private static final String ANSWER = """
            ## Loading orders

            Use `DataManager` with a JPQL query:

            ```java
            List<Order> orders = dataManager.load(Order.class)
                    .query("select o from Order o where o.customer = :customer")
                    .parameter("customer", customer)
                    .list();
            ```

            A few things to keep in mind:

            - add a fetch plan when you need referenced entities
            - use `maxResults` to page the result
            """;

    @ViewComponent
    private AiMessageList messageList;
    @ViewComponent
    private MessageBundle messageBundle;

    @Subscribe
    public void onInit(final InitEvent event) {
        messageList.setItems(
                AiMessageListItem.user(messageBundle.getMessage("transcript.question")),
                AiMessageListItem.assistant(ANSWER),
                AiMessageListItem.user(messageBundle.getMessage("transcript.longQuestion"))
        );
    }
}


