<Path>Layouts > Split > Split with ThemeVariant</Path>

The Split component has several theme variants: minimal small splitter-spacing You can set these styles to the Split component using the themeNames attribute either in the XML descriptor or in the view controller using constants from SplitLayoutVariant class.

split-theme-variant.xml

<view xmlns="http://jmix.io/schema/flowui/view">
    <layout>
        <split id="split" width="100%" height="100%" themeNames="splitter-spacing" splitterPosition="70">
            <vbox padding="false">
                <textArea label="TextArea1" width="100%" height="100%"/>
            </vbox>
            <checkboxGroup id="settingsCheckboxGroup" label="Splitter themes" themeNames="vertical"/>
        </split>
    </layout>
</view>




SplitThemeVariantSample.java

package io.jmix.uisamples.view.flowui.containers.split.themevariant;

import com.vaadin.flow.component.AbstractField.ComponentValueChangeEvent;
import io.jmix.flowui.component.checkboxgroup.JmixCheckboxGroup;
import io.jmix.flowui.component.splitlayout.JmixSplitLayout;
import io.jmix.flowui.view.*;

import java.util.Collection;
import java.util.List;

@ViewController("split-theme-variant")
@ViewDescriptor("split-theme-variant.xml")
public class SplitThemeVariantSample extends StandardView {

    @ViewComponent
    protected JmixSplitLayout split;
    @ViewComponent
    protected JmixCheckboxGroup<String> settingsCheckboxGroup;

    @Subscribe
    protected void onInit(InitEvent event) {
        List<String> settingsItems = List.of("Minimal", "Small", "Splitter-spacing");
        settingsCheckboxGroup.setItems(settingsItems);
    }

    @Subscribe("settingsCheckboxGroup")
    protected void onSettingsCheckboxGroupValueChange(ComponentValueChangeEvent<JmixCheckboxGroup<String>, Collection<String>> event) {
        if (event.getValue() == null) {
            return;
        }

        applySplitSettings(event.getValue());
    }

    protected void applySplitSettings(Collection<String> settings) {
        split.getElement().getThemeList().clear();

        settings.stream()
                .map(String::toLowerCase)
                .forEach(split::addThemeName);
    }
}

