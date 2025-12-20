<Path>Components > Button > Button with ThemeVariant</Path>

The Button component has several theme variants: primary success error contrast large small icon tertiary tertiary-inline You can set these styles to the Button component using the themeNames attribute either in the XML descriptor or in the view controller using constants from ButtonVariant class.

button-theme-variant.xml

<view xmlns="http://jmix.io/schema/flowui/view">
    <layout justifyContent="BETWEEN" classNames="flex-row flex-wrap">
        <vbox width="AUTO" padding="false">
            <details summaryText="Style variant" opened="true">
                <hbox classNames="flex-wrap">
                    <button id="primaryButton" text="Primary button" themeNames="primary"/>
                    <button id="successButton" text="Success button" themeNames="success"/>
                    <button id="errorButton" text="Error button" themeNames="error"/>
                    <button id="contrastButton" text="Contrast button" themeNames="contrast"/>
                </hbox>
            </details>

            <details summaryText="Size variant" opened="true">
                <hbox classNames="flex-wrap">
                    <button id="largeButton" text="Large button" themeNames="large"/>
                    <button id="medium" text="Medium button"/>
                    <button id="smallButton" text="Small button" themeNames="small"/>
                </hbox>
            </details>

            <details summaryText="Visual variant" opened="true">
                <hbox classNames="flex-wrap">
                    <button id="iconButton" themeNames="icon" icon="SMILEY_O"/>
                    <button id="tertiaryButton" text="Tertiary button" themeNames="tertiary"/>
                    <button id="tertiaryInlineButton" text="Tertiary-inline button" themeNames="tertiary-inline"/>
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

import com.vaadin.flow.component.icon.VaadinIcon;
import io.jmix.flowui.component.SupportsTypedValue.TypedValueChangeEvent;
import io.jmix.flowui.component.checkboxgroup.JmixCheckboxGroup;
import io.jmix.flowui.kit.component.button.JmixButton;
import io.jmix.flowui.view.*;

import java.util.Collection;
import java.util.List;

@ViewController("button-theme-variant")
@ViewDescriptor("button-theme-variant.xml")
public class ButtonThemeVariantSample extends StandardView {

    @ViewComponent
    protected JmixButton testButton;
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
        testButton.setIcon(null);
        testButton.setText("");
        testButton.setThemeName("");

        event.getValue().stream()
                .map(String::toLowerCase)
                .forEach(this::applyTestButtonTheme);
    }

    protected void applyTestButtonTheme(String command) {
        if ("text".equalsIgnoreCase(command)) {
            testButton.setText("Button text");
        } else if ("icon".equalsIgnoreCase(command)) {
            testButton.addThemeName(command);
            testButton.setIcon(VaadinIcon.SMILEY_O.create());
        } else {
            testButton.addThemeName(command);
        }
    }

    protected List<String> getSettingsCheckboxGroupItems() {
        return List.of("Text", "Primary", "Success", "Error", "Contrast",
                "Large", "Small", "Icon", "Tertiary", "Tertiary-inline");
    }
}


