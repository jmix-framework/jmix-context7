<Path>Layouts > Details > Details with ThemeVariant</Path>

The Details component has several theme variants: filled reverse small no-padding You can set these styles to the Details component using the themeNames attribute either in the XML descriptor or in the view controller using constants from DetailsVariant class.

details-theme-variant.xml

<view xmlns="http://jmix.io/schema/flowui/view">
    <layout>
        <details id="firstDetails" summaryText="Details 1" width="100%" opened="true">
            <checkboxGroup id="firstDetailsSettingsCheckboxGroup" label="Details themes" themeNames="horizontal"/>
        </details>
        <details id="secondDetails" summaryText="Details 2" width="100%">
            <checkboxGroup id="secondDetailsSettingsCheckboxGroup" label="Details themes" themeNames="horizontal"/>
        </details>
    </layout>
</view>




DetailsThemeVariantSample.java

package io.jmix.uisamples.view.flowui.containers.details.themevariant;

import com.vaadin.flow.component.details.Details;
import io.jmix.flowui.component.SupportsTypedValue.TypedValueChangeEvent;
import io.jmix.flowui.component.checkboxgroup.JmixCheckboxGroup;
import io.jmix.flowui.view.*;

import java.util.Collection;
import java.util.List;

@ViewController("details-theme-variant")
@ViewDescriptor("details-theme-variant.xml")
public class DetailsThemeVariantSample extends StandardView {

    @ViewComponent
    private Details firstDetails;
    @ViewComponent
    private JmixCheckboxGroup<String> firstDetailsSettingsCheckboxGroup;

    @ViewComponent
    private Details secondDetails;
    @ViewComponent
    private JmixCheckboxGroup<String> secondDetailsSettingsCheckboxGroup;

    @Subscribe
    public void onInit(InitEvent event) {
        List<String> settingsItems = getThemeList();

        firstDetailsSettingsCheckboxGroup.setItems(settingsItems);
        secondDetailsSettingsCheckboxGroup.setItems(settingsItems);
    }

    @Subscribe("firstDetailsSettingsCheckboxGroup")
    public void onFirstDetailsSettingsValueChange(
            TypedValueChangeEvent<JmixCheckboxGroup<String>, Collection<String>> event) {
        if (event.getValue() == null) {
            return;
        }

        applyDetailsSettings(event.getValue(), firstDetails);
    }

    @Subscribe("secondDetailsSettingsCheckboxGroup")
    public void onSecondDetailsSettingsValueChange(
            TypedValueChangeEvent<JmixCheckboxGroup<String>, Collection<String>> event) {
        if (event.getValue() == null) {
            return;
        }

        applyDetailsSettings(event.getValue(), secondDetails);
    }

    private void applyDetailsSettings(Collection<String> settings, Details targetDetails) {
        targetDetails.setThemeName("");

        settings.stream()
                .map(String::toLowerCase)
                .forEach(targetDetails::addThemeName);
    }

    private List<String> getThemeList() {
            return List.of("Filled", "Reverse", "Small", "No-padding");
    }
}


