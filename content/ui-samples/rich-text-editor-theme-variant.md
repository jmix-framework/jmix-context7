<Path>Components > RichTextEditor > RichTextEditor with ThemeVariant</Path>

You can control the availability of the RichTextEditor using the ReadOnly and Enabled attributes.

rich-text-editor-theme-variant.xml

<view xmlns="http://jmix.io/schema/flowui/view">
    <layout>
        <hbox width="100%" wrap="true">
            <checkbox id="readOnlyCheckbox" label="Read only"/>
            <checkbox id="enabledCheckbox" label="Disabled"/>
        </hbox>
        <richTextEditor id="richTextEditor"/>
    </layout>
</view>




RichTextEditorThemeVariantSample.java

package io.jmix.uisamples.view.flowui.components.richtexteditor.themevariant;

import com.vaadin.flow.component.AbstractField.ComponentValueChangeEvent;
import io.jmix.flowui.component.checkbox.JmixCheckbox;
import io.jmix.flowui.component.richtexteditor.RichTextEditor;
import io.jmix.flowui.view.*;

@ViewController("rich-text-editor-theme-variant")
@ViewDescriptor("rich-text-editor-theme-variant.xml")
public class RichTextEditorThemeVariantSample extends StandardView {

    @ViewComponent
    protected RichTextEditor richTextEditor;

    @Subscribe
    protected void onInit(InitEvent event) {
        richTextEditor.setValue("<p><strong>Bold</strong> <em>Italic</em> <u>Underline</u> <s>Strikethrough</s></p>");
    }

    @Subscribe("readOnlyCheckbox")
    protected void onGutterCheckboxValueChange(ComponentValueChangeEvent<JmixCheckbox, Boolean> event) {
        richTextEditor.setReadOnly(event.getValue());
    }

    @Subscribe("enabledCheckbox")
    protected void onLineNumbersCheckboxValueChange(ComponentValueChangeEvent<JmixCheckbox, Boolean> event) {
        richTextEditor.setEnabled(!event.getValue());
    }
}


