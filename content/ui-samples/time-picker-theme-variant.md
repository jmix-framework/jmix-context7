<Path>Components > TimePicker > TimePicker with ThemeVariant</Path>

The TimePicker component has several theme variants: small align-left align-center align-right helper-above-field You can set these styles to the TimePicker component using the themeNames attribute either in the XML descriptor or in the view controller using constants from TimePickerVariant class.

time-picker-theme-variant.xml

<view xmlns="http://jmix.io/schema/flowui/view">
    <layout>
        <details summaryText="Theme Variant" opened="true">
            <hbox classNames="flex-wrap">
                <timePicker label="Standard TimePicker"/>
                <timePicker label="Small TimePicker" themeNames="small"/>
                <timePicker label="Helper-above-field Field" themeNames="helper-above-field"
                            helperText="Helper text"/>
            </hbox>
        </details>
        <details summaryText="Align Variant" opened="true">
            <hbox classNames="flex-wrap">
                <timePicker label="Standard align TimePicker" placeholder="Placeholder"/>
                <timePicker label="Align-center TimePicker" themeNames="align-center" placeholder="Placeholder"/>
                <timePicker label="Align-right TimePicker" themeNames="align-right" placeholder="Placeholder"/>
            </hbox>
        </details>
    </layout>
</view>




TimePickerThemeVariantSample.java

package io.jmix.uisamples.view.flowui.components.timepicker.themevariant;

import io.jmix.flowui.view.StandardView;
import io.jmix.flowui.view.ViewController;
import io.jmix.flowui.view.ViewDescriptor;

@ViewController("time-picker-theme-variant")
@ViewDescriptor("time-picker-theme-variant.xml")
public class TimePickerThemeVariantSample extends StandardView {
}


