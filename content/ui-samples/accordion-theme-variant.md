<Path>Layouts > Accordion > Accordion with ThemeVariant</Path>

The AccordionPanel component has several theme variants: filled reverse small no-padding You can set these styles to the AccordionPanel component using the themeNames attribute either in the XML descriptor or in the view controller using constants from DetailsVariant class.

accordion-theme-variant.xml

<view xmlns="http://jmix.io/schema/flowui/view">
    <layout>
        <accordion id="mainAccordion" height="100%" width="100%">
            <accordionPanel id="firstPanel" summaryText="Panel 1">
                <checkboxGroup id="firstPanelSettingsCheckboxGroup" label="Panel themes" themeNames="horizontal"/>
            </accordionPanel>
            <accordionPanel id="secondPanel" summaryText="Panel 2">
                <checkboxGroup id="secondPanelSettingsCheckboxGroup" label="Panel themes" themeNames="horizontal"/>
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
    private AccordionPanel firstPanel;
    @ViewComponent
    private JmixCheckboxGroup<String> firstPanelSettingsCheckboxGroup;

    @ViewComponent
    private AccordionPanel secondPanel;
    @ViewComponent
    private JmixCheckboxGroup<String> secondPanelSettingsCheckboxGroup;

    @Subscribe
    public void onInit(InitEvent event) {
        List<String> settingsItems = getThemeList();
        firstPanelSettingsCheckboxGroup.setItems(settingsItems);
        secondPanelSettingsCheckboxGroup.setItems(settingsItems);
    }

    @Subscribe("firstPanelSettingsCheckboxGroup")
    public void onFirstPanelSettingsValueChange(
            TypedValueChangeEvent<JmixCheckboxGroup<String>, Collection<String>> event) {
        if (event.getValue() == null) {
            return;
        }

        applyPanelSettings(event.getValue(), firstPanel);
    }

    @Subscribe("secondPanelSettingsCheckboxGroup")
    public void onSecondPanelSettingsValueChange(
            TypedValueChangeEvent<JmixCheckboxGroup<String>, Collection<String>> event) {
        if (event.getValue() == null) {
            return;
        }

        applyPanelSettings(event.getValue(), secondPanel);
    }

    private void applyPanelSettings(Collection<String> settings, AccordionPanel targetPanel) {
        targetPanel.setThemeName("");

        settings.stream()
                .map(String::toLowerCase)
                .forEach(targetPanel::addThemeName);
    }

    private List<String> getThemeList() {
        return List.of("Filled", "Reverse", "Small", "No-padding");
    }
}


