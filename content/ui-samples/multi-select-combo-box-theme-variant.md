<Path>Components > MultiSelectComboBox > MultiSelectComboBox with ThemeVariant</Path>

The MultiSelectComboBox component has several theme variants: small align-left align-center align-right helper-above-field You can set these styles to the MultiSelectComboBox component using the themeNames attribute either in the XML descriptor or in the view controller using constants from MultiSelectComboBoxVariant class.

multi-select-combo-box-theme-variant.xml

<view xmlns="http://jmix.io/schema/flowui/view">
    <layout justifyContent="BETWEEN" classNames="flex-row flex-wrap">
        <vbox width="AUTO" padding="false">
            <details summaryText="Size variant" opened="true">
                <hbox classNames="flex-wrap">
                    <multiSelectComboBox id="defaultMultiSelectComboBox" label="Default MultiSelectComboBox"
                                         itemsEnum="io.jmix.uisamples.entity.Day"/>
                    <multiSelectComboBox id="smallMultiSelectComboBox" label="Small"
                                         themeNames="small"
                                         itemsEnum="io.jmix.uisamples.entity.Day"/>
                </hbox>
            </details>
            <details summaryText="Align variant" opened="true">
                <hbox classNames="flex-wrap">
                    <multiSelectComboBox id="alignLeftMultiSelectComboBox" label="Align left"
                                         themeNames="align-left"
                                         placeholder="Placeholder"
                                         itemsEnum="io.jmix.uisamples.entity.Day"/>
                    <multiSelectComboBox id="alignCenterMultiSelectComboBox" label="Align center"
                                         themeNames="align-center"
                                         placeholder="Placeholder"
                                         itemsEnum="io.jmix.uisamples.entity.Day"/>
                    <multiSelectComboBox id="alignRightMultiSelectComboBox" label="Align right"
                                         themeNames="align-right"
                                         placeholder="Placeholder"
                                         itemsEnum="io.jmix.uisamples.entity.Day"/>
                </hbox>
            </details>
            <details summaryText="Helper variant" opened="true">
                <hbox classNames="flex-wrap">
                    <multiSelectComboBox id="defaultHelperMultiSelectComboBox"
                                         label="Default helper"
                                         itemsEnum="io.jmix.uisamples.entity.Day"
                                         helperText="Default helper text"/>
                    <multiSelectComboBox id="helperAboveMultiSelectComboBox" label="Helper above field"
                                         themeNames="helper-above-field"
                                         itemsEnum="io.jmix.uisamples.entity.Day"
                                         helperText="Above helper text"/>
                </hbox>
            </details>
        </vbox>
        <details summaryText="Test MultiSelectComboBox" opened="true" width="35%">
            <vbox padding="false">
                <multiSelectComboBox id="testMultiSelectComboBox" itemsEnum="io.jmix.uisamples.entity.Day"/>
                <checkboxGroup id="settingsCheckboxGroup" label="TestMultiSelectComboBox settings"
                               themeNames="vertical"/>
            </vbox>
        </details>
    </layout>
</view>




MultiSelectComboBoxThemeVariantSample.java

package io.jmix.uisamples.view.flowui.components.multiselectcombobox.themevariant;

import io.jmix.flowui.component.SupportsTypedValue.TypedValueChangeEvent;
import io.jmix.flowui.component.checkboxgroup.JmixCheckboxGroup;
import io.jmix.flowui.component.multiselectcombobox.JmixMultiSelectComboBox;
import io.jmix.flowui.view.*;
import io.jmix.uisamples.entity.Day;

import java.util.Collection;
import java.util.List;

@ViewController("multi-select-combo-box-theme-variant")
@ViewDescriptor("multi-select-combo-box-theme-variant.xml")
public class MultiSelectComboBoxThemeVariantSample extends StandardView {

    @ViewComponent
    protected JmixMultiSelectComboBox<Day> testMultiSelectComboBox;
    @ViewComponent
    protected JmixCheckboxGroup<String> settingsCheckboxGroup;

    @Subscribe
    protected void onInit(InitEvent event) {
        settingsCheckboxGroup.setItems(getSettingsCheckboxGroupItems());
    }

    @Subscribe("settingsCheckboxGroup")
    protected void onSettingsValueChange(TypedValueChangeEvent<JmixCheckboxGroup<String>, Collection<String>> event) {
        if (event.getValue() == null) {
            return;
        }

        //clear
        testMultiSelectComboBox.setLabel("");
        testMultiSelectComboBox.setPlaceholder("");
        testMultiSelectComboBox.setHelperText("");
        testMultiSelectComboBox.setThemeName("");
        testMultiSelectComboBox.setReadOnly(false);

        event.getValue().stream()
                .map(String::toLowerCase)
                .forEach(this::applyTestComboBoxTheme);
    }

    protected void applyTestComboBoxTheme(String command) {
        switch (command) {
            case "label" -> testMultiSelectComboBox.setLabel("Label");
            case "placeholder" -> testMultiSelectComboBox.setPlaceholder("Placeholder");
            case "helper-text" -> testMultiSelectComboBox.setHelperText("Helper text");
            case "readonly" -> testMultiSelectComboBox.setReadOnly(true);
            default -> testMultiSelectComboBox.addThemeName(command);
        }
    }

    protected List<String> getSettingsCheckboxGroupItems() {
        return List.of("Label", "Placeholder", "Helper-Text", "Readonly", "Small", "Align-Left", "Align-Center",
                "Align-Right", "Helper-Above-Field");
    }
}


