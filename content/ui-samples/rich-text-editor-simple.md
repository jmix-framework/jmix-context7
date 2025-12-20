<Path>Components > RichTextEditor > Simple RichTextEditor</Path>

RichTextEditor component allows the user to author text that has rich formatting. It allows you to format and style your text using boldface, italics, headings, lists, images, links, etc.

rich-text-editor-simple.xml

<view xmlns="http://jmix.io/schema/flowui/view">
    <layout>
        <richTextEditor id="richTextEditor" label="RichTextEditor" helperText="Helper text"/>
    </layout>
</view>




RichTextEditorSimpleSample.java

package io.jmix.uisamples.view.flowui.components.richtexteditor.simple;

import io.jmix.flowui.component.richtexteditor.RichTextEditor;
import io.jmix.flowui.view.*;

@ViewController("rich-text-editor-simple")
@ViewDescriptor("rich-text-editor-simple.xml")
public class RichTextEditorSimpleSample extends StandardView {

    @ViewComponent
    protected RichTextEditor richTextEditor;

    @Subscribe
    protected void onInit(InitEvent event) {
        richTextEditor.setValue("""
                <h1>H1</h1>
                <h2>H2</h2>
                <h3>H3</h3>
                <ul>
                <li><b>Bold</b></li>
                <li><i>Italic</i></li>
                <li><u>Underline</u></li>
                </ul>
                <ol>
                <li><s>Strikethrough</s></li>
                <li>Sub<sub>script</sub></li>
                <li>Super<sup>script</sup></li>
                <li><a href="https://www.jmix.io/" rel="nofollow">Link</a>
                </li>
                </ol>
                <pre>&lt;code-block/&gt;</pre>
                <blockquote>Blockquote</blockquote>
                """);
    }
}


