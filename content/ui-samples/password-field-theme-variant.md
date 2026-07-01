<Path>Components > PasswordField > PasswordField with ThemeVariant</Path>

The PasswordField component has several theme variants: small align-left align-center align-right helper-above-field You can set these styles to the PasswordField component using the themeNames attribute either in the XML descriptor or in the view controller using constants from TextFieldVariant class.

password-field-theme-variant.xml

<view xmlns="http://jmix.io/schema/flowui/view">
    <layout>
        <details summaryText="Theme Variant" opened="true">
            <hbox wrap="true">
                <passwordField label="Standard PasswordField"/>
                <passwordField label="Small PasswordField" themeNames="small"/>
                <passwordField id="helperAboveField" label="Helper-above-field Field" themeNames="helper-above-field"
                               helperText="Helper text"/>
            </hbox>
        </details>
        <details id="alignVariantDetails" summaryText="Align Variant" opened="true">
            <hbox wrap="true">
                <passwordField label="Standard align PasswordField" placeholder="Placeholder"/>
                <passwordField label="Align-center PasswordField" themeNames="align-center" placeholder="Placeholder"/>
                <passwordField label="Align-right PasswordField" themeNames="align-right" placeholder="Placeholder"/>
            </hbox>
        </details>
    </layout>
</view>




PasswordFieldThemeVariantSample.java

package io.jmix.uisamples.view.flowui.components.passwordfield.themevariant;

import io.jmix.flowui.view.StandardView;
import io.jmix.flowui.view.ViewController;
import io.jmix.flowui.view.ViewDescriptor;

@ViewController("password-field-theme-variant")
@ViewDescriptor("password-field-theme-variant.xml")
public class PasswordFieldThemeVariantSample extends StandardView {
}


