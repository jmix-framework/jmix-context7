<Path>Components > DatePicker > DatePicker with ThemeVariant</Path>

The DatePicker component has several theme variants: small align-left align-center align-right helper-above-field You can set these styles to the DatePicker component using the themeNames attribute either in the XML descriptor or in the view controller using constants from DatePickerVariant class.

date-picker-theme-variant.xml

<view xmlns="http://jmix.io/schema/flowui/view">
    <layout>
        <details summaryText="Theme Variant" opened="true">
            <hbox classNames="flex-wrap">
                <datePicker label="Standard DatePicker"/>
                <datePicker label="Small DatePicker" themeNames="small"/>
                <datePicker label="Helper-above-field Field" themeNames="helper-above-field"
                            helperText="Helper text"/>
            </hbox>
        </details>
        <details summaryText="Align Variant" opened="true">
            <hbox classNames="flex-wrap">
                <datePicker label="Standard align DatePicker" placeholder="Placeholder"/>
                <datePicker label="Align-center DatePicker" themeNames="align-center" placeholder="Placeholder"/>
                <datePicker label="Align-right DatePicker" themeNames="align-right" placeholder="Placeholder"/>
            </hbox>
        </details>
    </layout>
</view>




DatePickerThemeVariantSample.java

package io.jmix.uisamples.view.flowui.components.datepicker.themevariant;

import io.jmix.flowui.view.StandardView;
import io.jmix.flowui.view.ViewController;
import io.jmix.flowui.view.ViewDescriptor;

@ViewController("date-picker-theme-variant")
@ViewDescriptor("date-picker-theme-variant.xml")
public class DatePickerThemeVariantSample extends StandardView {
}


