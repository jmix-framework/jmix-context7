<Path>Components > Markdown Components > Simple MarkdownEditor</Path>

The `MarkdownEditor` component allows the user to author text using the Markdown syntax. It provides an Edit/Preview
tab bar, a formatting toolbar with common Markdown actions, and keyboard shortcuts.

The component value is the Markdown source text. Switch to the *Preview* tab to see the rendered result.


markdown-editor-simple.xml

<view xmlns="http://jmix.io/schema/flowui/view">
    <layout>
        <markdownEditor id="markdownEditor" label="MarkdownEditor" helperText="Helper text"/>
    </layout>
</view>




MarkdownEditorSimpleSample.java

package io.jmix.uisamples.view.flowui.components.markdowncomponents.markdowneditorsimple;

import io.jmix.flowui.component.markdowneditor.MarkdownEditor;
import io.jmix.flowui.view.*;

@ViewController("markdown-editor-simple")
@ViewDescriptor("markdown-editor-simple.xml")
public class MarkdownEditorSimpleSample extends StandardView {

    @ViewComponent
    protected MarkdownEditor markdownEditor;

    @Subscribe
    protected void onInit(InitEvent event) {
        markdownEditor.setValue("""
                # Markdown Editor

                Use the **toolbar** or _keyboard shortcuts_ to format text.

                - Bulleted list item
                - [Link to jmix.io](https://www.jmix.io)
                - `inline code`

                > Switch to the **Preview** tab to see the rendered result.
                """);
    }
}


