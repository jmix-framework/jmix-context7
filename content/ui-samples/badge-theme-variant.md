<Path>Components > Badge > Badge with ThemeVariant</Path>

The Badge component has several theme variants: normal primary success warning error contrast small pill You can set these styles to the HTML Container component using the themeNames attribute either in the XML descriptor or in the view controller using themeList of component.

badge-theme-variant.xml

<view xmlns="http://jmix.io/schema/flowui/view">
    <layout justifyContent="BETWEEN" classNames="horizontal-layout badge-theme-variant">
        <vbox width="AUTO" padding="false">
            <details summaryText="Style variant" opened="true">
                <hbox wrap="true">
                    <span text="Pending" themeNames="badge normal"/>
                    <span text="Confirmed" themeNames="badge success"/>
                    <span text="Warning" themeNames="badge warning"/>
                    <span text="Denied" themeNames="badge error"/>
                    <span text="On hold" themeNames="badge contrast"/>
                </hbox>
            </details>
            <details summaryText="Size variant" opened="true">
                <hbox wrap="true">
                    <span text="Medium badge" themeNames="badge normal"/>
                    <span text="Small badge" themeNames="badge small"/>
                </hbox>
            </details>
            <details summaryText="Visual variant" opened="true">
                <hbox wrap="true">
                    <span text="Primary badge" themeNames="badge normal primary"/>
                    <span text="Pill badge" themeNames="badge normal pill"/>
                </hbox>
            </details>
        </vbox>
        <details summaryText="Test badge" opened="true" width="35%">
            <vbox padding="false">
                <span id="testBadge" themeNames="badge normal"/>
                <checkboxGroup id="settingsCheckboxGroup" label="TestBadge settings" themeNames="vertical"/>
            </vbox>
        </details>
    </layout>
</view>




BadgeThemeVariantSample.java

package io.jmix.uisamples.view.flowui.components.badge.themevariant;

import com.vaadin.flow.component.html.Span;
import com.vaadin.flow.component.icon.Icon;
import com.vaadin.flow.component.icon.VaadinIcon;
import io.jmix.flowui.component.SupportsTypedValue.TypedValueChangeEvent;
import io.jmix.flowui.component.checkboxgroup.JmixCheckboxGroup;
import io.jmix.flowui.view.*;

import java.util.Collection;
import java.util.List;

@ViewController("badge-theme-variant")
@ViewDescriptor("badge-theme-variant.xml")
public class BadgeThemeVariantSample extends StandardView {

    @ViewComponent
    protected Span testBadge;
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
        testBadge.removeAll();
        testBadge.getElement().getThemeList().clear();
        testBadge.getElement().getThemeList().add("badge");

        event.getValue().stream()
                .map(String::toLowerCase)
                .forEach(this::applyTestBadgeTheme);
    }

    protected void applyTestBadgeTheme(String command) {
        if ("text".equalsIgnoreCase(command)) {
            testBadge.add(new Span("Badge text"));
        } else if ("icon".equalsIgnoreCase(command)) {
            Icon icon = VaadinIcon.SMILEY_O.create();
            icon.addClassName("badge-icon");
            testBadge.addComponentAsFirst(icon);
        } else {
            testBadge.getElement().getThemeList().add(command);
        }
    }

    protected List<String> getSettingsCheckboxGroupItems() {
        return List.of("Text", "Icon", "Primary", "Pill", "Success", "Warning", "Error", "Contrast", "Small");
    }
}




badge-theme-variant.css


.badge-theme-variant .badged-icon {
    box-sizing: content-box;
}

.badge-theme-variant .badged-icon[theme~="badge"] {
    min-width: 1em;
    gap: 0;
}


