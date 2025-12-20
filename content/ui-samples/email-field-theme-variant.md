<Path>Components > EmailField > EmailField with ThemeVariant</Path>

The EmailField component has several theme variants: small align-left align-center align-right helper-above-field You can set these styles to the EmailField component using the themeNames attribute either in the XML descriptor or in the view controller using constants from TextFieldVariant class.

email-field-theme-variant.xml

<view xmlns="http://jmix.io/schema/flowui/view">
    <layout>
        <details summaryText="Theme Variant" opened="true">
            <hbox classNames="flex-wrap">
                <emailField label="Standard EmailField"/>
                <emailField label="Small EmailField" themeNames="small"/>
                <emailField label="Helper-above-field Field" themeNames="helper-above-field"
                            helperText="Helper text"/>
            </hbox>
        </details>
        <details summaryText="Align Variant" opened="true">
            <hbox classNames="flex-wrap">
                <emailField label="Standard align EmailField" placeholder="Placeholder"/>
                <emailField label="Align-center EmailField" themeNames="align-center" placeholder="Placeholder"/>
                <emailField label="Align-right EmailField" themeNames="align-right" placeholder="Placeholder"/>
            </hbox>
        </details>
    </layout>
</view>




EmailFieldThemeVariantSample.java

package io.jmix.uisamples.view.flowui.components.emailfield.themevariant;

import io.jmix.flowui.view.StandardView;
import io.jmix.flowui.view.ViewController;
import io.jmix.flowui.view.ViewDescriptor;

@ViewController("email-field-theme-variant")
@ViewDescriptor("email-field-theme-variant.xml")
public class EmailFieldThemeVariantSample extends StandardView {
}


