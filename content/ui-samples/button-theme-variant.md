<Path>Components > Button > Button with ThemeVariant</Path>

The Button component has several theme variants: primary success warning error large small icon tertiary You can set these styles to the Button component using the themeNames attribute either in the XML descriptor or in the view controller using constants from ButtonVariant class.

button-theme-variant.xml

<view xmlns="http://jmix.io/schema/flowui/view">
    <layout justifyContent="BETWEEN" classNames="horizontal-layout">
        <vbox width="AUTO" padding="false">
            <details summaryText="Style variant" opened="true">
                <hbox wrap="true">
                    <button id="primaryButton" text="Primary button" themeNames="primary"/>
                    <button id="successButton" text="Success button" themeNames="success"/>
                    <button id="warningButton" text="Warning button" themeNames="warning"/>
                    <button id="errorButton" text="Error button" themeNames="error"/>
                </hbox>
            </details>

            <details summaryText="Size variant" opened="true">
                <hbox wrap="true">
                    <button id="largeButton" text="Large button" themeNames="large"/>
                    <button id="medium" text="Medium button"/>
                    <button id="smallButton" text="Small button" themeNames="small"/>
                </hbox>
            </details>

            <details summaryText="Visual variant" opened="true">
                <hbox wrap="true">
                    <button id="iconButton" themeNames="icon" icon="SMILEY"/>
                    <button id="tertiaryButton" text="Tertiary button" themeNames="tertiary"/>
                </hbox>
            </details>
        </vbox>
        <details summaryText="Test button" opened="true" width="35%">
            <vbox padding="false">
                <button id="testButton"/>
                <checkboxGroup id="settingsCheckboxGroup" label="TestButton settings" themeNames="vertical"/>
            </vbox>
        </details>
    </layout>
</view>




ButtonThemeVariantSample.java

package io.jmix.uisamples.view.flowui.components.button.themevariant;

import io.jmix.flowui.component.SupportsTypedValue.TypedValueChangeEvent;
import io.jmix.flowui.component.checkboxgroup.JmixCheckboxGroup;
import io.jmix.flowui.icon.Icons;
import io.jmix.flowui.kit.component.button.JmixButton;
import io.jmix.flowui.kit.icon.JmixFontIcon;
import io.jmix.flowui.view.*;
import org.springframework.beans.factory.annotation.Autowired;

import java.util.Collection;
import java.util.List;

@ViewController("button-theme-variant")
@ViewDescriptor("button-theme-variant.xml")
public class ButtonThemeVariantSample extends StandardView {

    @ViewComponent
    private JmixButton testButton;
    @ViewComponent
    private JmixCheckboxGroup<String> settingsCheckboxGroup;
    @Autowired
    private Icons icons;

    @Subscribe
    public void onInit(InitEvent event) {
        settingsCheckboxGroup.setItems(getSettingsCheckboxGroupItems());
    }

    @Subscribe("settingsCheckboxGroup")
    public void onSettingsValueChange(TypedValueChangeEvent<JmixCheckboxGroup<String>, Collection<String>> event) {
        if (event.getValue() == null) {
            return;
        }

        //clear
        testButton.setIcon(null);
        testButton.setText("");
        testButton.setThemeName("");

        event.getValue().stream()
                .map(String::toLowerCase)
                .forEach(this::applyTestButtonTheme);
    }

    private void applyTestButtonTheme(String command) {
        if ("text".equalsIgnoreCase(command)) {
            testButton.setText("Button text");
        } else if ("icon".equalsIgnoreCase(command)) {
            testButton.addThemeName(command);
            testButton.setIcon(icons.get(JmixFontIcon.SMILEY));
        } else {
            testButton.addThemeName(command);
        }
    }

    private List<String> getSettingsCheckboxGroupItems() {
        return List.of(
                    "Text", "Primary", "Success", "Warning", "Error", "Large", "Small", "Icon", "Tertiary");
    }
}


