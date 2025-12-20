<Path>Components > IntegerField > IntegerField with ThemeVariant</Path>

The IntegerField component has several theme variants: small align-left align-center align-right helper-above-field You can set these styles to the IntegerField component using the themeNames attribute either in the XML descriptor or in the view controller using constants from TextFieldVariant class.

integer-field-theme-variant.xml

<view xmlns="http://jmix.io/schema/flowui/view">
    <layout>
        <details summaryText="Theme Variant" opened="true">
            <hbox classNames="flex-wrap">
                <integerField label="Standard IntegerField"/>
                <integerField label="Small IntegerField" themeNames="small"/>
                <integerField label="Helper-above-field Field" themeNames="helper-above-field"
                              helperText="Helper text"/>
            </hbox>
        </details>
        <details summaryText="Align Variant" opened="true">
            <hbox classNames="flex-wrap">
                <integerField label="Standard align IntegerField" placeholder="Placeholder"/>
                <integerField label="Align-center IntegerField" themeNames="align-center" placeholder="Placeholder"/>
                <integerField label="Align-right IntegerField" themeNames="align-right" placeholder="Placeholder"/>
            </hbox>
        </details>
    </layout>
</view>




IntegerFieldThemeVariantSample.java

package io.jmix.uisamples.view.flowui.components.integerfield.themevariant;

import io.jmix.flowui.view.StandardView;
import io.jmix.flowui.view.ViewController;
import io.jmix.flowui.view.ViewDescriptor;

@ViewController("integer-field-theme-variant")
@ViewDescriptor("integer-field-theme-variant.xml")
public class IntegerFieldThemeVariantSample extends StandardView {
}


