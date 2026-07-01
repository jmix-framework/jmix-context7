<Path>Components > NumberField > NumberField with ThemeVariant</Path>

The NumberField component has several theme variants: small align-left align-center align-right helper-above-field You can set these styles to the NumberField component using the themeNames attribute either in the XML descriptor or in the view controller using constants from TextFieldVariant class.

number-field-theme-variant.xml

<view xmlns="http://jmix.io/schema/flowui/view">
    <layout>
        <details summaryText="Theme Variant" opened="true">
            <hbox wrap="true">
                <numberField label="Standard NumberField"/>
                <numberField label="Small NumberField" themeNames="small"/>
                <numberField id="helperAboveField" label="Helper-above-field Field" themeNames="helper-above-field"
                             helperText="Helper text"/>
            </hbox>
        </details>
        <details id="alignVariantDetails" summaryText="Align Variant" opened="true">
            <hbox wrap="true">
                <numberField label="Standard align NumberField" placeholder="Placeholder"/>
                <numberField label="Align-center NumberField" themeNames="align-center" placeholder="Placeholder"/>
                <numberField label="Align-right NumberField" themeNames="align-right" placeholder="Placeholder"/>
            </hbox>
        </details>
    </layout>
</view>




NumberFieldThemeVariantSample.java

package io.jmix.uisamples.view.flowui.components.numberfield.themevariant;

import io.jmix.flowui.view.StandardView;
import io.jmix.flowui.view.ViewController;
import io.jmix.flowui.view.ViewDescriptor;

@ViewController("number-field-theme-variant")
@ViewDescriptor("number-field-theme-variant.xml")
public class NumberFieldThemeVariantSample extends StandardView {
}


