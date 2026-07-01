<Path>Components > BigDecimalField > BigDecimalField with ThemeVariant</Path>

The BigDecimalField component has several theme variants: small align-left align-center align-right helper-above-field You can set these styles to the BigDecimalField component using the themeNames attribute either in the XML descriptor or in the view controller using constants from TextFieldVariant class.

big-decimal-field-theme-variant.xml

<view xmlns="http://jmix.io/schema/flowui/view">
    <layout>
        <details summaryText="Theme Variant" opened="true">
            <hbox wrap="true">
                <bigDecimalField label="Standard BigDecimalField" width="15em"/>
                <bigDecimalField label="Small BigDecimalField" themeNames="small" width="15em"/>
                <bigDecimalField id="helperAboveField" label="Helper-above-field Field" themeNames="helper-above-field"
                                 width="15em"
                                 helperText="Helper text"/>
            </hbox>
        </details>
        <details id="alignVariantDetails" summaryText="Align Variant" opened="true">
            <hbox wrap="true">
                <bigDecimalField label="Standard align BigDecimalField" width="15em" placeholder="Placeholder"/>
                <bigDecimalField label="Align-center BigDecimalField" themeNames="align-center" width="15em"
                                 placeholder="Placeholder"/>
                <bigDecimalField label="Align-right BigDecimalField" themeNames="align-right" width="15em"
                                 placeholder="Placeholder"/>
            </hbox>
        </details>
    </layout>
</view>




BigDecimalFieldThemeVariantSample.java

package io.jmix.uisamples.view.flowui.components.bigdecimalfield.themevariant;

import io.jmix.flowui.view.StandardView;
import io.jmix.flowui.view.ViewController;
import io.jmix.flowui.view.ViewDescriptor;

@ViewController("big-decimal-field-theme-variant")
@ViewDescriptor("big-decimal-field-theme-variant.xml")
public class BigDecimalFieldThemeVariantSample extends StandardView {
}


