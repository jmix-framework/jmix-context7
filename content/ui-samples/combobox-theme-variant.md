<Path>Components > ComboBox > ComboBox with ThemeVariant</Path>

The ComboBox component has several theme variants: small align-left align-center align-right helper-above-field You can set these styles to the ComboBox component using the themeNames attribute either in the XML descriptor or in the view controller using constants from ComboBoxVariant class.

combobox-theme-variant.xml

<view xmlns="http://jmix.io/schema/flowui/view">
    <layout justifyContent="BETWEEN" classNames="flex-row flex-wrap">
        <vbox width="AUTO" padding="false">
            <details summaryText="Size variant" opened="true">
                <hbox classNames="flex-wrap">
                    <comboBox id="defaultComboBox" label="Default ComboBox"
                              itemsEnum="io.jmix.uisamples.entity.CustomerGrade"/>
                    <comboBox id="smallComboBox" label="Small"
                              themeNames="small"
                              itemsEnum="io.jmix.uisamples.entity.CustomerGrade"/>
                </hbox>
            </details>
            <details summaryText="Align variant" opened="true">
                <hbox classNames="flex-wrap">
                    <comboBox id="alignLeftComboBox" label="Align left"
                              themeNames="align-left"
                              placeholder="Placeholder"
                              itemsEnum="io.jmix.uisamples.entity.CustomerGrade"/>
                    <comboBox id="alignCenterComboBox" label="Align center"
                              themeNames="align-center"
                              placeholder="Placeholder"
                              itemsEnum="io.jmix.uisamples.entity.CustomerGrade"/>
                    <comboBox id="alignRightComboBox" label="Align right"
                              themeNames="align-right"
                              placeholder="Placeholder"
                              itemsEnum="io.jmix.uisamples.entity.CustomerGrade"/>
                </hbox>
            </details>
            <details summaryText="Helper variant" opened="true">
                <hbox classNames="flex-wrap">
                    <comboBox id="defaultHelperComboBox" label="Default helper ComboBox"
                              itemsEnum="io.jmix.uisamples.entity.CustomerGrade"
                              helperText="Default helper text"/>
                    <comboBox id="helperAboveComboBox" label="Helper above field"
                              themeNames="helper-above-field"
                              itemsEnum="io.jmix.uisamples.entity.CustomerGrade"
                              helperText="Above helper text"/>
                </hbox>
            </details>
        </vbox>
        <details summaryText="Test ComboBox" opened="true" width="35%">
            <vbox padding="false">
                <comboBox id="testComboBox" itemsEnum="io.jmix.uisamples.entity.CustomerGrade"/>
                <checkboxGroup id="settingsCheckboxGroup" label="TestComboBox settings" themeNames="vertical"/>
            </vbox>
        </details>
    </layout>
</view>




ComboBoxThemeVariantSample.java

package io.jmix.uisamples.view.flowui.components.combobox.themevariant;

import io.jmix.flowui.component.SupportsTypedValue.TypedValueChangeEvent;
import io.jmix.flowui.component.checkboxgroup.JmixCheckboxGroup;
import io.jmix.flowui.component.combobox.JmixComboBox;
import io.jmix.flowui.view.*;
import io.jmix.uisamples.entity.CustomerGrade;

import java.util.Collection;
import java.util.List;

@ViewController("combobox-theme-variant")
@ViewDescriptor("combobox-theme-variant.xml")
public class ComboBoxThemeVariantSample extends StandardView {

    @ViewComponent
    protected JmixComboBox<CustomerGrade> testComboBox;
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
        testComboBox.setLabel("");
        testComboBox.setPlaceholder("");
        testComboBox.setHelperText("");
        testComboBox.setThemeName("");
        testComboBox.setReadOnly(false);

        event.getValue().stream()
                .map(String::toLowerCase)
                .forEach(this::applyTestComboBoxTheme);
    }

    protected void applyTestComboBoxTheme(String command) {
        switch (command) {
            case "label" -> testComboBox.setLabel("Label");
            case "placeholder" -> testComboBox.setPlaceholder("Placeholder");
            case "helper-text" -> testComboBox.setHelperText("Helper text");
            case "readonly" -> testComboBox.setReadOnly(true);
            default -> testComboBox.addThemeName(command);
        }
    }

    protected List<String> getSettingsCheckboxGroupItems() {
        return List.of("Label", "Placeholder", "Helper-Text", "Readonly", "Small", "Align-Left", "Align-Center",
                "Align-Right", "Helper-Above-Field");
    }
}




CustomerGrade.java

package io.jmix.uisamples.entity;

import io.jmix.core.metamodel.datatype.EnumClass;
import org.springframework.lang.Nullable;

public enum CustomerGrade implements EnumClass<Integer> {

    PREMIUM(10),
    HIGH(20),
    STANDARD(30);

    private final Integer id;

    CustomerGrade(Integer id) {
        this.id = id;
    }

    @Override
    public Integer getId() {
        return id;
    }

    @Nullable
    public static CustomerGrade fromId(Integer id) {
        for (CustomerGrade grade : CustomerGrade.values()) {
            if (grade.getId().equals(id))
                return grade;
        }
        return null;
    }
}


