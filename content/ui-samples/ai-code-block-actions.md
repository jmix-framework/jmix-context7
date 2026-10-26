<Path>Add-ons > AI Chat > AiCodeBlock > AiCodeBlock actions</Path>

A code block carries two predefined actions. The copy action puts the raw source of the block on the clipboard. The wrap action switches the block between horizontal scrolling and soft wrapping.

`codeWrapped` sets the initial state of wrapping, as the second block shows. Replacing the code of a block resets wrapping to its default value.

Either action can be removed with `copyActionEnabled` or `wrapActionEnabled`. A disabled action is not rendered, which is why the third block has no buttons.

Without a language the block has no header row.


ai-code-block-actions.xml

<view xmlns="http://jmix.io/schema/flowui/view"
      xmlns:aichat="http://jmix.io/schema/aichat/ui">
    <layout>
        <vbox width="100%" maxWidth="60em" padding="false">
            <h4 text="msg://actionsSection.title"/>
            <aichat:aiCodeBlock id="actionsBlock" language="bash">
                <aichat:code><![CDATA[./gradlew -PvaadinProductionMode=true bootJar --stacktrace --info --no-daemon --refresh-dependencies]]></aichat:code>
            </aichat:aiCodeBlock>

            <h4 text="msg://wrappedSection.title"/>
            <aichat:aiCodeBlock id="wrappedBlock" language="bash" codeWrapped="true">
                <aichat:code><![CDATA[./gradlew -PvaadinProductionMode=true bootJar --stacktrace --info --no-daemon --refresh-dependencies]]></aichat:code>
            </aichat:aiCodeBlock>

            <h4 text="msg://noActionsSection.title"/>
            <aichat:aiCodeBlock id="noActionsBlock"
                                language="yaml"
                                copyActionEnabled="false"
                                wrapActionEnabled="false">
                <aichat:code><![CDATA[name: demo
services:
  db:
    image: postgres:17
    environment:
      POSTGRES_DB: demo
      POSTGRES_PASSWORD: demo]]></aichat:code>
            </aichat:aiCodeBlock>

            <h4 text="msg://noLanguageSection.title"/>
            <aichat:aiCodeBlock id="noLanguageBlock">
                <aichat:code><![CDATA[{
  "id": "a4f1c2e0-3b7d-4a91-8f56-2c0d9e8b1a34",
  "number": "ORD-00417",
  "amount": 149.90,
  "paid": false
}]]></aichat:code>
            </aichat:aiCodeBlock>
        </vbox>
    </layout>
</view>




AiCodeBlockActionsSample.java

package io.jmix.uisamples.view.flowui.aichat.codeblock.actions;

import io.jmix.flowui.view.StandardView;
import io.jmix.flowui.view.ViewController;
import io.jmix.flowui.view.ViewDescriptor;

@ViewController("ai-code-block-actions")
@ViewDescriptor("ai-code-block-actions.xml")
public class AiCodeBlockActionsSample extends StandardView {
}


