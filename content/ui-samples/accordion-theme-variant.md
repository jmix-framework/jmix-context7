<Path>Layouts > Accordion > Accordion with ThemeVariant</Path>

The AccordionPanel component has several theme variants: filled reverse small You can set these styles to the AccordionPanel component using the themeNames attribute either in the XML descriptor or in the view controller using constants from DetailsVariant class.

accordion-theme-variant.xml

<view xmlns="http://jmix.io/schema/flowui/view">
    <layout>
        <accordion id="mainAccordion" height="100%" width="100%">
            <accordionPanel id="firstPanel" summaryText="Panel 1">
                <checkboxGroup id="firstPanelSettingsCheckboxGroup" label="Panel themes"/>
            </accordionPanel>
            <accordionPanel id="secondPanel" summaryText="Panel 2">
                <checkboxGroup id="secondPanelSettingsCheckboxGroup" label="Panel themes"/>
            </accordionPanel>
        </accordion>
    </layout>
</view>




AccordionThemeVariantSample.java

package io.jmix.uisamples.view.flowui.containers.accordion.themevariant;

import com.vaadin.flow.component.accordion.AccordionPanel;
import io.jmix.flowui.component.SupportsTypedValue.TypedValueChangeEvent;
import io.jmix.flowui.component.checkboxgroup.JmixCheckboxGroup;
import io.jmix.flowui.view.*;

import java.util.Collection;
import java.util.List;

@ViewController("accordion-theme-variant")
@ViewDescriptor("accordion-theme-variant.xml")
public class AccordionThemeVariantSample extends StandardView {

    @ViewComponent
    protected AccordionPanel firstPanel;
    @ViewComponent
    protected JmixCheckboxGroup<String> firstPanelSettingsCheckboxGroup;

    @ViewComponent
    protected AccordionPanel secondPanel;
    @ViewComponent
    protected JmixCheckboxGroup<String> secondPanelSettingsCheckboxGroup;

    @Subscribe
    protected void onInit(InitEvent event) {
        List<String> settingsItems = List.of("Filled", "Reverse", "Small");

        firstPanelSettingsCheckboxGroup.setItems(settingsItems);
        secondPanelSettingsCheckboxGroup.setItems(settingsItems);
    }

    @Subscribe("firstPanelSettingsCheckboxGroup")
    protected void onFirstPanelSettingsValueChange(
            TypedValueChangeEvent<JmixCheckboxGroup<String>, Collection<String>> event) {
        if (event.getValue() == null) {
            return;
        }

        applyPanelSettings(event.getValue(), firstPanel);
    }

    @Subscribe("secondPanelSettingsCheckboxGroup")
    protected void onSecondPanelSettingsValueChange(
            TypedValueChangeEvent<JmixCheckboxGroup<String>, Collection<String>> event) {
        if (event.getValue() == null) {
            return;
        }

        applyPanelSettings(event.getValue(), secondPanel);
    }

    protected void applyPanelSettings(Collection<String> settings, AccordionPanel targetPanel) {
        targetPanel.setThemeName("");

        settings.stream()
                .map(String::toLowerCase)
                .forEach(targetPanel::addThemeName);
    }
}


