<Path>Components > DropdownButton > DropdownButton with ThemeVariant</Path>

The DropdownButton component has several theme variants: primary success warning error large small icon tertiary You can set these styles to the Button component using the themeNames attribute either in the XML descriptor or in the view controller using constants from ComboButtonVariant or DropdownButtonVariant classes.

dropdown-button-theme-variant.xml

<view xmlns="http://jmix.io/schema/flowui/view">
    <layout justifyContent="BETWEEN" classNames="horizontal-layout">
        <vbox width="AUTO" padding="false">
            <details summaryText="Style variant" opened="true">
                <hbox wrap="true">
                    <dropdownButton id="primaryButton" text="Primary button" themeNames="primary">
                        <items>
                            <textItem id="textItem" text="Text"/>
                        </items>
                    </dropdownButton>
                    <dropdownButton id="successButton" text="Success button" themeNames="success">
                        <items>
                            <textItem id="textItem" text="Text"/>
                        </items>
                    </dropdownButton>
                    <dropdownButton id="warningButton" text="Warning button" themeNames="warning">
                        <items>
                            <textItem id="textItem" text="Text"/>
                        </items>
                    </dropdownButton>
                    <dropdownButton id="errorButton" text="Error button" themeNames="error">
                        <items>
                            <textItem id="textItem" text="Text"/>
                        </items>
                    </dropdownButton>
                </hbox>
            </details>

            <details summaryText="Size variant" opened="true">
                <hbox wrap="true">
                    <dropdownButton id="largeButton" text="Large button" themeNames="large">
                        <items>
                            <textItem id="textItem" text="Text"/>
                        </items>
                    </dropdownButton>
                    <dropdownButton id="medium" text="Medium button">
                        <items>
                            <textItem id="textItem" text="Text"/>
                        </items>
                    </dropdownButton>
                    <dropdownButton id="smallButton" text="Small button" themeNames="small">
                        <items>
                            <textItem id="textItem" text="Text"/>
                        </items>
                    </dropdownButton>
                </hbox>
            </details>

            <details summaryText="Visual variant" opened="true">
                <hbox wrap="true">
                    <dropdownButton id="iconButton" themeNames="icon" icon="SMILEY_O">
                        <items>
                            <textItem id="textItem" text="Text"/>
                        </items>
                    </dropdownButton>
                    <dropdownButton id="tertiaryButton" text="Tertiary button" themeNames="tertiary">
                        <items>
                            <textItem id="textItem" text="Text"/>
                        </items>
                    </dropdownButton>
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

import com.vaadin.flow.component.orderedlayout.VerticalLayout;
import io.jmix.flowui.UiComponents;
import io.jmix.flowui.component.SupportsTypedValue;
import io.jmix.flowui.component.checkboxgroup.JmixCheckboxGroup;
import io.jmix.flowui.icon.Icons;
import io.jmix.flowui.kit.component.combobutton.ComboButton;
import io.jmix.flowui.kit.component.dropdownbutton.AbstractDropdownButton;
import io.jmix.flowui.kit.component.dropdownbutton.DropdownButton;
import io.jmix.flowui.kit.icon.JmixFontIcon;
import io.jmix.flowui.view.*;
import org.springframework.beans.factory.annotation.Autowired;

import java.util.ArrayList;
import java.util.Collection;
import java.util.List;

@ViewController("dropdown-button-theme-variant")
@ViewDescriptor("dropdown-button-theme-variant.xml")
public class DropdownButtonThemeVariantSample extends StandardView {

    @ViewComponent
    private VerticalLayout testButtonPlaceholder;
    @ViewComponent
    private JmixCheckboxGroup<String> settingsCheckboxGroup;

    @Autowired
    private UiComponents uiComponents;
    @Autowired
    private Icons icons;

    private AbstractDropdownButton testButton;

    @Subscribe
    public void onInit(InitEvent event) {
        testButton = uiComponents.create(DropdownButton.class);
        testButton.addItem("textItem", "Text");
        testButtonPlaceholder.addComponentAsFirst(testButton);
        settingsCheckboxGroup.setItems(getSettingsCheckboxGroupItems());
    }

    @Subscribe("settingsCheckboxGroup")
    public void onSettingsValueChange(SupportsTypedValue.TypedValueChangeEvent<JmixCheckboxGroup<String>, Collection<String>> event) {
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
        testButton.setIcon(null);
        testButton.setText("");
        testButton.getThemeNames().clear();

        event.getValue().remove("ComboButton");

        event.getValue().stream()
                .map(String::toLowerCase)
                .forEach(this::applyTestButtonTheme);
    }

    public void applyTestButtonTheme(String command) {
        if ("text".equalsIgnoreCase(command)) {
            testButton.setText("Button text");
        } else if ("icon".equalsIgnoreCase(command)) {
            testButton.addThemeName(command);
            testButton.setIcon(icons.get(JmixFontIcon.SMILEY_O));
        } else {
            testButton.addThemeName(command);
        }
    }

    private List<String> getSettingsCheckboxGroupItems() {
            return List.of(
                    "Text", "Primary", "Success", "Warning", "Error", "Large", "Small", "Icon", "Tertiary");
    }
}


