<Path>Add-ons > AI Chat > AiCodeBlock > Simple AiCodeBlock</Path>

`aiCodeBlock` displays a fragment of source code with syntax highlighting, an optional language label, and actions for copying and wrapping the code. Inside a conversation `aiMessageList` uses it automatically for every fenced code block of an assistant message.

A nested `code` element holds multi-line source, wrapped in `CDATA` so that it arrives verbatim. Write the element with the `aichat` prefix, as `aichat:code`.

The `code` attribute holds a single line instead, and accepts a message key, which is useful when the source is kept in a message bundle.

The `language` attribute does two things: it puts a label in the block's header, and it tells the highlighter which grammar to apply. `AiCodeBlockLanguage` holds the common language ids as constants.

`highlight="false"` keeps the header and the label and renders the code plain, as the last block shows. Omitting the language removes the header too.

A block takes the width of its content and never exceeds the width of its container.


ai-code-block-simple.xml

<view xmlns="http://jmix.io/schema/flowui/view"
      xmlns:aichat="http://jmix.io/schema/aichat/ui">
    <layout>
        <vbox width="100%" maxWidth="60em" padding="false">
            <h4 text="msg://javaSection.title"/>
            <aichat:aiCodeBlock id="javaBlock" language="java">
                <aichat:code><![CDATA[@Subscribe("saveButton")
public void onSaveButtonClick(final ClickEvent<JmixButton> event) {
    Order order = dataManager.create(Order.class);
    order.setCustomer(customer);
    dataManager.save(order);

    notifications.show("Saved");
}]]></aichat:code>
            </aichat:aiCodeBlock>

            <h4 text="msg://sqlSection.title"/>
            <aichat:aiCodeBlock id="sqlBlock" language="sql">
                <aichat:code><![CDATA[select c.name, count(o.id) as order_count
from CUSTOMER c
    left join ORDER_ o on o.customer_id = c.id
group by c.name
order by order_count desc]]></aichat:code>
            </aichat:aiCodeBlock>

            <h4 text="msg://highlightOffSection.title"/>
            <aichat:aiCodeBlock id="highlightOffBlock" language="properties" highlight="false">
                <aichat:code><![CDATA[main.datasource.url=jdbc:postgresql://localhost:5432/demo
main.datasource.username=demo
jmix.core.available-locales=en,ru]]></aichat:code>
            </aichat:aiCodeBlock>
        </vbox>
    </layout>
</view>




AiCodeBlockSimpleSample.java

package io.jmix.uisamples.view.flowui.aichat.codeblock.simple;

import io.jmix.flowui.view.StandardView;
import io.jmix.flowui.view.ViewController;
import io.jmix.flowui.view.ViewDescriptor;

@ViewController("ai-code-block-simple")
@ViewDescriptor("ai-code-block-simple.xml")
public class AiCodeBlockSimpleSample extends StandardView {
}


