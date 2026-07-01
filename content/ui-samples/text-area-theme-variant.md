<Path>Components > TextArea > TextArea with ThemeVariant</Path>

The TextArea component has several theme variants: small align-left align-center align-right helper-above-field You can set these styles to the TextArea component using the themeNames attribute either in the XML descriptor or in the view controller using constants from TextAreaVariant class.

text-area-theme-variant.xml

<view xmlns="http://jmix.io/schema/flowui/view">
    <layout>
        <details summaryText="Theme Variant" opened="true">
            <hbox wrap="true">
                <textArea label="Standard TextArea"/>
                <textArea label="Small TextArea" themeNames="small"/>
                <textArea id="helperAboveField" label="Helper-above-field Field" themeNames="helper-above-field"
                          helperText="Helper text"/>
            </hbox>
        </details>
        <details id="alignVariantDetails" summaryText="Align Variant" opened="true">
            <hbox wrap="true">
                <textArea label="Standard align TextArea" placeholder="Placeholder"/>
                <textArea label="Align-center TextArea" themeNames="align-center" placeholder="Placeholder"/>
                <textArea label="Align-right TextArea" themeNames="align-right" placeholder="Placeholder"/>
            </hbox>
        </details>
    </layout>
</view>




TextAreaThemeVariantSample.java

package io.jmix.uisamples.view.flowui.components.textarea.themevariant;

import io.jmix.flowui.view.StandardView;
import io.jmix.flowui.view.ViewController;
import io.jmix.flowui.view.ViewDescriptor;

@ViewController("text-area-theme-variant")
@ViewDescriptor("text-area-theme-variant.xml")
public class TextAreaThemeVariantSample extends StandardView {
}


