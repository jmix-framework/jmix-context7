<Path>Components > DropdownButton > DropdownButton with ThemeVariant</Path>

The DropdownButton component has several theme variants: primary success error contrast large small icon tertiary tertiary-inline You can set these styles to the Button component using the themeNames attribute either in the XML descriptor or in the view controller using constants from ComboButtonVariant or DropdownButtonVariant classes.

dropdown-button-theme-variant.xml

<view xmlns="http://jmix.io/schema/flowui/view">
    <layout justifyContent="BETWEEN" classNames="flex-row flex-wrap">
        <vbox width="AUTO" padding="false">
            <details summaryText="Style variant" opened="true">
                <hbox classNames="flex-wrap">
                    <dropdownButton id="primaryButton" text="Primary button" themeNames="primary"/>
                    <dropdownButton id="successButton" text="Success button" themeNames="success"/>
                    <dropdownButton id="errorButton" text="Error button" themeNames="error"/>
                    <dropdownButton id="contrastButton" text="Contrast button" themeNames="contrast"/>
                </hbox>
            </details>

            <details summaryText="Size variant" opened="true">
                <hbox classNames="flex-wrap">
                    <dropdownButton id="largeButton" text="Large button" themeNames="large"/>
                    <dropdownButton id="medium" text="Medium button"/>
                    <dropdownButton id="smallButton" text="Small button" themeNames="small"/>
                </hbox>
            </details>

            <details summaryText="Visual variant" opened="true">
                <hbox classNames="flex-wrap">
                    <dropdownButton id="iconButton" themeNames="icon" icon="SMILEY_O"/>
                    <dropdownButton id="tertiaryButton" text="Tertiary button" themeNames="tertiary"/>
                    <dropdownButton id="tertiaryInlineButton" text="Tertiary-inline button"
                                    themeNames="tertiary-inline"/>
                </hbox>
            </details>
        </vbox>
        <details summaryText="Test button" opened="true" width="35%">
            <vbox id="testButtonPlaceholder" padding="false">
                <checkboxGroup id="settingsCheckboxGroup" label="TestButton settings" themeNames="vertical"/>
            </vbox>
        </details>
    </layout>
</view>




DropdownButtonThemeVariantSample.java

package io.jmix.uisamples.view.flowui.components.dropdownbutton.themevariant;

import com.vaadin.flow.component.icon.VaadinIcon;
import com.vaadin.flow.component.orderedlayout.VerticalLayout;
import io.jmix.flowui.UiComponents;
import io.jmix.flowui.component.SupportsTypedValue;
import io.jmix.flowui.component.checkboxgroup.JmixCheckboxGroup;
import io.jmix.flowui.kit.component.combobutton.ComboButton;
import io.jmix.flowui.kit.component.dropdownbutton.AbstractDropdownButton;
import io.jmix.flowui.kit.component.dropdownbutton.DropdownButton;
import io.jmix.flowui.view.*;
import org.springframework.beans.factory.annotation.Autowired;

import java.util.Collection;
import java.util.List;

@ViewController("dropdown-button-theme-variant")
@ViewDescriptor("dropdown-button-theme-variant.xml")
public class DropdownButtonThemeVariantSample extends StandardView {

    @ViewComponent
    protected VerticalLayout testButtonPlaceholder;
    @ViewComponent
    protected JmixCheckboxGroup<String> settingsCheckboxGroup;

    @Autowired
    protected UiComponents uiComponents;

    protected AbstractDropdownButton testButton;

    @Subscribe
    protected void onInit(InitEvent event) {
        testButton = uiComponents.create(DropdownButton.class);
        testButtonPlaceholder.addComponentAsFirst(testButton);
        settingsCheckboxGroup.setItems(getSettingsCheckboxGroupItems());
    }

    @Subscribe("settingsCheckboxGroup")
    protected void onSettingsValueChange(SupportsTypedValue.TypedValueChangeEvent<JmixCheckboxGroup<String>, Collection<String>> event) {
        if (event.getValue() == null) {
            return;
        }

        if (event.getValue().contains("ComboButton")) {
            if (testButton instanceof DropdownButton) {
                testButton.removeFromParent();
                testButton = uiComponents.create(ComboButton.class);
                testButtonPlaceholder.addComponentAsFirst(testButton);
            }
        } else if (testButton instanceof ComboButton) {
            testButton.removeFromParent();
            testButton = uiComponents.create(DropdownButton.class);
            testButtonPlaceholder.addComponentAsFirst(testButton);
        }

        //clear
        testButton.setIconComponent(null);
        testButton.setText("");
        testButton.getThemeNames().clear();

        event.getValue().remove("ComboButton");

        event.getValue().stream()
                .map(String::toLowerCase)
                .forEach(this::applyTestButtonTheme);
    }

    protected void applyTestButtonTheme(String command) {
        if ("text".equalsIgnoreCase(command)) {
            testButton.setText("Button text");
        } else if ("icon".equalsIgnoreCase(command)) {
            testButton.addThemeName(command);
            testButton.setIconComponent(VaadinIcon.SMILEY_O.create());
        } else {
            testButton.addThemeName(command);
        }
    }

    protected List<String> getSettingsCheckboxGroupItems() {
        return List.of("ComboButton", "Text", "Primary", "Success", "Error", "Contrast",
                "Large", "Small", "Icon", "Tertiary", "Tertiary-inline");
    }
}


