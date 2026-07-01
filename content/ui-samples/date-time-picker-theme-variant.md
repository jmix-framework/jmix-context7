<Path>Components > DateTimePicker > DateTimePicker with ThemeVariant</Path>

The DateTimePicker component has several theme variants: small align-left align-center align-right helper-above-field You can set these styles to the DateTimePicker component using the themeNames attribute either in the XML descriptor or in the view controller using constants from DateTimePickerVariant class.

date-time-picker-theme-variant.xml

<view xmlns="http://jmix.io/schema/flowui/view">
    <layout>
        <details summaryText="Theme Variant" opened="true">
            <hbox wrap="true">
                <dateTimePicker label="Standard DateTimePicker"/>
                <dateTimePicker label="Small DateTimePicker" themeNames="small"/>
                <dateTimePicker id="helperAboveField" label="Helper-above-field Field" themeNames="helper-above-field"
                                helperText="Helper text"/>
            </hbox>
        </details>
        <details id="alignVariantDetails" summaryText="Align Variant" opened="true">
            <hbox wrap="true">
                <dateTimePicker id="dateTimePicker" label="Standard align DateTimePicker"
                                datePlaceholder="Placeholder" timePlaceholder="Placeholder"/>
                <dateTimePicker id="dateTimePicker2" label="Align-center DateTimePicker" themeNames="align-center"
                                datePlaceholder="Placeholder" timePlaceholder="Placeholder"/>
                <dateTimePicker id="dateTimePicker3" label="Align-right DateTimePicker" themeNames="align-right"
                                datePlaceholder="Placeholder" timePlaceholder="Placeholder"/>
            </hbox>
        </details>
    </layout>
</view>




DateTimePickerThemeVariantSample.java

package io.jmix.uisamples.view.flowui.components.datetimepicker.themevariant;

import io.jmix.flowui.view.StandardView;
import io.jmix.flowui.view.ViewController;
import io.jmix.flowui.view.ViewDescriptor;

@ViewController("date-time-picker-theme-variant")
@ViewDescriptor("date-time-picker-theme-variant.xml")
public class DateTimePickerThemeVariantSample extends StandardView {
}


