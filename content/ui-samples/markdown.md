<Path>Components > Markdown Components > Markdown</Path>

The `markdown` component renders content written in the markdown syntax as HTML. It supports basic text formatting, lists,
links, and more. All content provided to the component is internally sanitized to prevent potentially dangerous HTML
from being rendered.


markdown.xml

<view xmlns="http://jmix.io/schema/flowui/view">
    <layout>
        <tabSheet id="tabSheet" width="100%">
            <tab id="declarativeTab" label="msg://declarativeTab.label">
                <markdown>
                    <content>
                        <![CDATA[
# Markdown Sample

This is a sample text that showcases the usage of a Markdown component in Jmix.

## Formatting:
Here is some formatting:

- **Bold text:** Use the `**` to make text **bold**.
- *Italic text:* Use the `*` tag to make text *italic*.

## Lists:
Here are some examples of lists:

### Ordered List:
1. First item
2. Second item
3. Third item

### Unordered List:
- Fruits
  - Apples 🍎
  - Bananas 🍌
  - Oranges 🍊
- Vegetables
  - Carrots
  - Broccoli

## Hyperlinks:
Hyperlinks can be added using the `[text](link)` construction:

[Visit jmix.io](https://www.jmix.io)
                        ]]>
                    </content>
                </markdown>
            </tab>
        </tabSheet>
    </layout>
</view>




MarkdownSample.java

package io.jmix.uisamples.view.flowui.components.markdowncomponents.markdown;

import com.vaadin.flow.component.markdown.Markdown;
import io.jmix.core.Resources;
import io.jmix.flowui.component.tabsheet.JmixTabSheet;
import io.jmix.flowui.view.*;
import org.springframework.beans.factory.annotation.Autowired;

@ViewController("markdown")
@ViewDescriptor("markdown.xml")
public class MarkdownSample extends StandardView {

    private static final String SRC_PATH = "META-INF/resources/markdown/markdown-component.md";

    @ViewComponent
    private JmixTabSheet tabSheet;
    @ViewComponent
    private MessageBundle messageBundle;

    @Autowired
    private Resources resources;

    @Subscribe
    public void onInit(InitEvent event) {
        String content = resources.getResourceAsString(SRC_PATH);

        Markdown markdown = new Markdown(content);
        tabSheet.add(messageBundle.getMessage("programmaticTab.label"), markdown);
    }
}


